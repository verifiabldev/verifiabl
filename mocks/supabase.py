# CHANGELOG: https://supabase.com/changelog  (no RSS/atom feed as of 2026-03)
# SPEC:      https://api.supabase.com/api/v1-json
# SANDBOX:   https://supabase.com/dashboard
# SKILL:     —
# MCP:       https://supabase.com/docs/guides/getting-started/mcp
# LLMS:      https://supabase.com/llms.txt
from mocks.base import BaseMock, route
from models import MockResponse


class SupabaseMock(BaseMock):
    prefix = "/supabase"
    spec_url = "https://api.supabase.com/api/v1-json"
    sandbox_base = "https://api.supabase.com"

    @route("GET", "/v1/projects", writes=False)
    async def list_projects(self, request, **kw):
        return MockResponse(
            body=[
                {
                    "id": "proj_mock_verifiabl",
                    "ref": "abcdefghijklmnopqrst",
                    "organization_id": "org_mock_001",
                    "organization_slug": "mock_org",
                    "name": "Mock Project",
                    "region": "us-east-1",
                    "created_at": "2023-03-29T16:32:59Z",
                    "status": "ACTIVE_HEALTHY",
                    "database": {
                        "host": "db.abc.supabase.co",
                        "version": "15",
                        "postgres_engine": "15",
                        "release_channel": "stable",
                    },
                },
                {
                    "id": "proj_mock_002",
                    "ref": "pqrstuvwxyzabcdefghij",
                    "organization_id": "org_mock_001",
                    "organization_slug": "mock_org",
                    "name": "Second Project",
                    "region": "us-west-1",
                    "created_at": "2024-01-15T10:00:00Z",
                    "status": "ACTIVE_HEALTHY",
                    "database": {
                        "host": "db.pqr.supabase.co",
                        "version": "15",
                        "postgres_engine": "15",
                        "release_channel": "stable",
                    },
                },
            ]
        )

    @route("GET", "/v1/projects/{ref}", writes=False)
    async def get_project(self, request, ref="", **kw):
        return MockResponse(
            body={
                "id": "proj_mock_verifiabl",
                "ref": ref or "abcdefghijklmnopqrst",
                "organization_id": "org_mock_001",
                "organization_slug": "mock_org",
                "name": "Mock Project",
                "region": "us-east-1",
                "created_at": "2023-03-29T16:32:59Z",
                "status": "ACTIVE_HEALTHY",
                "database": {
                    "host": "db.abc.supabase.co",
                    "version": "15",
                    "postgres_engine": "15",
                    "release_channel": "stable",
                },
            }
        )

    @route("POST", "/v1/projects")
    async def create_project(self, request, **kw):
        return MockResponse(
            status=201,
            body={
                "id": "proj_mock_new",
                "ref": "newrefabcdefghijklmnop",
                "organization_id": "org_mock_001",
                "organization_slug": "mock_org",
                "name": "New Project",
                "region": "us-east-1",
                "created_at": "2026-03-14T12:00:00Z",
                "status": "INACTIVE",
            },
        )

    @route("PATCH", "/v1/projects/{ref}")
    async def update_project(self, request, ref="", **kw):
        return MockResponse(
            body={
                "id": "proj_mock_verifiabl",
                "ref": ref or "abcdefghijklmnopqrst",
                "organization_id": "org_mock_001",
                "organization_slug": "mock_org",
                "name": "Updated Project",
                "region": "us-east-1",
                "created_at": "2023-03-29T16:32:59Z",
                "status": "ACTIVE_HEALTHY",
                "database": {
                    "host": "db.abc.supabase.co",
                    "version": "15",
                    "postgres_engine": "15",
                    "release_channel": "stable",
                },
            }
        )

    @route("GET", "/v1/organizations", writes=False)
    async def list_organizations(self, request, **kw):
        return MockResponse(
            body=[
                {"id": "org_mock_001", "slug": "mock_org", "name": "Mock Organization"},
                {"id": "org_mock_002", "slug": "other_org", "name": "Other Org"},
            ]
        )

    @route("GET", "/v1/organizations/{slug}", writes=False)
    async def get_organization(self, request, slug="", **kw):
        return MockResponse(
            body={
                "id": "org_mock_001",
                "name": slug or "mock_org",
                "plan": "free",
                "opt_in_tags": [],
                "allowed_release_channels": ["stable"],
            }
        )

    @route("GET", "/v1/organizations/{slug}/projects", writes=False)
    async def list_org_projects(self, request, slug="", **kw):
        return MockResponse(
            body=[
                {
                    "id": "proj_mock_verifiabl",
                    "ref": "abcdefghijklmnopqrst",
                    "organization_id": "org_mock_001",
                    "name": "Mock Project",
                    "region": "us-east-1",
                    "created_at": "2023-03-29T16:32:59Z",
                    "status": "ACTIVE_HEALTHY",
                },
            ]
        )

    @route("GET", "/v1/projects/available-regions", writes=False)
    async def available_regions(self, request, **kw):
        return MockResponse(
            body=[
                {"region": "us-east-1", "name": "East US (N. Virginia)"},
                {"region": "us-west-1", "name": "West US (N. California)"},
                {"region": "eu-west-1", "name": "Europe (Ireland)"},
            ]
        )
