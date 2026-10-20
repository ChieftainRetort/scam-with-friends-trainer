# Contributing to Scam With Your Friends Trainer

Thanks for wanting to help out with the scam-with-friends-trainer project.

## Ground rules

- This is a hobbyist trainer/overlay tool for **Scam With Your Friends**. It is not affiliated with the game's developers.
- Do not submit code that targets other players' accounts, payment systems, or anything outside the local game client sandbox.
- Keep PRs focused. One feature or fix per PR.

## Workflow

1. Fork the repo and create a branch: `git checkout -b feat/handler-xyz`
2. Install deps: `pip install -r requirements.txt`
3. Run the trainer: `python -m trainer.bootstrap`
4. Run tests: `pytest tests/`
5. Open a PR describing what changed and how you tested it in-game.

## Style

- Python 3.11+, type hints on public functions.
- Handlers go in `handlers/`, processing logic in `processors/`, and output in `drivers/`.
- No hardcoded offsets — put them in `config/offsets.yaml`.

## Reporting bugs

Use the issue template and include your game build number and trainer version.