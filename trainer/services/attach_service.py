"""Attaches to the ScamWithFriends.exe process and holds the handle."""

from __future__ import annotations

import time

import psutil
import win32api
import win32process

from trainer.config_loader import Config

PROCESS_QUERY_INFORMATION = 0x0400
PROCESS_VM_READ = 0x0010


class AttachService:
    def __init__(self, cfg: Config) -> None:
        self.cfg = cfg
        self.pid: int | None = None
        self.handle: int | None = None

    def _find_pid(self) -> int | None:
        for proc in psutil.process_iter(["name"]):
            if proc.info["name"] == self.cfg.trainer.game_exe:
                return proc.pid
        return None

    def wait_for_game(self) -> bool:
        deadline = time.time() + self.cfg.trainer.attach_timeout_ms / 1000
        while time.time() < deadline:
            pid = self._find_pid()
            if pid:
                self.pid = pid
                self.handle = win32api.OpenProcess(
                    PROCESS_QUERY_INFORMATION | PROCESS_VM_READ, False, pid
                )
                return True
            time.sleep(0.25)
        return False

    def is_alive(self) -> bool:
        if not self.pid:
            return False
        return psutil.pid_exists(self.pid)

    def detach(self) -> None:
        if self.handle:
            win32api.CloseHandle(self.handle)
        self.handle = None
        self.pid = None