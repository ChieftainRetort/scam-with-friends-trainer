"""Reads the local chat buffer and forwards new lines to the overlay."""

from __future__ import annotations

from collections import deque

from trainer.services.attach_service import AttachService
from trainer.services.memory_reader import MemoryReader
from trainer.config_loader import load_offsets


class ChatInjector:
    name = "chat_injector"

    def __init__(self, attach: AttachService, max_lines: int = 64) -> None:
        self._reader = MemoryReader(attach)
        self._offsets = load_offsets()["chat"]
        self._seen: deque[str] = deque(maxlen=max_lines)

    def process(self, state: dict) -> dict:
        if not state.get("alive"):
            return {"chat": []}
        buf = self._offsets["buffer"]
        stride = self._offsets["line_stride"]
        fresh = []
        for i in range(8):
            line = self._reader.read_cstring(buf + i * stride, 120)
            if line and line not in self._seen:
                self._seen.append(line)
                fresh.append(line)
        return {"chat": fresh}