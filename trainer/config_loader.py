"""Loads default.yaml + offsets.yaml into typed config objects."""

from __future__ import annotations

from pathlib import Path

import yaml
from pydantic import BaseModel, Field

ROOT = Path(__file__).resolve().parent.parent
CONFIG_DIR = ROOT / "config"


class TrainerCfg(BaseModel):
    name: str
    version: str
    game_exe: str
    attach_timeout_ms: int = 8000
    log_level: str = "INFO"


class PipelineCfg(BaseModel):
    ingest_interval_ms: int = 50
    processors: list[str] = Field(default_factory=list)
    drivers: list[str] = Field(default_factory=list)


class OverlayCfg(BaseModel):
    enabled: bool = True
    font: str = "Cascadia Mono"
    opacity: float = 0.85
    anchor: str = "top_left"


class SafetyCfg(BaseModel):
    require_confirm_hotkey: bool = True
    panic_key: str = "F12"
    disable_on_process_exit: bool = True


class Config(BaseModel):
    trainer: TrainerCfg
    pipeline: PipelineCfg
    overlay: OverlayCfg
    safety: SafetyCfg


def load_config() -> Config:
    with open(CONFIG_DIR / "default.yaml", "r", encoding="utf-8") as f:
        raw = yaml.safe_load(f)
    return Config(**raw)


def load_offsets() -> dict:
    with open(CONFIG_DIR / "offsets.yaml", "r", encoding="utf-8") as f:
        return yaml.safe_load(f)