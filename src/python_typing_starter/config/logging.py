"""Central logging configuration for the rag_service runtime."""

import logging

from python_typing_starter.config.settings import settings


def _level(value: str) -> int:
    """Map a textual log level to a ``logging`` module constant.

    Args:
        value (str): Log level string such as ``INFO`` or ``DEBUG``.

    Returns:
        int: Numeric logging level. Defaults to ``logging.INFO`` if unknown.
    """
    return getattr(logging, value.upper(), logging.INFO)


def configure_logging() -> None:
    """Configure root and service-specific loggers with a shared formatter.

    Returns:
        None: Logging is configured via module-level side effects.
    """
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

    logging.getLogger("rag_service").setLevel(_level(settings.RAG_SERVICE_LOG_LEVEL))
    logging.getLogger("__main__").setLevel(_level(settings.RAG_SERVICE_LOG_LEVEL))
