"""Central logging configuration for the smi runtime."""

import logging

from smi.config.settings import settings


def _level(value: str) -> int:
    """Map a textual log level to a ``logging`` module constant."""
    return getattr(logging, value.upper(), logging.INFO)


def configure_logging() -> None:
    """Configure root and smi-specific loggers with a shared formatter."""
    handler = logging.StreamHandler()
    handler.setFormatter(
        logging.Formatter(
            fmt="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
    )

    root = logging.getLogger()
    root.handlers.clear()
    root.addHandler(handler)
    root.setLevel(_level(settings.ROOT_LOG_LEVEL))

    logging.getLogger("smi").setLevel(_level(settings.SMI_LOG_LEVEL))
