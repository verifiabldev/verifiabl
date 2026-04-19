# verifiabl.dev

**Your AI agent says it's done. Now prove it.**

verifiabl.dev is a mock API server for AI coding agents. **The public endpoint is live at [https://verifiabl.dev](https://verifiabl.dev);** run locally for development (see Local Development below). Can't get a Gong sandbox? Workday credentials locked behind a client contract? SAP SuccessFactors Try Out down again? Point any HTTP client at `verifiabl.dev/{integration}` and get schema-faithful responses instantly — no sign-up, no sales call, no contract.

The key insight: unit tests are self-referential. An AI agent writes them and passes them — that proves nothing. verifiabl.dev is an independent endpoint the agent doesn't control. When the agent's integration hits it and gets back real schema responses, that's actual proof.

> _"Verification loops are the unlock."_ — [Addy Osmani](https://addyosmani.com/blog/coding-agents-manager/), [Your AI coding agents need a manager](https://addyosmani.com/blog/coding-agents-manager/)

Mocks are generated from real OpenAPI specs. Some integrations are also cross-checked against live sandboxes using verifiabl's own credentials, while broader automated validation is still being hardened for production.

## Quick Start

No sign-up required for the first 60 requests/hour.

```bash
curl -sS https://verifiabl.dev/stripe/v1/balance | jq
```

Works with any HTTP client — curl, CLIs, language libraries, or direct requests: Gong, Workday, Salesforce, HubSpot, Slack, and 100+ more.

## Why Not Just Write a Unit Test?

Unit tests that mock the API are written by the same agent that wrote the integration. They prove the agent's code calls the right methods — not that it calls the right API. verifiabl.dev closes that loop: swap the base URL, run the agent's code against a real schema endpoint, get an independent result.

This matters especially for enterprise APIs that have no public sandbox:

- **Gong** — no developer sandbox; requires a contract
- **Workday** — credentials only available via client org
- **Salesforce** — sandbox tied to a paid org
- **Rippling / Coupa / Oracle HCM / Concur** — all behind enterprise plans or partner credentials

## How It Works

1. **Base URL swap** — any HTTP client works out of the box
2. **Zero credentials** — verifiabl ignores auth headers; agents need nothing to start
3. **Schema-faithful** — responses match the real API's OpenAPI spec, not invented shapes
4. **Nightly validation** — verifiabl runs real sandbox calls on its own accounts to keep mocks honest

## Beta Scope

|            | Anonymous         | Free key                | Paid / stateful writes |
| ---------- | ----------------- | ----------------------- | ---------------------- |
| Rate limit | 60/hr per IP      | 1,000/hr                | Not in beta yet        |
| GET        | Mock data         | Mock data               | Not in beta yet        |
| Writes     | Dropped (200/201) | Dropped + notice header | Not in beta yet        |
| Usage      | —                 | Usage dashboard         | Not in beta yet        |

**Free-tier writes are silently dropped.** The response looks like it worked (valid 200/201), but the data is not persisted. A `X-Verifiabl-Notice` header indicates this. Stateful writes are planned after the beta launch.

## Local Development

```bash
uv sync
cp .env.example .env
uv run python scripts/seed_universal.py
uv run uvicorn main:app --reload
```

No real sandbox credentials needed — `seed_universal.py` loads bundled fixture data.

## Deploy to Cloudflare Workers

The Workers Python runtime can't `pip install` at request time, so it loads dependencies from a vendored `python_modules/` directory at deploy time. That directory is gitignored (it's a build artifact); rebuild it from `pyproject.toml` before each deploy:

```bash
uv pip install --target python_modules -r <(uv pip compile pyproject.toml)
npx wrangler deploy
```

Update `wrangler.toml` (`name`, `[[d1_databases]]`, `[[kv_namespaces]]`, `[[routes]]`) with your own resource IDs and route before the first deploy.

## Adding an Integration

See [CONTRIBUTING.md](CONTRIBUTING.md) for the 4-step process.

## Trademarks

All product names, logos, and company names are trademarks of their respective owners. verifiabl.dev is not affiliated with or endorsed by any listed company.

## License

MIT
