# CHANGELOG: https://feedback.instantly.ai/changelog  (no RSS/atom feed as of 2026-03)
# SPEC:      https://developer.instantly.ai/api-reference/openapi.json
# SANDBOX:   https://app.instantly.ai
# SKILL:     —
# MCP:       —
# LLMS:      —
# AUTH:      Bearer token in Authorization header (per docs)
from mocks.base import BaseMock, route
from models import MockResponse


def _campaign(id_="019cc043-e30c-7245-9123-8470ac01f534", name="Mock Campaign", status=1):
    return {
        "id": id_,
        "name": name,
        "status": status,
        "campaign_schedule": {"start_date": "2025-01-15", "end_date": None, "schedules": []},
        "timestamp_created": "2025-01-10T12:00:00Z",
        "timestamp_updated": "2025-01-12T14:00:00Z",
    }


def _lead(id_="019cc043-d74d-7eae-885a-00ddc8a51e91", contact="lead_mock@verifiabl.dev"):
    return {
        "id": id_,
        "contact": contact,
        "first_name": "Jane",
        "last_name": "Lead",
        "status": "FILTER_VAL_CONTACTED",
        "campaign_id": "019cc043-e30c-7245-9123-8470ac01f534",
    }


# LOC EXCEPTION: Campaign/lead schema and list envelope (items + next_starting_after) need helpers and 12 routes for campaigns, leads, lead-lists, accounts, workspace.
class InstantlyMock(BaseMock):
    prefix = "/instantly"
    spec_url = "https://developer.instantly.ai/api-reference/openapi.json"
    sandbox_base = "https://api.instantly.ai"

    @route("GET", "/api/v2/campaigns", writes=False)
    async def list_campaigns(self, request, **kw):
        return MockResponse(
            body={
                "items": [
                    _campaign("019cc043-e30c-7245-9123-8470ac01f534", "Outreach Q1"),
                    _campaign("019cc043-e30c-7245-9123-8470ac01f535", "Follow-up", 2),
                ],
                "next_starting_after": None,
            }
        )

    @route("POST", "/api/v2/campaigns")
    async def create_campaign(self, request, **kw):
        return MockResponse(
            status=201, body=_campaign("019cc043-e30c-7245-9123-8470ac01f536", "New Campaign", 0)
        )

    @route("GET", "/api/v2/campaigns/{id}", writes=False)
    async def get_campaign(self, request, id="", **kw):
        return MockResponse(body=_campaign(id or "019cc043-e30c-7245-9123-8470ac01f534"))

    @route("PATCH", "/api/v2/campaigns/{id}")
    async def patch_campaign(self, request, id="", **kw):
        return MockResponse(body=_campaign(id or "019cc043-e30c-7245-9123-8470ac01f534"))

    @route("POST", "/api/v2/campaigns/{id}/activate")
    async def activate_campaign(self, request, id="", **kw):
        return MockResponse(body=_campaign(id or "019cc043-e30c-7245-9123-8470ac01f534", status=1))

    @route("POST", "/api/v2/campaigns/{id}/stop")
    async def stop_campaign(self, request, id="", **kw):
        return MockResponse(body=_campaign(id or "019cc043-e30c-7245-9123-8470ac01f534", status=2))

    @route("POST", "/api/v2/leads/list", writes=False)
    async def list_leads(self, request, **kw):
        return MockResponse(
            body={
                "items": [
                    _lead(),
                    _lead("019cc043-d74d-7eae-885a-00ddc8a51e92", "lead_mock_2@verifiabl.dev"),
                ],
                "next_starting_after": None,
            }
        )

    @route("GET", "/api/v2/leads/{id}", writes=False)
    async def get_lead(self, request, id="", **kw):
        return MockResponse(body=_lead(id or "019cc043-d74d-7eae-885a-00ddc8a51e91"))

    @route("POST", "/api/v2/leads/add")
    async def add_leads_bulk(self, request, **kw):
        return MockResponse(
            body={
                "status": "success",
                "total_sent": 5,
                "leads_uploaded": 4,
                "in_blocklist": 0,
                "blocklist_used": None,
                "duplicated_leads": 0,
                "skipped_count": 0,
                "invalid_email_count": 1,
                "incomplete_count": 0,
                "duplicate_email_count": 0,
            }
        )

    @route("GET", "/api/v2/lead-lists", writes=False)
    async def list_lead_lists(self, request, **kw):
        return MockResponse(
            body={
                "items": [
                    {
                        "id": "019cc043-d74d-7eae-885a-00dcbf3b1304",
                        "name": "Mock List",
                        "timestamp_created": "2025-01-08T10:00:00Z",
                    },
                    {
                        "id": "019cc043-d74d-7eae-885a-00dcbf3b1305",
                        "name": "Second List",
                        "timestamp_created": "2025-01-09T11:00:00Z",
                    },
                ],
                "next_starting_after": None,
            }
        )

    @route("GET", "/api/v2/accounts", writes=False)
    async def list_accounts(self, request, **kw):
        return MockResponse(
            body={
                "items": [
                    {
                        "id": "019cc043-acc1-7000-9000-000000000001",
                        "email": "sender_mock@verifiabl.dev",
                        "status": "healthy",
                    },
                    {
                        "id": "019cc043-acc1-7000-9000-000000000002",
                        "email": "sender_mock_2@verifiabl.dev",
                        "status": "healthy",
                    },
                ],
                "next_starting_after": None,
            }
        )

    @route("GET", "/api/v2/workspace", writes=False)
    async def get_workspace(self, request, **kw):
        return MockResponse(
            body={
                "id": "019cc043-wksp-7000-9000-000000000001",
                "name": "Mock Workspace",
                "timestamp_created": "2025-01-01T00:00:00Z",
            }
        )
