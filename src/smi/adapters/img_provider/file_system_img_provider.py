"""Lädt ein Blech-Bild aus dem Dateisystem als base64-data-URL."""

from __future__ import annotations

import base64
from pathlib import Path

IMG_BASE_DIR = Path("data/sheet_metal")
IMG_SUFFIX = ".png"
IMG_MIME_TYPE = "image/png"


def load_img_data_url(sheet_metal_id: str) -> str:
    """Liest ``data/sheet_metal/{sheet_metal_id}.png`` und gibt eine data-URL zurück.

    Die zurückgegebene URL kann direkt in einer ``HumanMessage`` als
    ``image_url``-Block verwendet oder in den HTML-Report eingebettet werden.
    """
    path = IMG_BASE_DIR / f"{sheet_metal_id}{IMG_SUFFIX}"
    if not path.is_file():
        raise FileNotFoundError(
            f"Bild für sheet_metal_id={sheet_metal_id!r} nicht gefunden: {path}"
        )
    b64 = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:{IMG_MIME_TYPE};base64,{b64}"
