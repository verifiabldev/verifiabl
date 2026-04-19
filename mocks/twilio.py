# CHANGELOG: https://www.twilio.com/en-us/changelog  (feed documented at /changelog/feed.xml; may be unstable as of 2026-03)
# SKILL:     —
# MCP:       https://github.com/twilio-labs/mcp
# LLMS:      https://www.twilio.com/docs/llms.txt
from mocks.base import BaseMock, route
from models import MockResponse


class TwilioMock(BaseMock):
    prefix = "/twilio"
    spec_url = "https://github.com/twilio/twilio-oai"
    sandbox_base = "https://api.twilio.com"

    @route("GET", "/2010-04-01/Accounts/{sid}")
    async def get_account(self, request, sid="", **kw):
        return MockResponse(body={"sid": sid or "AC_MOCK", "status": "active", "type": "Full"})

    @route("POST", "/2010-04-01/Accounts/{sid}/Messages.json")
    async def send_message(self, request, sid="", **kw):
        return MockResponse(
            status=201,
            body={
                "sid": "SM_MOCK",
                "status": "queued",
                "to": "+15551234567",
                "from": "+15559876543",
            },
        )

    @route("GET", "/2010-04-01/Accounts/{sid}/Messages.json")
    async def list_messages(self, request, sid="", **kw):
        return MockResponse(body={"messages": [{"sid": "SM_MOCK", "status": "delivered"}]})
