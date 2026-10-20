"""Entry point. Boots the pipeline and wires handlers -> processors -> drivers."""

from __future__ import annotations

import logging
import sys

from rich.logging import RichHandler

from trainer.config_loader import load_config
from trainer.handlers.process_handler import ProcessHandler
from trainer.handlers.hotkey_handler import HotkeyHandler
from trainer.processors.loot_spoofer import LootSpoofer
from trainer.processors.trade_peek import TradePeek
from trainer.processors.chat_injector import ChatInjector
from trainer.drivers.overlay_driver import OverlayDriver
from trainer.drivers.console_driver import ConsoleDriver
from trainer.services.attach_service import AttachService
from trainer.utils.pipeline import Pipeline


def build_logger(level: str) -> logging.Logger:
    logging.basicConfig(
        level=level,
        format="%(message)s",
        handlers=[RichHandler(rich_tracebacks=True, show_path=False)],
    )
    return logging.getLogger("trainer")


def main() -> int:
    cfg = load_config()
    log = build_logger(cfg.trainer.log_level)
    log.info("scam-with-friends-trainer v%s starting", cfg.trainer.version)

    attach = AttachService(cfg)
    if not attach.wait_for_game():
        log.error("could not attach to %s", cfg.trainer.game_exe)
        return 1

    pipeline = Pipeline(interval_ms=cfg.pipeline.ingest_interval_ms)

    pipeline.add_handler(ProcessHandler(attach))
    pipeline.add_handler(HotkeyHandler(cfg.safety.panic_key))

    pipeline.add_processor(LootSpoofer(attach))
    pipeline.add_processor(TradePeek(attach))
    pipeline.add_processor(ChatInjector(attach))

    pipeline.add_driver(ConsoleDriver())
    if cfg.overlay.enabled:
        pipeline.add_driver(OverlayDriver(cfg.overlay))

    try:
        pipeline.run_forever()
    except KeyboardInterrupt:
        log.info("shutting down")
    finally:
        attach.detach()
    return 0


if __name__ == "__main__":
    sys.exit(main())