"""Reads the local player's inventory and emits spoofed loot rows for the overlay.

NOTE: this only affects the *local* overlay rendering. It does not modify
the game's memory or the server's view of your inventory.
"""

from __future__ import annotations

from trainer.services.attach_service import AttachService
from trainer.services.memory_reader import MemoryReader
from trainer.config_loader import load_offsets

RARITY_TAGS = {0: "common", 1: "uncommon", 2: "rare", 3: "epic", 4: "legendary"}


class LootSpoofer:
    name = "loot_spoofer"

    def __init__(self, attach: AttachService) -> None:
        self._reader = MemoryReader(attach)
        self._offsets = load_offsets()

    def process(self, state: dict) -> dict:
        if not state.get("alive"):
            return {"loot": []}
        inv = self._offsets["inventory"]
        base = self._reader.read_ptr(self._offsets["player"]["base"], self._offsets["player"]["inventory_ptr"])
        count = self._reader.read_u32(base + inv["item_count"])
        rows = []
        for i in range(min(count, 32)):
            addr = base + inv["slots"] + i * inv["item_id_stride"]
            item_id = self._reader.read_u32(addr)
            rarity = self._reader.read_u8(addr + 0x4)
            rows.append({"id": item_id, "rarity": RARITY_TAGS.get(rarity, "common")})
        return {"loot": rows}