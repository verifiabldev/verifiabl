# CHANGELOG: https://developers.hubspot.com/changelog/tag/api?format=rss
# SKILL:     —
# MCP:       https://developers.hubspot.com/mcp
# LLMS:      —
from mocks.base import BaseMock, route
from models import MockResponse


class HubSpotMock(BaseMock):
    prefix = "/hubspot"
    spec_url = "https://github.com/HubSpot/HubSpot-public-api-spec-collection"
    sandbox_base = "https://api.hubapi.com"

    @route("GET", "/crm/v3/objects/contacts")
    async def list_contacts(self, request, **kw):
        return MockResponse(
            body={
                "results": [
                    {
                        "id": "1",
                        "properties": {
                            "email": "test@verifiabl.dev",
                            "firstname": "Mock",
                            "lastname": "User",
                        },
                    },
                ],
                "paging": {"next": None},
            }
        )

    @route("POST", "/crm/v3/objects/contacts")
    async def create_contact(self, request, **kw):
        return MockResponse(
            status=201,
            body={
                "id": "101",
                "properties": {
                    "email": "new@verifiabl.dev",
                    "firstname": "New",
                    "lastname": "Contact",
                },
            },
        )

    @route("GET", "/crm/v3/objects/deals")
    async def list_deals(self, request, **kw):
        return MockResponse(
            body={
                "results": [
                    {
                        "id": "1",
                        "properties": {
                            "dealname": "Mock Deal",
                            "amount": "10000",
                            "dealstage": "closedwon",
                        },
                    },
                ],
                "paging": {"next": None},
            }
        )

    @route("POST", "/crm/v3/objects/deals")
    async def create_deal(self, request, **kw):
        return MockResponse(
            status=201,
            body={
                "id": "201",
                "properties": {
                    "dealname": "New Deal",
                    "amount": "5000",
                    "dealstage": "appointmentscheduled",
                },
            },
        )
