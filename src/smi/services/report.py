"""Rendert die Bewertungsergebnisse als HTML-Report."""

from __future__ import annotations

import logging
from datetime import datetime
from pathlib import Path

from jinja2 import Environment, PackageLoader, select_autoescape

from smi.domain.schema.result import PotentialResult

logger = logging.getLogger("smi.services.report")


PROJECT_ROOT = Path(__file__).resolve().parents[4]

_DEFAULT_OUTPUT_DIR = PROJECT_ROOT / "output" / "sheet_metal"
_TIMESTAMP_FORMAT = "%Y%m%d_%H%M%S"

_env = Environment(
    loader=PackageLoader("smi", "templates"),
    autoescape=select_autoescape(["html", "j2", "html.j2"]),
    trim_blocks=True,
    lstrip_blocks=True,
)


def render_report(
    *,
    sheet_metal_id: str,
    image_data_url: str,
    results: list[PotentialResult],
    output_dir: Path = _DEFAULT_OUTPUT_DIR,
) -> Path:
    """Rendert den Report und schreibt ihn unter ``output_dir``.

    Dateiname folgt ``{sheet_metal_id}_{YYYYMMDD_HHMMSS}.html``.
    """
    now = datetime.now()
    filename = f"{sheet_metal_id}_{now.strftime(_TIMESTAMP_FORMAT)}.html"
    output_dir.mkdir(parents=True, exist_ok=True)
    path = output_dir / filename

    template = _env.get_template("report.html.j2")
    html = template.render(
        sheet_metal_id=sheet_metal_id,
        image_data_url=image_data_url,
        results=results,
        generated_at=now.strftime("%Y-%m-%d %H:%M:%S"),
    )
    path.write_text(html, encoding="utf-8")
    logger.info("Report geschrieben: %s", path)
    return path
