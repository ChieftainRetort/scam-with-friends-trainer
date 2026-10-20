"""Dumps pipeline output to stdout for debugging."""

from __future__ import annotations

import json


class ConsoleDriver:
    name = "console_driver"

    def __init__(self, verbose: bool = False) -> None:
        self.verbose = verbose

    def emit(self, event: dict) -> None:
        if not self.verbose and not any(event.get(k) for k in ("loot", "trade", "chat", "panic")):
            return
        print(json.dumps(event, default=str))