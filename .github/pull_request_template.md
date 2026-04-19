## New Integration Checklist

- [ ] `mocks/<name>.py` — subclasses `BaseMock`, uses `@route()` decorator, under 50 LOC
- [ ] `fixtures/<name>.json` — realistic seed data for local dev
- [ ] `INTEGRATIONS.md` — row added with status set to `live`
- [ ] Tested locally: `python scripts/seed_universal.py && uvicorn main:app --reload`
