# Repository Guidelines

The `shorts-download1121` workspace is still hardening; treat these notes as the contract for how we grow the pipeline scaffold until every module and asset lands.

## Project Structure & Module Organization
- `src/shorts_dl/` – Python package for download pipelines, HTTP/yt-dlp clients, and orchestration jobs; keep modules pure and inject filesystem/network helpers.
- `scripts/` – idempotent utilities run via `python scripts/<name>.py` for bootstrapping, fixture refreshes, and packaging chores.
- `tests/` – Pytest suites mirroring `src`, with shared data under `tests/fixtures/` and tiny media blobs in `assets/samples/`.
- `configs/` – YAML/JSON defaults plus `.env.example` describing every secret (cookies, ffmpeg path, cache dir). Environment overrides stay ignored by git.

## Build, Test & Development Commands
- `python -m venv .venv && source .venv/bin/activate` – shared virtual environment.
- `pip install -r requirements.txt` and `pip install -r requirements-dev.txt` – install runtime and tooling deps; keep both lists alphabetized.
- `python -m scripts.bootstrap` – create folders, verify ffmpeg, and pull lightweight reference media.
- `pytest -q && ruff check src tests && mypy src` – must pass locally before every push because CI runs the same trio.

## Coding Style & Naming Conventions
Target Python 3.11+, 4-space indents, `snake_case` for functions/modules, `PascalCase` for classes, and `UPPER_SNAKE_CASE` for env vars. Format with `black` (line length 100), lint with `ruff`, provide type hints, and keep docstrings concise and Google-style.

## Testing Guidelines
Place tests in `tests/test_<feature>.py`, mirroring the source tree. Prefer fixtures and dependency injection over sleeps or live traffic. Mock outbound requests with `responses` or `pytest`'s `monkeypatch`, store deterministic hashes in `tests/fixtures/checksums.json`, and maintain ≥85 % statement coverage via `pytest --cov=src --cov-report=term-missing`. Mark expensive scenarios with `@pytest.mark.slow`.

## Commit & Pull Request Guidelines
Follow Conventional Commits (`feat:`, `fix:`, `chore:`) with ≤72-character subjects plus `Refs #<issue>` footers when relevant. Rebase on `main`, attach CLI output or screenshots proving downloads still succeed, call out new env vars, and keep PRs narrowly scoped (<500 LOC).

## Security & Configuration Tips
Never commit `.env` files, cookies, or API keys. Validate incoming URLs before download helpers to avoid SSRF, keep files non-executable unless required

## 中文速記
- 專案結構：`src` 放核心程式，`scripts` 放工具腳本，`tests` 與 `assets/samples` 儲存測試與小型媒體。
- 建置流程：建立 `.venv` 後用 `pip install -r requirements*.txt` 安裝，再跑 `python -m scripts.bootstrap` 與 `pytest -q && ruff check && mypy`。
- 程式風格：Python 3.11、4 空白縮排、`black` + `ruff`、函式 `snake_case`、環境變數大寫底線。
- 測試與提交：測試覆蓋率至少 85%，慢測加 `@pytest.mark.slow`，提交遵守 Conventional Commits 並附執行證明。
