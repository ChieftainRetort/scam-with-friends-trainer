"""Registers global hotkeys (panic key, overlay toggle)."""

from __future__ import annotations

import keyboard


class HotkeyHandler:
    name = "hotkey_handler"

    def __init__(self, panic_key: str = "F12") -> None:
        self.panic_key = panic_key
        self._panic = False
        keyboard.add_hotkey(panic_key, self._on_panic)

    def _on_panic(self) -> None:
        self._panic = True

    def poll(self) -> dict:
        triggered = self._panic
        self._panic = False
        return {"panic": triggered}