"""Kern-Service: Bewertung einer Blechkonstruktion je Subpotenzial."""

from __future__ import annotations

import logging
from dataclasses import dataclass

from langchain_core.language_models import BaseChatModel
from langchain_core.messages import HumanMessage
from langchain_core.runnables import RunnableConfig

from smi.adapters.pdf_provider import load_pdf_base64
from smi.config.settings import settings
from smi.domain.potentials.registry import get_potential
from smi.domain.prompts.prompt import create_prompt
from smi.domain.schema.result import PotentialResult, SubPotentialResult
from smi.domain.schema.sub_potential import (
    LLMSheetMetalSubPotential,
    SheetMetalSubPotential,
)
from smi.services.aggregation import aggregate_rating

logger = logging.getLogger("smi.services.assessment")


@dataclass(frozen=True, slots=True)
class _Task:
    """Interne Zuordnung einer Batch-Position zu Potenzial + Subpotenzial."""

    potential_id: str
    potential_name: str
    spec: SheetMetalSubPotential


def _build_human_message(
    *,
    spec: SheetMetalSubPotential,
    potential_id: str,
    potential_name: str,
    sheet_metal_id: str,
    image_data_url: str,
    pdf_base64: str,
) -> HumanMessage:
    """Baut den multimodalen HumanMessage-Content für ein Subpotenzial."""
    pdf_name = f"{potential_id}.pdf"
    prompt_text = create_prompt(
        potential_name=potential_name,
        subpotential_name=spec.subpotential_name,
        img_name=sheet_metal_id,
        pdf_name=pdf_name,
        llm_evaluation_goal=spec.llm_evaluation_goal,
        llm_check_method=spec.llm_check_method,
        potential_high=spec.llm_potenzial_rating_logic.high,
        potential_medium=spec.llm_potenzial_rating_logic.medium,
        potential_low=spec.llm_potenzial_rating_logic.low,
    )
    return HumanMessage(
        content=[
            {"type": "text", "text": prompt_text},
            {"type": "image_url", "image_url": {"url": image_data_url}},
            {
                "type": "file",
                "source_type": "base64",
                "mime_type": "application/pdf",
                "data": pdf_base64,
                "filename": pdf_name,
            },
        ]
    )


async def assess_sheet_metal(
    *,
    sheet_metal_id: str,
    potential_ids: list[str],
    chat_model: BaseChatModel,
    image_data_url: str,
) -> list[PotentialResult]:
    """Bewertet die angefragten Potenziale für eine Blechkonstruktion.

    Führt einen gemeinsamen ``abatch``-Aufruf über *alle* Subpotenziale aller
    angefragten Potenziale aus (maximiert ``LLM_MAX_CONCURRENCY``), fängt
    Einzel-Exceptions ab und aggregiert das Ergebnis pro Potenzial.
    """
    tasks: list[_Task] = []
    messages: list[HumanMessage] = []

    for pid in potential_ids:
        potential = get_potential(pid)
        pdf_b64 = load_pdf_base64(pid)
        logger.info(
            "Potenzial %s (%s) geladen, %d Subpotenziale",
            potential.potential_id,
            potential.potential_name,
            len(potential.subpotentials),
        )
        for sp in potential.subpotentials:
            tasks.append(
                _Task(
                    potential_id=potential.potential_id,
                    potential_name=potential.potential_name,
                    spec=sp,
                )
            )
            messages.append(
                _build_human_message(
                    spec=sp,
                    potential_id=potential.potential_id,
                    potential_name=potential.potential_name,
                    sheet_metal_id=sheet_metal_id,
                    image_data_url=image_data_url,
                    pdf_base64=pdf_b64,
                )
            )

    if not tasks:
        logger.warning("Keine Subpotenziale zu bewerten.")
        return []

    structured = chat_model.with_structured_output(LLMSheetMetalSubPotential)
    logger.info(
        "Starte abatch über %d Subpotenziale (max_concurrency=%d)",
        len(tasks),
        settings.LLM_MAX_CONCURRENCY,
    )
    raw_results = await structured.abatch(
        [[msg] for msg in messages],
        config=RunnableConfig(max_concurrency=settings.LLM_MAX_CONCURRENCY),
        return_exceptions=True,
    )

    # Ergebnisse je Potenzial sammeln, Reihenfolge der potential_ids erhalten.
    by_potential: dict[str, list[SubPotentialResult]] = {pid: [] for pid in potential_ids}
    potential_names: dict[str, str] = {}

    for task, raw in zip(tasks, raw_results, strict=True):
        potential_names[task.potential_id] = task.potential_name
        if isinstance(raw, BaseException):
            logger.exception(
                "LLM-Call fehlgeschlagen: sheet_metal_id=%s potential=%s sub=%s model=%s",
                sheet_metal_id,
                task.potential_id,
                task.spec.subpotential_id,
                settings.OPENAI_MODEL,
                exc_info=raw,
            )
            by_potential[task.potential_id].append(
                SubPotentialResult.from_error(spec=task.spec, exc=raw)
            )
            continue

        # with_structured_output liefert das Pydantic-Modell direkt.
        assert isinstance(raw, LLMSheetMetalSubPotential)
        logger.debug(
            "Bewertung erhalten: potential=%s sub=%s rating=%s confidence=%.2f",
            task.potential_id,
            task.spec.subpotential_id,
            raw.rating.value,
            raw.confidence,
        )
        by_potential[task.potential_id].append(
            SubPotentialResult.from_llm(spec=task.spec, llm=raw)
        )

    results: list[PotentialResult] = []
    for pid in potential_ids:
        subs = by_potential[pid]
        results.append(
            PotentialResult(
                potential_id=pid,
                potential_name=potential_names[pid],
                rating=aggregate_rating(subs),
                subpotentials=subs,
            )
        )
    return results
