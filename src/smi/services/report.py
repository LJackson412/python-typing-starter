"""Render the assessment result as a standalone HTML report."""

from __future__ import annotations

import logging
from datetime import datetime
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, select_autoescape

from smi.domain.schema.optimisation_potential import OptimisationPotentialAssessment

logger = logging.getLogger(__name__)

_TEMPLATE_DIR = Path(__file__).resolve().parent.parent / "templates"
_PROJECT_ROOT = Path(__file__).resolve().parents[3]
_DEFAULT_OUTPUT_DIR = _PROJECT_ROOT / "output" / "reports"

_env = Environment(
    loader=FileSystemLoader(_TEMPLATE_DIR),
    autoescape=select_autoescape(["html", "html.j2"]),
)


def render_report(
    sheet_metal_id: str,
    image_data_url: str,
    potentials: list[OptimisationPotentialAssessment],
    output_dir: Path | None = None,
) -> Path:
    """Render the report and return the output path."""
    out_dir = output_dir or _DEFAULT_OUTPUT_DIR
    out_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_path = out_dir / f"{sheet_metal_id}_{timestamp}.html"

    template = _env.get_template("report.html.j2")
    html = template.render(
        sheet_metal_id=sheet_metal_id,
        image_data_url=image_data_url,
        potentials=potentials,
        generated_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    )
    out_path.write_text(html, encoding="utf-8")
    logger.info("HTML-Report geschrieben: %s", out_path)
    return out_path
