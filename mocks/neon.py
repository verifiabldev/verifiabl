# CHANGELOG: https://neon.com/docs/changelog/rss.xml
# SPEC:      https://neon.com/api_spec/release/v2.json
# SANDBOX:   https://console.neon.tech
# SKILL:     —
# MCP:       https://mcp.neon.tech/mcp
# LLMS:      —
# AUTH:      Bearer token in Authorization header (per OpenAPI BearerAuth)
from mocks.base import BaseMock, route
from models import MockResponse


# Phase 2 endpoint plan (OpenAPI v2):
# | Method | Path                                              | Resource        | writes? | Why included                    |
# | GET    | /projects                                         | list projects   | No      | Core resource, SDK quickstart   |
# | POST   | /projects                                         | create project  | Yes     | Prerequisite for branches       |
# | GET    | /projects/{project_id}                            | get project     | No      | Single project lookup           |
# | GET    | /projects/{project_id}/branches                    | list branches   | No      | Branching core                  |
# | POST   | /projects/{project_id}/branches                   | create branch   | Yes     | CI/CD, preview branches        |
# | GET    | /projects/{project_id}/branches/{branch_id}        | get branch      | No      | Branch status                   |
# | GET    | /projects/{project_id}/branches/.../databases     | list databases  | No      | Database listing                |
# | POST   | /projects/{project_id}/branches/.../databases      | create database | Yes     | Create DB on branch             |
# | GET    | /projects/.../databases/{database_name}            | get database    | No      | Single DB lookup                |
# | GET    | /projects/{project_id}/endpoints                   | list endpoints  | No      | Connection endpoints            |
# | GET    | /regions                                           | list regions    | No      | Available regions               |
# LOC EXCEPTION: 11 schema-faithful project/branch/database/endpoint/region endpoints per OpenAPI v2.
class NeonMock(BaseMock):
    prefix = "/neon"
    spec_url = "https://neon.com/api_spec/release/v2.json"
    sandbox_base = "https://console.neon.tech/api/v2"

    @route("GET", "/projects", writes=False)
    async def list_projects(self, request, **kw):
        return MockResponse(
            body={
                "projects": [
                    {
                        "id": "proj_mock_verifiabl",
                        "platform_id": "aws",
                        "region_id": "aws-us-east-2",
                        "name": "Mock Project",
                        "provisioner": "k8s-pod",
                        "pg_version": 15,
                        "created_at": "2023-03-29T16:32:59Z",
                        "updated_at": "2023-03-29T16:32:59Z",
                        "proxy_host": "us-east-2.aws.neon.tech",
                        "cpu_used_sec": 0,
                        "branch_logical_size_limit": 0,
                        "owner_id": "owner_mock_001",
                        "creation_source": "console",
                        "store_passwords": True,
                    },
                    {
                        "id": "proj_mock_002",
                        "platform_id": "aws",
                        "region_id": "aws-us-west-2",
                        "name": "Second Project",
                        "provisioner": "k8s-pod",
                        "pg_version": 16,
                        "created_at": "2024-01-15T10:00:00Z",
                        "updated_at": "2024-01-15T10:00:00Z",
                        "proxy_host": "us-west-2.aws.neon.tech",
                        "cpu_used_sec": 0,
                        "branch_logical_size_limit": 0,
                        "owner_id": "owner_mock_001",
                        "creation_source": "console",
                        "store_passwords": True,
                    },
                ],
                "pagination": {"cursor": "eyJjcmVhdGVk", "limit": 10},
            }
        )

    @route("POST", "/projects")
    async def create_project(self, request, **kw):
        return MockResponse(
            status=201,
            body={
                "project": {
                    "id": "proj_mock_new",
                    "platform_id": "aws",
                    "region_id": "aws-us-east-2",
                    "name": "New Project",
                    "provisioner": "k8s-pod",
                    "pg_version": 15,
                    "created_at": "2026-03-14T12:00:00Z",
                    "updated_at": "2026-03-14T12:00:00Z",
                    "proxy_host": "us-east-2.aws.neon.tech",
                    "cpu_used_sec": 0,
                    "branch_logical_size_limit": 0,
                    "owner_id": "owner_mock_001",
                    "creation_source": "api",
                    "store_passwords": True,
                },
            },
        )

    @route("GET", "/projects/{project_id}", writes=False)
    async def get_project(self, request, project_id="", **kw):
        pid = project_id or "proj_mock_verifiabl"
        return MockResponse(
            body={
                "project": {
                    "id": pid,
                    "platform_id": "aws",
                    "region_id": "aws-us-east-2",
                    "name": "Mock Project",
                    "provisioner": "k8s-pod",
                    "pg_version": 15,
                    "created_at": "2023-03-29T16:32:59Z",
                    "updated_at": "2023-03-29T16:32:59Z",
                    "proxy_host": "us-east-2.aws.neon.tech",
                    "branch_logical_size_limit": 0,
                    "cpu_used_sec": 0,
                    "owner_id": "owner_mock_001",
                    "creation_source": "console",
                    "store_passwords": True,
                },
            }
        )

    @route("GET", "/projects/{project_id}/branches", writes=False)
    async def list_branches(self, request, project_id="", **kw):
        return MockResponse(
            body={
                "branches": [
                    {
                        "id": "br_mock_main",
                        "project_id": project_id or "proj_mock_verifiabl",
                        "name": "main",
                        "current_state": "ready",
                        "created_at": "2023-03-29T16:32:59Z",
                        "updated_at": "2023-03-29T16:32:59Z",
                        "default": True,
                        "protected": False,
                    },
                    {
                        "id": "br_mock_dev",
                        "project_id": project_id or "proj_mock_verifiabl",
                        "parent_id": "br_mock_main",
                        "name": "dev",
                        "current_state": "ready",
                        "created_at": "2024-01-15T10:00:00Z",
                        "updated_at": "2024-01-15T10:00:00Z",
                        "default": False,
                        "protected": False,
                    },
                ],
                "pagination": {"cursor": "eyJjcmVhdGVk", "limit": 10},
            }
        )

    @route("POST", "/projects/{project_id}/branches")
    async def create_branch(self, request, project_id="", **kw):
        return MockResponse(
            status=201,
            body={
                "branch": {
                    "id": "br_mock_new",
                    "project_id": project_id or "proj_mock_verifiabl",
                    "parent_id": "br_mock_main",
                    "name": "staging",
                    "current_state": "init",
                    "created_at": "2026-03-14T12:00:00Z",
                    "updated_at": "2026-03-14T12:00:00Z",
                    "default": False,
                    "protected": False,
                },
                "operations": [
                    {
                        "id": "op_mock_001",
                        "project_id": project_id or "proj_mock_verifiabl",
                        "branch_id": "br_mock_new",
                        "action": "create_timeline",
                        "status": "running",
                        "failures_count": 0,
                        "created_at": "2026-03-14T12:00:00Z",
                        "updated_at": "2026-03-14T12:00:00Z",
                    }
                ],
            },
        )

    @route("GET", "/projects/{project_id}/branches/{branch_id}", writes=False)
    async def get_branch(self, request, project_id="", branch_id="", **kw):
        return MockResponse(
            body={
                "branch": {
                    "id": branch_id or "br_mock_main",
                    "project_id": project_id or "proj_mock_verifiabl",
                    "name": "main",
                    "current_state": "ready",
                    "created_at": "2023-03-29T16:32:59Z",
                    "updated_at": "2023-03-29T16:32:59Z",
                    "default": True,
                    "protected": False,
                },
            }
        )

    @route("GET", "/projects/{project_id}/branches/{branch_id}/databases", writes=False)
    async def list_databases(self, request, project_id="", branch_id="", **kw):
        return MockResponse(
            body={
                "databases": [
                    {
                        "id": 834686,
                        "branch_id": branch_id or "br_mock_main",
                        "name": "neondb",
                        "owner_name": "neon_superuser",
                        "created_at": "2023-03-29T16:32:59Z",
                        "updated_at": "2023-03-29T16:32:59Z",
                    },
                    {
                        "id": 834687,
                        "branch_id": branch_id or "br_mock_main",
                        "name": "mydb",
                        "owner_name": "neon_superuser",
                        "created_at": "2024-01-15T10:00:00Z",
                        "updated_at": "2024-01-15T10:00:00Z",
                    },
                ],
            }
        )

    @route("POST", "/projects/{project_id}/branches/{branch_id}/databases")
    async def create_database(self, request, project_id="", branch_id="", **kw):
        return MockResponse(
            status=201,
            body={
                "database": {
                    "id": 876692,
                    "branch_id": branch_id or "br_mock_main",
                    "name": "newdb",
                    "owner_name": "neon_superuser",
                    "created_at": "2026-03-14T12:00:00Z",
                    "updated_at": "2026-03-14T12:00:00Z",
                },
                "operations": [
                    {
                        "id": "op_mock_002",
                        "project_id": project_id or "proj_mock_verifiabl",
                        "branch_id": branch_id or "br_mock_main",
                        "action": "apply_config",
                        "status": "running",
                        "failures_count": 0,
                        "created_at": "2026-03-14T12:00:00Z",
                        "updated_at": "2026-03-14T12:00:00Z",
                    }
                ],
            },
        )

    @route(
        "GET", "/projects/{project_id}/branches/{branch_id}/databases/{database_name}", writes=False
    )
    async def get_database(self, request, project_id="", branch_id="", database_name="", **kw):
        return MockResponse(
            body={
                "database": {
                    "id": 834686,
                    "branch_id": branch_id or "br_mock_main",
                    "name": database_name or "neondb",
                    "owner_name": "neon_superuser",
                    "created_at": "2023-03-29T16:32:59Z",
                    "updated_at": "2023-03-29T16:32:59Z",
                },
            }
        )

    @route("GET", "/projects/{project_id}/endpoints", writes=False)
    async def list_endpoints(self, request, project_id="", **kw):
        return MockResponse(
            body={
                "endpoints": [
                    {
                        "id": "ep_mock_001",
                        "project_id": project_id or "proj_mock_verifiabl",
                        "branch_id": "br_mock_main",
                        "host": "ep_mock_001.us-east-2.aws.neon.tech",
                        "region_id": "aws-us-east-2",
                        "type": "read_write",
                        "current_state": "idle",
                        "created_at": "2023-03-29T16:32:59Z",
                        "updated_at": "2023-03-29T16:32:59Z",
                        "proxy_host": "us-east-2.aws.neon.tech",
                        "pooler_enabled": False,
                        "settings": {"pg_settings": {}},
                    },
                ],
            }
        )

    @route("GET", "/regions", writes=False)
    async def list_regions(self, request, **kw):
        return MockResponse(
            body={
                "regions": [
                    {"slug": "aws-us-east-2", "name": "US East (Ohio)"},
                    {"slug": "aws-us-west-2", "name": "US West (Oregon)"},
                    {"slug": "eu-central-1", "name": "EU (Frankfurt)"},
                ],
            }
        )
