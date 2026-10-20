"""Shared log formatting used by bootstrap and tests."""

from __future__ import annotations

import logging

PREFIX = "[scam-with-friends-trainer]"


def get_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    if not logger.handlers:
        h = logging.StreamHandler()
        h.setFormatter(logging.Formatter(f"{PREFIX} %(levelname)s %(name)s: %(message)s"))
        logger.addHandler(h)
        logger.setLevel(logging.INFO)
    return logger