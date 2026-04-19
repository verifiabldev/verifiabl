---
name: verifiabl-add-integration
description: Research and implement a new mock integration for verifiabl.dev. Given a service name (e.g. "Stripe"), research real-world API usage, find the OpenAPI spec and changelog feed, plan the endpoint set from official sources, and produce a schema-faithful mock file. Use when asked to add a new integration, add a new mock, or expand an existing mock.
---

**Date:** Use the actual current date for "as of" changelog/feed notes and sample timestamps — LLMs often default to wrong dates unless reminded.

# Adding a New Mock Integration

Given a service name (e.g. "Stripe"), follow this exact workflow:

---

## Phase 1 — Research (always do this first)

The goal is to understand **which endpoints matter most to real developers**, not just which exist.

### 1a. Community signal (infer demand)

Search for real-world usage signals. Useful queries (substitute `{SERVICE}`):

- `site:reddit.com "{SERVICE} API" most common endpoints`
- `site:reddit.com "{SERVICE} API" frustrating slow broken`
- `"{SERVICE} API" rate limit workaround site:stackoverflow.com`
- `"{SERVICE} API" webhook error site:community.{service}.com`
- GitHub code search: `https://cs.github.com/?q=%22{service}.com%22+language%3APython` (or JS/Ruby/Go)

What to extract:

- Top 5-10 endpoints developers **actually call** in production (not just listed in docs)
- Known pain points: fields that are missing, status codes that surprise, pagination quirks
- Any fields that SDKs add/transform that the raw API doesn't expose

### 1b. Official sources (find the spec)

Check these in order, stopping when you find a machine-readable spec:

1. **OpenAPI / Swagger spec**
   - Check `https://api.{service}.com/openapi.json`
   - Check `https://api.{service}.com/v1/swagger.json`
   - Check GitHub: `https://github.com/{service}` — search repos for `openapi.yaml`, `swagger.json`, `api-spec`
   - Known public specs: Stripe → `github.com/stripe/openapi`, Slack → `api.slack.com/specs`, GitHub → `github.com/github/rest-api-description`

2. **Postman collection**
   - Check `https://www.postman.com/explore` — search `{SERVICE} API`
   - Many vendors publish official collections: `postman.com/{service}/`
   - Download the collection JSON. The `item[].request` array gives you method + path + example body.

3. **Official SDK source**
   - Find the Python or Node SDK on GitHub (e.g. `github.com/stripe/stripe-python`)
   - Read the `api_resources/` or `src/resources/` directory — filenames map directly to API resources
   - Look for `DEFAULT_BASE_URL`, `API_BASE`, or `base_url` constants → confirms `sandbox_base`
   - Read method definitions: `def create(cls, ...)`, `def retrieve(cls, ...)` → these are the routes

4. **CLI reverse engineering** (if vendor has one)
   - Run `{service} --help` and `{service} api --help` if installed
   - For Stripe CLI: `stripe fixtures` ships with canonical request/response pairs → gold standard for mock bodies

5. **Official documentation**
   - Read the API reference, not the quickstart
   - Focus on the resource index — what resources exist, what methods each supports
   - Note any `idempotency-key`, required headers, or envelope patterns (e.g. `{"data": [...]}` vs bare array)

6. **Changelog feed** — find it now, you will use it in Phase 3
   - Try: `https://docs.{service}.com/changelog/feed.atom`
   - Try: `https://{service}.com/changelog/rss`
   - Try: `https://{service}.com/feed.xml`
   - Google: `"{SERVICE}" changelog RSS atom feed`
   - Record the URL. If none exists, record the changelog page URL instead.

### 1c. Auth (real API only)

Research how the **real** API authenticates. Mocks never validate credentials — verifiabl resolves tier in `main.py` before the request reaches the mock. You need this so agents and docs know what the real API expects.

1. **OpenAPI**: In the spec, check `components.securitySchemes` and `security` on paths. Note the scheme name (e.g. `Bearer`, `ApiKeyAuth`) and where the key goes: `header` (name), `query`, or `cookie`.
2. **SDK**: Look for `api_key`, `auth`, or `Authorization` in client constructors and request builders.
3. **Docs**: "Authentication" or "Getting started" — header name (e.g. `Authorization: Bearer`, `X-API-Key`), query param, or basic auth.

Record in the mock file header so the integration is self-describing:

```python
# AUTH: Bearer token in Authorization header (per OpenAPI securitySchemes)
```

If the real API uses a custom header or query param, use that exact name. No auth logic goes in the mock; this is documentation only.

### 1d. Resolve conflicts between sources

Sources disagree. Priority order for **field names and shapes**:

1. Official OpenAPI spec (machine-generated, most accurate)
2. Official SDK source (maintained against real API)
3. Postman collection (often slightly stale)
4. Documentation prose (sometimes lags the actual API)
5. Reddit/Stack Overflow (can reflect older API versions)

---

## Phase 2 — Plan the endpoint set

### Selection criteria

Include an endpoint if it meets **any** of these:

- It appears in SDK quickstart examples
- It is called in >3 distinct GitHub repos found via code search
- It is listed in the "core resources" section of the official docs
- It is a prerequisite for other included endpoints (e.g. you must create a customer before a payment intent)

Skip an endpoint if:

- It is admin/management only (not called from application code)
- It is deprecated and the SDK no longer surfaces it
- It duplicates a covered endpoint (e.g. `GET /v1/customers` + `GET /v1/customers?email=x` — one route handles both)

### Target endpoint count

- Minimum: 6 endpoints (anything less fails to cover a real agent workflow)
- Sweet spot: 10-15 endpoints
- Maximum before splitting: 20 endpoints

If a service has 20+ important endpoints, split by resource into multiple mock files:
`mocks/{service}_billing.py`, `mocks/{service}_webhooks.py`, etc. Each file stays under 80 LOC. Explain the split in the implementation plan.

### Plan format

Write the plan as a table before writing any code:

| Method | Path          | Resource        | writes? | Why included                               |
| ------ | ------------- | --------------- | ------- | ------------------------------------------ |
| GET    | /v1/customers | list customers  | No      | Core resource, called in every integration |
| POST   | /v1/customers | create customer | Yes     | Prerequisite for charges                   |
| ...    |               |                 |         |                                            |

**`writes?`** is `False` for pure reads, `True` for state mutations. This maps directly to the `@route()` `writes` param.

---

## Phase 3 — Implement the mock file

### File header (required)

Every mock file MUST start with a comment block containing changelog info and auth. Below `# SANDBOX:` add optional SKILL, MCP, LLMS when the vendor provides them (otherwise use `—`):

```python
# CHANGELOG: https://docs.{service}.com/changelog/feed.atom
# SPEC:      https://github.com/{service}/openapi
# SANDBOX:   https://dashboard.{service}.com/test/
# SKILL:     https://... (company-promoted skill / how to use with AI) or —
# MCP:       https://... (MCP server endpoint or docs) or —
# LLMS:      https://.../llms.txt or —
# AUTH:      Bearer token in Authorization header (per OpenAPI securitySchemes)
```

If no feed URL was found, use the changelog page URL and note it. Use the exact auth mechanism from the real API (header name, Bearer vs API key, query param).

```python
# CHANGELOG: https://{service}.com/changelog  (no RSS/atom feed found as of 2026-03)
```

Use the current year-month in "as of" notes (see Date above).

### File structure

Follow `mocks/base.py` contract exactly:

```python
# CHANGELOG: <url>
# SPEC:      <url>
# SANDBOX:   <url>
# SKILL:     <url> or —
# MCP:       <url> or —
# LLMS:      <url> or —
from mocks.base import BaseMock, route
from models import MockResponse


class {Name}Mock(BaseMock):
    prefix = "/{name}"
    spec_url = "<openapi or sdk url>"
    sandbox_base = "https://api.{service}.com"

    @route("GET", "/v1/resource")
    async def list_resource(self, request, **kw):
        return MockResponse(body={...})

    @route("POST", "/v1/resource")
    async def create_resource(self, request, **kw):
        return MockResponse(status=201, body={...})

    @route("GET", "/v1/resource/{id}")
    async def get_resource(self, request, id="", **kw):
        return MockResponse(body={...})
```

### Response body rules

- Use **real field names** from the spec. Do not invent names.
- For IDs: use `{resource_type}_mock_{short_token}` pattern (e.g. `cus_mock_verifiabl`, `pi_mock_001`)
- For timestamps: use `1710400000` (a fixed Unix epoch, not `time.time()`)
- For amounts: use realistic values (e.g. `2000` = $20.00 for Stripe, not `1`)
- For enums: use the most common/happy-path value (e.g. Stripe status → `"requires_payment_method"`)
- For lists: return 2-3 items — enough to test pagination logic, not so many it floods logs
- For `object` envelope fields (Stripe): always include `"object": "{resource_name}"`
- For `data` envelope fields (HubSpot, Salesforce): wrap list in `{"results": [...]}` or `{"data": [...]}` per spec

### LOC budget exception rule

The ~50 LOC target is a guide, not a cap. You **may exceed it** when:

- The service has a non-trivial envelope pattern that requires a helper method (add the helper, explain why in a comment above it)
- The service returns deeply nested bodies and abbreviating them would make the mock useless for agent testing (an agent that calls `GET /v1/subscriptions/{id}` and gets back `{"id": "sub_mock"}` cannot test subscription cancellation flows)
- You are splitting a large integration and the split boundary naturally lands at 60-70 LOC per file

When you exceed 80 LOC, add a comment at the top of the class:

```python
# LOC EXCEPTION: <one sentence reason>
```

### The fixture file

Create `fixtures/{name}.json` alongside the mock. It seeds local dev and the nightly recorder.

Minimum shape:

```json
{
  "{resource}": [
    { "id": "{resource}_mock_001", ...all required fields... },
    { "id": "{resource}_mock_002", ...all required fields... }
  ]
}
```

Use the same field names and value conventions as the mock response bodies.

---

## Phase 4 — Validate before committing

1. **Cross-check method + path against the spec** — not the docs prose, the machine-readable spec
2. **Check the `writes` flag** — a route that returns existing data is `writes=False` even if the HTTP method is POST (Slack does this heavily)
3. **Verify `sandbox_base`** — confirm the URL in the SDK source, not from memory
4. **Verify `spec_url`** — must be a stable permalink, not a redirect
5. **Check `# AUTH:`** — matches the real API’s scheme (header/query name, Bearer vs API key); no auth logic in the mock
6. **Count LOC** — if >80, either trim or add the exception comment
7. **Check INTEGRATIONS.md** exists and add one row

---

## Reference: Known spec locations

| Service            | OpenAPI spec                                                                                             | Changelog feed                                                                      |
| ------------------ | -------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------- |
| Stripe             | `github.com/stripe/openapi`                                                                              | `stripe.com/docs/changelog/feed.atom`                                               |
| Slack              | `api.slack.com/specs`                                                                                    | `api.slack.com/changelog/feed`                                                      |
| GitHub             | `github.com/github/rest-api-description`                                                                 | `github.blog/changelog/feed`                                                        |
| Twilio             | `github.com/twilio/twilio-oai`                                                                           | `twilio.com/en-us/changelog/feed.xml`                                               |
| HubSpot            | `api.hubspot.com/api-catalog-public/v1/apis`                                                             | `developers.hubspot.com/changelog/rss.xml`                                          |
| Atlassian          | `dac-static.atlassian.com/cloud/jira/platform/swagger-v3.v3.json`                                        | `community.atlassian.com/t5/forums/feedpage/board-id/atlassian-cloud-platform-blog` |
| Adobe Acrobat Sign | `developer.adobe.com/document-services/docs/apis/` (REST ref, no OpenAPI)                                | developer.adobe.com/acrobat-sign/docs/overview/releasenotes/ (no RSS/atom feed)     |
| Zendesk            | `developer.zendesk.com/api-reference/ticketing/introduction/#openapi-spec`                               | `developer.zendesk.com/changelog/feed.xml`                                          |
| Okta               | `github.com/okta/okta-management-openapi-spec`                                                           | `developer.okta.com/feed.xml`                                                       |
| OpenAI             | `github.com/openai/openai-openapi`                                                                       | developers.openai.com/changelog (no RSS/atom feed)                                  |
| OpenRouter         | `openrouter.ai/openapi.json`                                                                             | openrouter.ai/announcements (no RSS/atom feed)                                      |
| Microsoft          | `learn.microsoft.com/en-us/graph/api/overview` (REST ref, no OpenAPI)                                    | `developer.microsoft.com/en-us/graph/changelog/rss`                                 |
| Mintlify           | `www.mintlify.com/docs/api/introduction` (OpenAPI snippets per endpoint in docs)                         | mintlify.com/docs/changelog (no RSS/atom feed)                                      |
| Modal              | `modal.com/docs/reference` (Python SDK; no public REST — mock derived from CLI/SDK)                      | modal.com/docs (no RSS/atom feed)                                                   |
| Google Workspace   | `admin.googleapis.com/$discovery/rest?version=directory_v1`                                              | `developers.google.com/feeds/admin-sdk-release-notes.xml`                           |
| Salesforce         | `developer.salesforce.com/docs/atlas.en-us.api_rest.meta/api_rest/` (no OpenAPI)                         | (no RSS/atom feed)                                                                  |
| Databricks         | `docs.databricks.com/api/workspace/introduction` (REST ref, no OpenAPI)                                  | `docs.databricks.com/en/release-notes/` (no RSS/atom feed)                          |
| ServiceNow         | `docs.servicenow.com/.../c_TableAPI.html` (Table API, no OpenAPI)                                        | developer.servicenow.com/blog (no RSS/atom)                                         |
| Workday            | `community.workday.com/.../productionapi/` (WSDL/REST docs, no OpenAPI)                                  | userguide.doc.workday.com API Changes by Release (no RSS)                           |
| SAP                | `github.com/SAP/openapi-specification` (SAP OData/S/4HANA via API Business Hub)                          | help.sap.com/docs (no RSS/atom feed)                                                |
| SAP SuccessFactors | SuccessFactors OData v2 API Reference (help.sap.com SuccessFactors Platform)                             | help.sap.com/docs (no RSS/atom feed)                                                |
| Oracle NetSuite    | `system.netsuite.com/help/.../REST_API_Browser/record/v1/` (OpenAPI 3.0 metadata)                        | docs.oracle.com/.../chapter_3798389663.html (no RSS/atom feed)                      |
| Oracle Fusion ERP  | `docs.oracle.com/.../financials/.../rest-endpoints.html` (REST ref, no OpenAPI)                          | (no RSS/atom feed)                                                                  |
| Oracle Fusion HCM  | `docs.oracle.com/.../human-resources/.../farws/index.html` (REST ref, no OpenAPI)                        | (no RSS/atom feed)                                                                  |
| SAP Concur         | `developer.concur.com/api-explorer` (Swagger, Expense Reports v4)                                        | `developer.concur.com/tools-support/release-notes/` (no RSS/atom feed)              |
| Snowflake          | `github.com/snowflakedb/snowflake-rest-api-specs` (REST + SQL API docs)                                  | data-docs.snowflake.com/foundations/changelog (no RSS/atom)                         |
| Statsig            | `api.statsig.com/openapi/20240601.json`                                                                  | statsig.com/updates (no RSS/atom feed as of 2026-03)                                |
| Cisco Meraki       | `github.com/meraki/openapi`                                                                              | meraki.io/whats-new/ (no RSS/atom feed)                                             |
| Cisco Webex        | `developer.webex.com/docs/rest-api-basics` (REST ref, no OpenAPI)                                        | developer.webex.com/docs/api/changelog (no RSS/atom feed)                           |
| Figma              | `github.com/figma/rest-api-spec`                                                                         | developers.figma.com/docs/rest-api/changelog/ (no RSS/atom feed)                    |
| Framer             | `www.framer.com/developers/server-api-reference` (Server API WebSocket/SDK; no public REST)              | www.framer.com/updates (no RSS/atom feed)                                           |
| Prisma Access      | `pan.dev/access/api/prisma-access-config/`                                                               | pan.dev/scm/docs/release-notes/changelog (no RSS/atom feed)                         |
| Jam.dev            | jam.dev/docs/debug-a-jam/mcp (REST-style mock inferred from MCP + webhooks; no public OpenAPI)           | jam.dev/docs (no RSS/atom feed as of 2026-03)                                       |
| Jamf Pro           | `developer.jamf.com/jamf-pro/reference/jamf-pro-api` (instance schema at /api/schema)                    | developer.jamf.com/jamf-pro/docs/ (no RSS/atom feed)                                |
| Zscaler (ZIA)      | `help.zscaler.com/legacy-apis/understanding-zia-api` (REST ref, no OpenAPI)                              | help.zscaler.com/legacy-apis (no RSS/atom feed)                                     |
| CrowdStrike Falcon | `developer.crowdstrike.com/docs/openapi` (Swagger per region, login required)                            | developer.crowdstrike.com/blog/ (no RSS/atom feed)                                  |
| GitLab             | `gitlab.com/gitlab-org/gitlab/-/blob/master/doc/api/openapi/openapi.yaml`                                | docs.gitlab.com/ee/update/ (no RSS/atom feed)                                       |
| Gumloop            | docs.gumloop.com/api-reference/openapi.yaml                                                              | docs.gumloop.com (no RSS/atom feed as of 2026-03)                                   |
| Gong               | help.gong.io/docs (API reference); OpenAPI per-instance at /ajax/settings/api/documentation/specs        | help.gong.io/docs/release-notes (no RSS/atom feed)                                  |
| Groq               | console.groq.com/docs/api-reference (OpenAI-compatible at api.groq.com/openai/v1)                        | console.groq.com/docs/changelog (no RSS/atom feed as of 2026-03)                    |
| Resend             | github.com/resend/resend-openapi                                                                         | resend.com/changelog (no RSS/atom feed)                                             |
| Rippling           | developer.rippling.com/documentation/base-api (REST ref, no OpenAPI)                                     | rippling.com/blog (no RSS/atom feed)                                                |
| Supabase           | api.supabase.com/api/v1-json (Management API); PostgREST per-project at &lt;ref&gt;.supabase.co/rest/v1/ | supabase.com/changelog (no RSS/atom feed)                                           |
| Cloudflare         | github.com/cloudflare/api-schemas                                                                        | developers.cloudflare.com/changelog/rss/index.xml                                   |
| Vercel             | vercel.com/docs/rest-api/reference (REST ref, no OpenAPI)                                                | vercel.com/changelog (no RSS/atom feed)                                             |
| Weaviate           | github.com/weaviate/weaviate (openapi-specs/schema.json)                                                 | weaviate.io/weaviate/release-notes (no RSS/atom feed)                               |
| PostHog            | posthog.com/docs/api/overview (OpenAPI at app.posthog.com/api/schema/ when logged in)                    | posthog.com/changelog (no RSS/atom feed as of 2026-03)                              |
| Claude (Anthropic) | docs.anthropic.com/en/api/overview (REST ref, no OpenAPI)                                                | docs.anthropic.com/en/release-notes/api (no RSS/atom feed)                          |
| Mistral            | docs.mistral.ai/openapi.yaml; github.com/mistralai/platform-docs-public                                  | docs.mistral.ai/changelog (no RSS/atom feed as of 2026-03)                          |
| Fly.io             | docs.machines.dev (Machines API OpenAPI 3.0)                                                             | fly.io/changelog.xml                                                                |
| n8n                | github.com/n8n-io/n8n-docs (docs/api/v1/openapi.yml)                                                     | github.com/n8n-io/n8n/releases.atom                                                 |
| Railway            | docs.railway.com/reference/public-api (GraphQL; schema at backboard.railway.com/graphql/v2)              | railway.app/changelog (no RSS/atom feed)                                            |
| Render             | api-docs.render.com/v1.0/openapi/render-public-api-1.json                                                | render.com/changelog (no RSS/atom feed)                                             |
| Cinder             | docs.cinder.co (access gated; mock inferred from Trust & Safety domain)                                  | cinder.co/blog-posts (no RSS/atom feed as of 2026-03)                               |
| Merge              | docs.merge.dev/get-started/unified-api/ (HRIS, ATS, etc.; OpenAPI per category via Postman)              | docs.merge.dev (no RSS/atom feed as of 2026-03)                                     |
| Pinecone           | github.com/pinecone-io/pinecone-api                                                                      | docs.pinecone.io/release-notes/ (no RSS/atom feed)                                  |
| Feedly             | developers.feedly.com/reference/introduction (REST ref, no OpenAPI)                                      | developers.feedly.com/changelog (no RSS/atom feed as of 2026-03)                    |
| Sim.ai             | docs.sim.ai/api-reference/getting-started (REST ref, no OpenAPI)                                         | sim.ai/changelog (no RSS/atom feed as of 2026-03)                                   |
| Tavily             | docs.tavily.com/documentation/api-reference/openapi.json (Search, Extract, Crawl, Map, Research, Usage)  | docs.tavily.com/changelog (no RSS/atom feed as of 2026-03)                          |
| Depthfirst         | depthfirst.com (no public OpenAPI — mock inferred from product description)                              | depthfirst.com/changelog (no RSS/atom feed as of 2026-03)                           |
| Hugging Face       | huggingface.co/.well-known/openapi.json (Hub API)                                                        | huggingface.co/changelog (no RSS/atom feed as of 2026-03)                           |
| You.com            | docs.you.com/openapi.json (multi-API; Search, Contents, Research, Images, Live News)                     | docs.you.com (no RSS/atom feed as of 2026-03)                                       |
| Vapi               | docs.vapi.ai/api-reference (OpenAPI 3.1.0 per endpoint; Calls, Assistants, Chats)                        | docs.vapi.ai/changelog (no RSS/atom feed as of 2026-03)                             |
| ElevenLabs         | elevenlabs.io/docs/api-reference/introduction; api.elevenlabs.io/openapi.json (spec may redirect)        | elevenlabs.io/docs/changelog (no RSS/atom feed as of 2026-03)                       |
| Fern               | buildwithfern.com/learn/docs/ai-features/ask-fern/api-reference/overview (OpenAPI snippets per endpoint) | buildwithfern.com/learn/docs/changelog (no RSS/atom feed)                           |
| AssemblyAI         | github.com/AssemblyAI/assemblyai-api-spec (openapi.yml)                                                  | assemblyai.com/changelog (no RSS/atom feed as of 2026-03)                           |
| Replit             | docs.replit.com (Extensions/GraphQL; replit.com/graphql; no public OpenAPI)                              | docs.replit.com/updates/ (no RSS/atom feed as of 2026-03)                           |
| Decagon            | docs.decagon.ai/api-reference (access gated; mock inferred from conversational AI platform)              | docs.decagon.ai (no RSS/atom feed as of 2026-03)                                    |
| Loops              | app.loops.so/openapi.json                                                                                | loops.so/docs/api-reference/changelog (no RSS/atom feed)                            |
| Bubble             | manual.bubble.io/core-resources/api/the-bubble-api/the-data-api/data-api-requests (Data API; Postman)    | manual.bubble.io/core-resources/application-settings/versions (no RSS/atom feed)    |
| Brave Search       | brave.com/search/api (REST ref, no OpenAPI)                                                              | api-dashboard.search.brave.com/documentation (no RSS/atom feed as of 2026-03)       |
| Ollama             | docs.ollama.com/api (OpenAPI snippets per endpoint; no single spec file)                                 | github.com/ollama/ollama/releases (no RSS/atom feed)                                |
| Oneleet            | docs.oneleet.com (no public OpenAPI — mock inferred from product)                                        | docs.oneleet.com (no RSS/atom feed as of 2026-03)                                   |
| Otter              | help.otter.ai (REST ref; no public OpenAPI — mock inferred)                                              | help.otter.ai (no RSS/atom feed as of 2026-03)                                      |
| Paddle             | github.com/PaddleHQ/paddle-openapi                                                                       | developer.paddle.com/changelog/overview (no RSS/atom feed as of 2026-03)            |
| Ahrefs             | ahrefs.com/api/documentation (REST ref, no OpenAPI)                                                      | ahrefs.com/api/docs/changelog (no RSS/atom feed as of 2026-03)                      |
| Polar              | polar.sh/docs/openapi.yaml                                                                               | polar.sh/docs/changelog/api.md (no RSS/atom feed as of 2026-03)                     |
| Coupler.io         | docs.coupler.io (no public OpenAPI — mock inferred from data integration product)                        | docs.coupler.io (no RSS/atom feed as of 2026-03)                                    |
| ChatPRD            | www.chatprd.ai/docs (no public OpenAPI — mock inferred from MCP document management)                     | www.chatprd.ai/docs (no RSS/atom feed as of 2026-03)                                |
| PhotoRoom          | image-api.photoroom.com/openapi                                                                          | docs.photoroom.com/getting-started/changelog (no RSS/atom feed as of 2026-03)       |
| Linear             | developers.linear.app/docs/graphql/working-with-the-graphql-api (GraphQL; mock is REST facade)           | developers.linear.app/changelog (no RSS/atom feed as of 2026-03)                    |
| Retell AI          | docs.retellai.com/api-references (OpenAPI snippets per endpoint; no single spec file)                    | www.retellai.com/changelog (no RSS/atom feed as of 2026-03)                         |
| Synthesia          | docs.synthesia.io/reference/introduction (OpenAPI 3.0.2 per endpoint in docs)                            | synthesia.noticeable.news/api.rss                                                   |

Add new entries here as integrations are added.
