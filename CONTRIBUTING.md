# Contributing to verifiabl.dev

## Adding a New Integration (4 Steps)

The entire contribution surface is **one Python file**. You never need to touch core files.

### 1. Scaffold

```bash
python scripts/scaffold.py --spec <openapi-spec-url> --name <name> --out mocks/<name>.py
```

### 2. Review and Edit

Open `mocks/<name>.py`. The scaffold generates routes from the spec — review the response shapes, trim to the most-used endpoints, keep it under 50 LOC.

### 3. Add Fixture Data

Create `fixtures/<name>.json` with realistic seed data. This lets contributors run the mock locally without real sandbox credentials.

### 4. Register

Add one row to [INTEGRATIONS.md](INTEGRATIONS.md) with your integration's name, spec URL, sandbox signup link, and your GitHub handle.

That's it. `BaseMock.__subclasses__()` autodiscovery picks up your new file at startup — no config changes needed.

## Local Dev

```bash
uv sync
cp .env.example .env
uv run python scripts/seed_universal.py
uv run uvicorn main:app --reload
```

No real sandbox credentials needed.

## Rules

- Mock files must subclass `BaseMock` and use the `@route()` decorator
- Keep mock files under 50 LOC
- Do not import from `auth.py`, `store.py`, or `main.py`
- Every mock must have a matching `fixtures/<name>.json`
- Do not add new core files — add to existing ones

## Code style

```bash
uv run ruff format .   # format
uv run ruff check .    # lint
```

Run both before committing. CI enforces the same checks.
