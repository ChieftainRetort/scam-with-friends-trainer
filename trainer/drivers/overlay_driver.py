"""Minimal always-on-top overlay window using pywin32 + tkinter."""

from __future__ import annotations

import tkinter as tk

from trainer.config_loader import OverlayCfg


class OverlayDriver:
    name = "overlay_driver"

    def __init__(self, cfg: OverlayCfg) -> None:
        self.cfg = cfg
        self._root = tk.Tk()
        self._root.overrideredirect(True)
        self._root.attributes("-topmost", True)
        self._root.attributes("-alpha", cfg.opacity)
        self._root.geometry("+40+40")
        self._label = tk.Label(
            self._root,
            text="scam-with-friends-trainer",
            font=(cfg.font, 11),
            fg="#9ef0a0",
            bg="#101014",
            justify="left",
            anchor="nw",
        )
        self._label.pack(fill="both", expand=True)

    def emit(self, event: dict) -> None:
        lines = ["scam-with-friends-trainer"]
        if event.get("trade"):
            t = event["trade"]
            lines.append(f"trade: {t['peer']} confirmed={t['confirmed']}")
        for row in event.get("loot", [])[:6]:
            lines.append(f"  [{row['rarity']}] #{row['id']}")
        for line in event.get("chat", [])[-3:]:
            lines.append(f"> {line}")
        self._label.config(text="\n".join(lines))
        self._root.update_idletasks()