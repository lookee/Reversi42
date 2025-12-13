<!-- Copilot instructions for Reversi42 - concise, actionable guidance for AI coding agents -->
# Reversi42 — Copilot / AI Agent Instructions

Purpose: give an AI coding agent immediate, actionable knowledge to be productive in this repository.

Big picture
- **Architecture:** modular layered Python project. Key layers: `src/ui` (presentation), `src/Board` (application), `src/Reversi` + `src/AI` (domain), `src/infrastructure` (persistence/config). See `docs/architecture/README.md` for diagrams and ADRs.
- **Entry points:** console scripts `reversi42` and `reversi42-server` (defined in `pyproject.toml`) map to `webgui.cli`.

Developer workflows (common tasks)
- Setup dev env: run `./scripts/setup_dev.sh` (creates `venv`, installs `requirements.txt` and `requirements-dev.txt`, runs a smoke test). `dev.sh` activates `venv` and runs `python3 -m webgui.cli`.
- Run app in dev: `./dev.sh` or `python3 -m webgui.cli` (dev server). `dev.sh` exports `PYTHONPATH=src`.
- Run tests: `./scripts/run_tests.sh` (project wrapper). For coverage: `pytest --cov=src tests/`.
- Quick installs: `pip install -e .` to work with source edits.

Project-specific conventions
- Source directory is `src/` and is added to `PYTHONPATH` in dev scripts. Prefer editable install or `PYTHONPATH=src` when running tools.
- AI/player configuration lives under `config/players/` and enabled players in `config/players/enabled/`. Example template: `config/players/00_AI_CONFIG_TEMPLATE.yaml`.
- Configuration precedence: code defaults < user config (`~/.reversi42/`) < env vars (`REVERSI42_*`) < CLI args. See `docs/architecture/README.md` section "Configuration Management".
- Formatting/linting: `black` line-length 100, `isort` profile=black, `pylint` rules in `pyproject.toml`.

Patterns to preserve when editing
- Domain-first: domain layer (`src/Reversi`, `src/AI`, `src/Players`) must not depend on `infrastructure` or `ui`.
- Immutable bitboard model: `BitboardGame` is immutable — prefer returning new state objects instead of in-place mutation (`src/Reversi/BitboardGame`).
- Player system: uses Strategy + Factory patterns. New players should subclass `Player` and register via `PlayerFactory` (`src/Players`).
- UI uses MVP for board/view separation (`src/Board`, `src/ui`). Keep view logic separate from business rules.

Integration points & external dependencies
- Web server: FastAPI + Uvicorn — check `pyproject.toml` dependencies and `webgui/` module.
- Opening book & AI engine: `src/AI/Apocalyptron` (search algorithms, transposition tables) and opening book loaders referenced in docs (`docs/architecture/opening-book.md`).
- Data files and installed config: package data and `config/*.yaml` are included by setuptools (see `pyproject.toml` `data-files` and `package-data`).

Tests and markers to use
- Pytest markers used: `asyncio`, `e2e`, `slow`, `integration`, `unit`, `webgui`, `backend`, `characterization`. See `pytest.ini` and `pyproject.toml` for defaults.
- Performance and optional tests are excluded by default; use explicit flags to include them.

Examples (use concrete commands)
- Start dev server: `./dev.sh --reload`
- Run unit tests only: `pytest -m "unit"`
- Run a single test quickly: `pytest tests/core/test_game_config.py::TestGameConfig::test_initial -q`
- Install editable: `pip install -e . && ./dev.sh`

When editing code
- Preserve layer boundaries and public APIs unless a change requires it. Update docs under `docs/` and add ADRs for design changes.
- Add tests for new behavior under `tests/` and use existing markers. Keep new long-running tests behind `slow` or `performance` markers.

Where to look first (quick pointers)
- `docs/architecture/README.md` — high-level architecture and data flows.
- `README.md` — quick start, features, and common commands.
- `scripts/setup_dev.sh`, `dev.sh` — environment setup and dev runner.
- `pyproject.toml` & `pytest.ini` — formatting, linting, test configuration, entry points.
- `src/Players`, `src/AI`, `src/Reversi`, `src/Board` — core domain + AI + presentation code to change for game logic or AI.

If unsure
- Run the dev smoke steps: `./scripts/setup_dev.sh` then `./dev.sh` and a small `pytest` selection. Ask for clarification and point to code examples (file paths above).

---
If you want, I can refine any section, add short code snippets, or translate this file to another language.
