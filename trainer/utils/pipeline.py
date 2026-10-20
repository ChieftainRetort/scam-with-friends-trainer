"""The tick loop: handlers -> processors -> drivers."""

from __future__ import annotations

import time
from typing import Protocol


class Handler(Protocol):
    name: str
    def poll(self) -> dict: ...


class Processor(Protocol):
    name: str
    def process(self, state: dict) -> dict: ...


class Driver(Protocol):
    name: str
    def emit(self, event: dict) -> None: ...


class Pipeline:
    def __init__(self, interval_ms: int = 50) -> None:
        self.interval = interval_ms / 1000
        self._handlers: list[Handler] = []
        self._processors: list[Processor] = []
        self._drivers: list[Driver] = []

    def add_handler(self, h: Handler) -> None:
        self._handlers.append(h)

    def add_processor(self, p: Processor) -> None:
        self._processors.append(p)

    def add_driver(self, d: Driver) -> None:
        self._drivers.append(d)

    def tick(self) -> dict:
        state: dict = {}
        for h in self._handlers:
            state.update(h.poll())
        if state.get("panic"):
            state["alive"] = False
        event: dict = {}
        for p in self._processors:
            event.update(p.process(state))
        for d in self._drivers:
            d.emit(event)
        return event

    def run_forever(self) -> None:
        while True:
            self.tick()
            time.sleep(self.interval)