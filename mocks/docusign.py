# CHANGELOG: https://developers.docusign.com/  (release notes in community; no RSS/atom feed as of 2026-03)
# SKILL:     —
# MCP:       —
# LLMS:      —
from mocks.base import BaseMock, route
from models import MockResponse


class DocuSignMock(BaseMock):
    prefix = "/docusign"
    spec_url = "https://github.com/docusign/OpenAPI-Specifications"
    sandbox_base = "https://demo.docusign.net/restapi"

    @route("GET", "/v2.1/accounts/{account_id}")
    async def get_account(self, request, account_id="", **kw):
        return MockResponse(body={"accountId": account_id or "MOCK", "accountName": "Mock Account"})

    @route("POST", "/v2.1/accounts/{account_id}/envelopes")
    async def create_envelope(self, request, account_id="", **kw):
        return MockResponse(
            status=201,
            body={"envelopeId": "env_mock_001", "status": "sent", "uri": "/envelopes/env_mock_001"},
        )

    @route("GET", "/v2.1/accounts/{account_id}/envelopes/{envelope_id}")
    async def get_envelope(self, request, account_id="", envelope_id="", **kw):
        return MockResponse(body={"envelopeId": envelope_id, "status": "completed"})
