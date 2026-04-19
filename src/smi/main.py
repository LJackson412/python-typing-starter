"""Entry point for the sheet-metal optimisation-potential prototype."""

from __future__ import annotations

import asyncio
import logging

from smi.adapters.chat_model.factory import get_chat_model
from smi.config.logging import configure_logging
from smi.config.settings import settings
from smi.services.assessment import assess_sheet_metal
from smi.services.knowledge_base import load_image_data_url
from smi.services.report import render_report

logger = logging.getLogger("smi.main")

# --- Nutzer-Parameter ---------------------------------------------------
sheet_metal_id = "SM01"
optimisation_potential_ids = ["P01"]
# ------------------------------------------------------------------------


async def main() -> None:
    configure_logging()
    logger.info(
        "Starte Bewertung für %s mit Potenzialen %s (Modell=%s, concurrency=%d)",
        sheet_metal_id,
        optimisation_potential_ids,
        settings.OPENAI_MODEL,
        settings.LLM_MAX_CONCURRENCY,
    )

    chat_model = get_chat_model(model_name=settings.OPENAI_MODEL)

    image_data_url = load_image_data_url(sheet_metal_id)
    results = await assess_sheet_metal(
        sheet_metal_id=sheet_metal_id,
        optimisation_potential_ids=optimisation_potential_ids,
        image_data_url=image_data_url,
        chat_model=chat_model,
    )

    report_path = render_report(
        sheet_metal_id=sheet_metal_id,
        image_data_url=image_data_url,
        potentials=results,
    )
    logger.info("Fertig. Report: %s", report_path)


if __name__ == "__main__":
    asyncio.run(main())
