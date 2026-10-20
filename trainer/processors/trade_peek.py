"""Detects an open trade window and surfaces the peer's offer locally."""

from __future__ import annotations

from trainer.services.attach_service import AttachService
from trainer.services.memory_reader import MemoryReader
from trainer.config_loader import load_offsets


class TradePeek:
    name = "trade_peek"

    def __init__(self, attach: AttachService) -> None:
        self._reader = MemoryReader(attach)
        self._offsets = load_offsets()["trade"]

    def process(self, state: dict) -> dict:
        if not state.get("alive"):
            return {"trade": None}
        window = self._reader.read_ptr_abs(self._offsets["window_ptr"])
        if not window:
            return {"trade": None}
        peer = self._reader.read_cstring(window + self._offsets["peer_name"], 32)
        confirmed = bool(self._reader.read_u8(window + self._offsets["confirm_flag"]))
        return {"trade": {"peer": peer, "confirmed": confirmed}}