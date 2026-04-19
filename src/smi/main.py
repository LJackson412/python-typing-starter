"""Entry point for the sheet-metal optimisation-potential prototype."""

from __future__ import annotations

import asyncio
import logging

from smi.adapters.chat_model.factory import get_chat_model
from smi.config.logging import configure_logging
from smi.config.settings import settings


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

    # TODO: Adapter-Schicht load_img_data_url implementieren
    # python-typing-starter\src\smi\adapters\img_provider\file_system_img_provider.py

    # TODO: Service-Schicht: assess_sheet_metal implementieren
    # Verwendet python-typing-starter\src\smi\domain
    # Dort sind Schemas, Prompts und Definitionen 
    # Mapping muss implementiert werden P01 -> verwendet python-typing-starter\src\smi\domain\sub_potentials\p01_definitions.py für sub_potentials
    

    # TODO: Service-Schicht: render_report implementieren
    # ViewModel erstellen, z.B. mit Pydantic, um die Daten zu strukturieren für das Template
    # Template erstellen, mit Jinja2, und dann die Daten einfüllen


    logger.info("Fertig. Report: %s", report_path)


if __name__ == "__main__":
    asyncio.run(main())
