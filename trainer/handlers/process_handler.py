"""Polls the game process for liveness and exposes a read handle."""

from __future__ import annotations

from trainer.services.attach_service import AttachService


class ProcessHandler:
    name = "process_handler"

    def __init__(self, attach: AttachService) -> None:
        self._attach = attach
        self._last_alive = True

    def poll(self) -> dict:
        alive = self._attach.is_alive()
        if alive != self._last_alive:
            self._last_alive = alive
        return {
            "alive": alive,
            "pid": self._attach.pid if alive else None,
            "handle": self._attach.handle if alive else None,
        }