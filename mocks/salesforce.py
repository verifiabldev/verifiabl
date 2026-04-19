# CHANGELOG: https://developer.salesforce.com/docs/atlas.en-us.api_rest.meta/api_rest/ (no RSS/atom feed as of 2026-03)
# SPEC:      https://developer.salesforce.com/docs/atlas.en-us.api_rest.meta/api_rest/
# SANDBOX:   https://developer.salesforce.com/signup
# SKILL:     —
# MCP:       https://developer.salesforce.com/docs/einstein/genai/guide/mcp.html
# LLMS:      —
from mocks.base import BaseMock, route
from models import MockResponse


class SalesforceMock(BaseMock):
    prefix = "/salesforce"
    spec_url = "https://developer.salesforce.com/docs/atlas.en-us.api_rest.meta/api_rest/"
    sandbox_base = "https://test.salesforce.com"

    @route("GET", "/services/data/v59.0/sobjects", writes=False)
    async def list_sobjects(self, request, **kw):
        return MockResponse(
            body={
                "sobjects": [
                    {"name": "Account", "label": "Account", "custom": False},
                    {"name": "Contact", "label": "Contact", "custom": False},
                    {"name": "Opportunity", "label": "Opportunity", "custom": False},
                ],
            }
        )

    @route("GET", "/services/data/v59.0/sobjects/{sobject}/describe", writes=False)
    async def describe_sobject(self, request, sobject="", **kw):
        return MockResponse(
            body={
                "name": sobject or "Account",
                "label": sobject or "Account",
                "fields": [
                    {"name": "Id", "type": "id", "nillable": False},
                    {"name": "Name", "type": "string", "length": 255},
                ],
            }
        )

    @route("GET", "/services/data/v59.0/sobjects/{sobject}/{id}", writes=False)
    async def get_record(self, request, sobject="", id="", **kw):
        return MockResponse(
            body={
                "attributes": {
                    "type": sobject or "Account",
                    "url": f"/services/data/v59.0/sobjects/{sobject or 'Account'}/{id}",
                },
                "Id": id or "001_mock_verifiabl",
                "Name": "Mock Account",
            }
        )

    @route("POST", "/services/data/v59.0/sobjects/{sobject}")
    async def create_record(self, request, sobject="", **kw):
        return MockResponse(status=201, body={"id": "001_mock_new", "success": True})

    @route("PATCH", "/services/data/v59.0/sobjects/{sobject}/{id}")
    async def update_record(self, request, sobject="", id="", **kw):
        return MockResponse(body={})

    @route("GET", "/services/data/v59.0/query", writes=False)
    async def query(self, request, **kw):
        return MockResponse(
            body={
                "totalSize": 2,
                "done": True,
                "records": [
                    {"attributes": {"type": "Account"}, "Id": "001_mock_001", "Name": "Acme"},
                    {"attributes": {"type": "Account"}, "Id": "001_mock_002", "Name": "Globex"},
                ],
            }
        )

    @route("GET", "/services/data/v59.0/limits", writes=False)
    async def limits(self, request, **kw):
        return MockResponse(
            body={
                "DailyApiRequests": {"Max": 15000, "Remaining": 14900},
                "DailyBulkApiRequests": {"Max": 10000, "Remaining": 10000},
            }
        )
