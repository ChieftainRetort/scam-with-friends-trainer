"""Thin wrapper around ReadProcessMemory with typed helpers."""

from __future__ import annotations

import struct

import win32process

from trainer.services.attach_service import AttachService


class MemoryReader:
    def __init__(self, attach: AttachService) -> None:
        self._attach = attach

    def _read(self, addr: int, size: int) -> bytes:
        if not self._attach.handle:
            raise RuntimeError("not attached")
        return win32process.ReadProcessMemory(self._attach.handle, addr, size)

    def read_u8(self, addr: int) -> int:
        return self._read(addr, 1)[0]

    def read_u32(self, addr: int) -> int:
        return struct.unpack("<I", self._read(addr, 4))[0]

    def read_ptr(self, base: int, offset: int) -> int:
        return self.read_u32(base + offset)

    def read_ptr_abs(self, addr: int) -> int:
        return self.read_u32(addr)

    def read_cstring(self, addr: int, max_len: int = 128) -> str:
        raw = self._read(addr, max_len)
        end = raw.find(b"\x00")
        if end >= 0:
            raw = raw[:end]
        return raw.decode("utf-8", errors="replace")