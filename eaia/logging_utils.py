import json
import logging
import os
from typing import Any


def configure_logging(default_level: str = "INFO") -> None:
    """Configure app-wide logging.

    This is intentionally small and dependency-free so scripts can call it early.
    """
    level_name = os.getenv("LOG_LEVEL", default_level).upper()
    level = getattr(logging, level_name, logging.INFO)
    logging.basicConfig(level=level, format="%(asctime)s %(levelname)s %(name)s %(message)s")


def log_kv(logger: logging.Logger, message: str, **fields: Any) -> None:
    """Structured log helper without requiring extra deps."""
    if not fields:
        logger.info(message)
        return
    logger.info("%s %s", message, json.dumps(fields, ensure_ascii=False, sort_keys=True))
