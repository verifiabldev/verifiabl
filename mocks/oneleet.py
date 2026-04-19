# CHANGELOG: https://docs.oneleet.com/ (no RSS/atom feed as of 2026-03)
# SPEC:      https://docs.oneleet.com (no public OpenAPI — mock inferred from product)
# SANDBOX:   https://oneleet.com
# SKILL:     —
# MCP:       —
# LLMS:      —
# AUTH:      Bearer token in Authorization header
from mocks.base import BaseMock, route
from models import MockResponse


class OneleetMock(BaseMock):
    prefix = "/oneleet"
    spec_url = "https://docs.oneleet.com"
    sandbox_base = "https://api.oneleet.com"

    @route("GET", "/v1/organizations", writes=False)
    async def list_organizations(self, request, **kw):
        return MockResponse(
            body={
                "organizations": [
                    {"id": "org_mock_001", "name": "Acme Corp", "created_at": 1710400000},
                    {"id": "org_mock_002", "name": "Beta Inc", "created_at": 1710400100},
                ],
            }
        )

    @route("GET", "/v1/organizations/{id}", writes=False)
    async def get_organization(self, request, id="", **kw):
        return MockResponse(
            body={
                "id": id or "org_mock_001",
                "name": "Acme Corp",
                "created_at": 1710400000,
            }
        )

    @route("GET", "/v1/users", writes=False)
    async def list_users(self, request, **kw):
        return MockResponse(
            body={
                "users": [
                    {
                        "id": "user_mock_001",
                        "email": "alice@verifiabl.dev",
                        "first_name": "Alice",
                        "last_name": "Smith",
                        "mfa_enabled": True,
                    },
                    {
                        "id": "user_mock_002",
                        "email": "bob@verifiabl.dev",
                        "first_name": "Bob",
                        "last_name": "Jones",
                        "mfa_enabled": False,
                    },
                ],
            }
        )

    @route("GET", "/v1/users/{id}", writes=False)
    async def get_user(self, request, id="", **kw):
        return MockResponse(
            body={
                "id": id or "user_mock_001",
                "email": "alice@verifiabl.dev",
                "first_name": "Alice",
                "last_name": "Smith",
                "mfa_enabled": True,
            }
        )

    @route("GET", "/v1/vendors", writes=False)
    async def list_vendors(self, request, **kw):
        return MockResponse(
            body={
                "vendors": [
                    {"id": "vendor_mock_001", "name": "GitLab", "integration_id": "int_mock_001"},
                    {
                        "id": "vendor_mock_002",
                        "name": "Microsoft 365",
                        "integration_id": "int_mock_002",
                    },
                ],
            }
        )

    @route("GET", "/v1/vendors/{id}", writes=False)
    async def get_vendor(self, request, id="", **kw):
        return MockResponse(
            body={
                "id": id or "vendor_mock_001",
                "name": "GitLab",
                "integration_id": "int_mock_001",
            }
        )

    @route("GET", "/v1/integrations", writes=False)
    async def list_integrations(self, request, **kw):
        return MockResponse(
            body={
                "integrations": [
                    {
                        "id": "int_mock_001",
                        "vendor_id": "vendor_mock_001",
                        "type": "gitlab",
                        "status": "connected",
                    },
                    {
                        "id": "int_mock_002",
                        "vendor_id": "vendor_mock_002",
                        "type": "microsoft365",
                        "status": "connected",
                    },
                ],
            }
        )

    @route("GET", "/v1/integrations/{id}", writes=False)
    async def get_integration(self, request, id="", **kw):
        return MockResponse(
            body={
                "id": id or "int_mock_001",
                "vendor_id": "vendor_mock_001",
                "type": "gitlab",
                "status": "connected",
            }
        )

    @route("GET", "/v1/access-reviews", writes=False)
    async def list_access_reviews(self, request, **kw):
        return MockResponse(
            body={
                "access_reviews": [
                    {
                        "id": "ar_mock_001",
                        "name": "Q1 2025 vendor access",
                        "status": "in_progress",
                        "created_at": 1710400000,
                    },
                    {
                        "id": "ar_mock_002",
                        "name": "Q4 2024 vendor access",
                        "status": "completed",
                        "created_at": 1705000000,
                    },
                ],
            }
        )

    @route("GET", "/v1/access-reviews/{id}", writes=False)
    async def get_access_review(self, request, id="", **kw):
        return MockResponse(
            body={
                "id": id or "ar_mock_001",
                "name": "Q1 2025 vendor access",
                "status": "in_progress",
                "created_at": 1710400000,
            }
        )

    @route("POST", "/v1/access-reviews")
    async def create_access_review(self, request, **kw):
        return MockResponse(
            status=201,
            body={
                "id": "ar_mock_new",
                "name": "New access review",
                "status": "draft",
                "created_at": 1710400000,
            },
        )

    @route("PATCH", "/v1/access-reviews/{id}")
    async def update_access_review(self, request, id="", **kw):
        return MockResponse(
            body={
                "id": id or "ar_mock_001",
                "name": "Q1 2025 vendor access",
                "status": "in_progress",
            }
        )
