"""Lädt eine Optimisation-Potenzial-PDF aus dem Dateisystem als base64-String."""

from __future__ import annotations

import base64
from pathlib import Path

PDF_BASE_DIR = Path("data/optimisation_potential")
PDF_SUFFIX = ".pdf"


def load_pdf_base64(potential_id: str) -> str:
    """Liest ``data/optimisation_potential/{potential_id}.pdf`` als base64.

    Der zurückgegebene String enthält **keinen** ``data:`` Prefix, da er direkt
    in einem ``HumanMessage``-``file``-Block (``source_type="base64"``,
    ``mime_type="application/pdf"``) verwendet wird.
    """
    path = PDF_BASE_DIR / f"{potential_id}{PDF_SUFFIX}"
    if not path.is_file():
        raise FileNotFoundError(
            f"PDF für potential_id={potential_id!r} nicht gefunden: {path}"
        )
    return base64.b64encode(path.read_bytes()).decode("ascii")
