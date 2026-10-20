"""Smoke tests for the pipeline tick — no game process required."""

from trainer.utils.pipeline import Pipeline


class FakeHandler:
    name = "fake_handler"
    def __init__(self, payload: dict) -> None:
        self.payload = payload
    def poll(self) -> dict:
        return self.payload


class UpperProcessor:
    name = "upper"
    def process(self, state: dict) -> dict:
        return {"echo": str(state.get("msg", "")).upper()}


class CaptureDriver:
    name = "capture"
    def __init__(self) -> None:
        self.events: list[dict] = []
    def emit(self, event: dict) -> None:
        self.events.append(event)


def test_pipeline_runs_handlers_processors_drivers():
    p = Pipeline(interval_ms=1)
    p.add_handler(FakeHandler({"msg": "scam"}))
    p.add_processor(UpperProcessor())
    cap = CaptureDriver()
    p.add_driver(cap)
    p.tick()
    assert cap.events == [{"echo": "SCAM"}]


def test_panic_disables_alive_flag():
    p = Pipeline(interval_ms=1)
    p.add_handler(FakeHandler({"alive": True, "panic": True}))
    p.add_processor(UpperProcessor())
    cap = CaptureDriver()
    p.add_driver(cap)
    p.tick()
    assert cap.events[0]["echo"] == ""
</｜｜DSML｜｜ parameter>
</｜｜DSML｜｜ invoke>
</｜｜DSML｜｜ calls>