"""Loaders for images, prüfplan-PDFs, base prompt and spec markdown files."""

from __future__ import annotations

import base64
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Literal

_PROJECT_ROOT = Path(__file__).resolve().parents[3]

DATA_DIR = _PROJECT_ROOT / "data"
SHEET_METAL_IMAGE_DIR = DATA_DIR / "kb" / "sm"
POTENTIAL_PDF_DIR = DATA_DIR / "optimisation_potential"
SCHEMA_DIR = DATA_DIR / "schema"
POTENTIAL_SPEC_DIR = SCHEMA_DIR / "optimisation_potential"
SUB_POTENTIAL_SPEC_DIR = SCHEMA_DIR / "sub_optimisation_potential"
BASE_PROMPT_PATH = SCHEMA_DIR / "1_prompt.md"


@dataclass(frozen=True)
class SubPotentialSpec:
    """Static spec of a sub-potential parsed from its markdown file."""

    subpotential_id: str
    subpotential_name: str
    checkpoint_typ: Literal["quantitativ", "qualitativ"] | None
    raw_markdown: str


def load_image_data_url(sheet_metal_id: str) -> str:
    """Load ``{id}.png`` and return it as a ``data:image/png;base64,...`` URL."""
    path = SHEET_METAL_IMAGE_DIR / f"{sheet_metal_id}.png"
    if not path.is_file():
        raise FileNotFoundError(f"Sheet-metal image not found: {path}")
    encoded = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:image/png;base64,{encoded}"


def load_pdf_base64(potential_id: str) -> str:
    """Load ``{id}.pdf`` and return its base64 encoding (no data-URL prefix)."""
    path = POTENTIAL_PDF_DIR / f"{potential_id}.pdf"
    if not path.is_file():
        raise FileNotFoundError(f"Prüfplan PDF not found: {path}")
    return base64.b64encode(path.read_bytes()).decode("ascii")


def load_base_prompt() -> str:
    return BASE_PROMPT_PATH.read_text(encoding="utf-8")


def load_potential_spec(potential_id: str) -> str:
    path = POTENTIAL_SPEC_DIR / f"{potential_id}.md"
    if not path.is_file():
        raise FileNotFoundError(f"Potential spec not found: {path}")
    return path.read_text(encoding="utf-8")


def _sp_prefix_for(potential_id: str) -> str:
    """Convert ``P01`` → ``SP01`` (sub-potential filename prefix)."""
    if not potential_id.startswith("P"):
        raise ValueError(
            f"Unexpected potential id '{potential_id}' (must start with 'P')."
        )
    return "SP" + potential_id[1:]


_H2_NAME_RE = re.compile(r"^\s*##\s*(?:Beispiel:\s*)?(.+?)\s*$", re.MULTILINE)
_CHECKPOINT_RE = re.compile(r"\b(quantitativ|qualitativ)\b", re.IGNORECASE)


def _parse_sub_potential_name(markdown: str, fallback: str) -> str:
    match = _H2_NAME_RE.search(markdown)
    if not match:
        return fallback
    heading = match.group(1).strip()
    # Typical form: "SP01_01 -  90°-Schweißverbindung..."
    if " - " in heading or " -  " in heading:
        return heading.split("-", 1)[1].strip()
    return heading


def _parse_checkpoint_typ(
    markdown: str,
) -> Literal["quantitativ", "qualitativ"] | None:
    match = _CHECKPOINT_RE.search(markdown)
    if not match:
        return None
    value = match.group(1).lower()
    if value == "quantitativ":
        return "quantitativ"
    return "qualitativ"


def discover_sub_potentials(potential_id: str) -> list[SubPotentialSpec]:
    """Find ``SP{N}_*.md`` files belonging to potential ``P{N}``."""
    prefix = _sp_prefix_for(potential_id)
    specs: list[SubPotentialSpec] = []
    for path in sorted(SUB_POTENTIAL_SPEC_DIR.glob(f"{prefix}_*.md")):
        sp_id = path.stem
        raw = path.read_text(encoding="utf-8")
        specs.append(
            SubPotentialSpec(
                subpotential_id=sp_id,
                subpotential_name=_parse_sub_potential_name(raw, sp_id),
                checkpoint_typ=_parse_checkpoint_typ(raw),
                raw_markdown=raw,
            )
        )
    return specs
