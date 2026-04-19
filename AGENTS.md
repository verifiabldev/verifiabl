# verifiabl.dev — Agent Instructions

Mock API server for AI coding agents. Schema-faithful responses, no real credentials needed.

## Commands

```bash
uv sync                                                          # install deps
cp .env.example .env                                             # first-time setup
uv run python scripts/seed_universal.py                          # seed local store
uv run uvicorn main:app --reload                                 # local dev server
uv run python -m unittest discover -s tests -p "test_*.py"      # run tests
uv run ruff format .                                             # format
uv run ruff check .                                              # lint
```

## Project structure

| File / Dir             | Responsibility                                                   |
| ---------------------- | ---------------------------------------------------------------- |
| `main.py`              | FastAPI app, auth middleware, mock router, all endpoints         |
| `auth.py`              | All auth and tier logic — no tier checks anywhere else           |
| `store.py`             | All data access — always via `store.read()` / `store.write()`    |
| `models.py`            | All dataclasses and enums — no inline dataclasses elsewhere      |
| `recorder.py`          | Sandbox recording against real APIs (verifiabl credentials only) |
| `worker.py`            | Cloudflare Workers entrypoint                                    |
| `mocks/base.py`        | `BaseMock`, `@route()` decorator — the mock contract             |
| `mocks/{name}.py`      | One file per integration; auto-discovered at startup             |
| `fixtures/{name}.json` | Seed data for local dev; every mock needs one                    |
| `scripts/`             | `scaffold.py` (generate mock from OpenAPI), `seed_universal.py`  |

Integration discovery uses `BaseMock.__subclasses__()` — adding `mocks/foo.py` is sufficient to register it. No config changes needed.

## Code style and boundaries

- **No new core files.** Add to existing files unless a plan explicitly calls for a new one.
- **Auth/tier logic** lives only in `auth.py`.
- **Data access** only via `store.read()` / `store.write()`.
- **Dataclasses/enums** only in `models.py`.
- **Mock files** must subclass `BaseMock`, use `@route()`, stay under 50 LOC, and not import from `auth.py`, `store.py`, or `main.py`.
- All secrets come from `os.environ` via `python-dotenv`. Never hardcoded.
- Dropped PUT/POST/PATCH (free/anon tier): return 200/201 with `X-Verifiabl-Notice` header. Never return an error for a dropped write.
- Comments explain non-obvious intent only — no narration of what the code does.

## Adding a new integration or route

For a new integration (`mocks/{name}.py`) or a new route to an existing mock, read the full workflow first:

**`.cursor/skills/verifiabl-dev/ADD-INTEGRATION.md`**

(Same file on GitHub: `https://github.com/verifiabldev/verifiabl/blob/main/.cursor/skills/verifiabl-dev/ADD-INTEGRATION.md`)

That document covers: community signal research → OpenAPI spec → endpoint selection → implementation → fixture data → INTEGRATIONS.md row → PR checklist.

## What not to do

- Do not add tier checks, key lookups, or IP counting outside `auth.py`.
- Do not access store internals directly — always go through `store`.
- Do not hardcode sandbox credentials; they belong in `.env` only.
- Do not create `onboarding.py`, `usage.py`, `router.py`, or similar split files.
- Do not commit `.env`, `.venv/`, or `.venv-workers/`.
