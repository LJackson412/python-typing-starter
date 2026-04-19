"""Orchestration: build multimodal messages, run abatch, aggregate results."""

from __future__ import annotations

import logging
import re

from langchain_core.language_models import BaseChatModel
from langchain_core.messages import HumanMessage
from langchain_core.runnables import RunnableConfig

from smi.config.settings import settings
from smi.domain.schema.optimisation_potential import (
    OptimisationPotentialAssessment,
    aggregate_rating,
)
from smi.domain.schema.sub_optimisation_potential import (
    LLMSubPotentialAssessment,
    SubPotentialAssessment,
)
from smi.services.knowledge_base import (
    discover_sub_potentials,
    load_base_prompt,
    load_pdf_base64,
    load_potential_spec,
)

logger = logging.getLogger(__name__)


def _compose_prompt(
    base_prompt: str,
    potential_spec_md: str,
    sub_potential_spec_md: str,
) -> str:
    return (
        "# Basis-Prompt\n"
        f"{base_prompt.strip()}\n\n"
        "# Übergeordnetes Optimierungspotenzial (Spec)\n"
        f"{potential_spec_md.strip()}\n\n"
        "# Sub-Optimierungspotenzial (Spec)\n"
        f"{sub_potential_spec_md.strip()}\n\n"
        "# Aufgabe\n"
        "Bewerte ausschließlich das oben beschriebene Sub-Optimierungspotenzial "
        "auf Basis des beigefügten Bildes und der beigefügten Prüfplan-PDF. "
        "Gib das Ergebnis strukturiert gemäß dem vorgegebenen Schema zurück: "
        "`rating` (low/medium/high), `reason`, `evidence` (Liste beobachtbarer "
        "Hinweise), `confidence` (0.0–1.0)."
    )


def build_human_message(
    *,
    image_data_url: str,
    pdf_base64: str,
    pdf_filename: str,
    base_prompt: str,
    potential_spec_md: str,
    sub_potential_spec_md: str,
) -> HumanMessage:
    """Compose a multimodal HumanMessage with text, image and PDF blocks."""
    text = _compose_prompt(base_prompt, potential_spec_md, sub_potential_spec_md)
    return HumanMessage(
        content=[
            {"type": "text", "text": text},
            {"type": "image_url", "image_url": {"url": image_data_url}},
            {
                "type": "file",
                "source_type": "base64",
                "mime_type": "application/pdf",
                "data": pdf_base64,
                "filename": pdf_filename,
            },
        ]
    )


async def _assess_single_potential(
    *,
    sheet_metal_id: str,
    potential_id: str,
    image_data_url: str,
    base_prompt: str,
    chat_model: BaseChatModel,
) -> OptimisationPotentialAssessment:
    potential_spec_md = load_potential_spec(potential_id)
    potential_name = _extract_potential_name(potential_spec_md, potential_id)
    pdf_base64 = load_pdf_base64(potential_id)
    sub_specs = discover_sub_potentials(potential_id)

    if not sub_specs:
        logger.warning(
            "Keine Subpotenziale für %s gefunden (Ordner %s)",
            potential_id,
            "data/schema/sub_optimisation_potential",
        )
        return OptimisationPotentialAssessment(
            potential_id=potential_id,
            potential_name=potential_name,
            subpotentials=[],
            rating=aggregate_rating([]),
        )

    messages = [
        build_human_message(
            image_data_url=image_data_url,
            pdf_base64=pdf_base64,
            pdf_filename=f"{potential_id}.pdf",
            base_prompt=base_prompt,
            potential_spec_md=potential_spec_md,
            sub_potential_spec_md=spec.raw_markdown,
        )
        for spec in sub_specs
    ]

    structured = chat_model.with_structured_output(LLMSubPotentialAssessment)
    config: RunnableConfig = {"max_concurrency": settings.LLM_MAX_CONCURRENCY}
    raw_results = await structured.abatch(
        [[m] for m in messages],
        config=config,
        return_exceptions=True,
    )

    model_name = getattr(chat_model, "model_name", None) or getattr(
        chat_model, "model", "unknown"
    )
    assessments: list[SubPotentialAssessment] = []
    for spec, result in zip(sub_specs, raw_results, strict=True):
        if isinstance(result, BaseException):
            logger.exception(
                "LLM-Aufruf fehlgeschlagen "
                "(sheet_metal_id=%s, potential_id=%s, "
                "sub_potential_id=%s, model=%s): %s",
                sheet_metal_id,
                potential_id,
                spec.subpotential_id,
                model_name,
                result,
            )
            assessments.append(
                SubPotentialAssessment.from_error(
                    subpotential_id=spec.subpotential_id,
                    subpotential_name=spec.subpotential_name,
                    checkpoint_typ=spec.checkpoint_typ,
                    error=str(result),
                )
            )
            continue

        assessments.append(
            SubPotentialAssessment.from_llm(
                result,
                subpotential_id=spec.subpotential_id,
                subpotential_name=spec.subpotential_name,
                checkpoint_typ=spec.checkpoint_typ,
            )
        )
        logger.info(
            "Bewertung abgeschlossen: %s -> %s (confidence=%.2f)",
            spec.subpotential_id,
            result.rating.value,
            result.confidence,
        )

    return OptimisationPotentialAssessment(
        potential_id=potential_id,
        potential_name=potential_name,
        subpotentials=assessments,
        rating=aggregate_rating(assessments),
    )


async def assess_sheet_metal(
    sheet_metal_id: str,
    optimisation_potential_ids: list[str],
    image_data_url: str,
    chat_model: BaseChatModel,
) -> list[OptimisationPotentialAssessment]:
    """Assess a sheet-metal image across multiple parent potentials."""
    base_prompt = load_base_prompt()

    results: list[OptimisationPotentialAssessment] = []
    for potential_id in optimisation_potential_ids:
        logger.info("Starte Bewertung: %s / %s", sheet_metal_id, potential_id)
        result = await _assess_single_potential(
            sheet_metal_id=sheet_metal_id,
            potential_id=potential_id,
            image_data_url=image_data_url,
            base_prompt=base_prompt,
            chat_model=chat_model,
        )
        logger.info(
            "Gesamtbewertung %s: %s", potential_id, result.rating.value
        )
        results.append(result)
    return results


_POTENTIAL_NAME_RE = re.compile(r"##\s*(?:Beispiel:\s*)?[A-Z]\d+\s*[-–]\s*(.+)")


def _extract_potential_name(spec_md: str, fallback: str) -> str:
    for line in spec_md.splitlines():
        match = _POTENTIAL_NAME_RE.match(line.strip())
        if match:
            return match.group(1).strip()
    return fallback
