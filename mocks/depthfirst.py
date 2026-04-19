# CHANGELOG: https://depthfirst.com/changelog  (no RSS/atom feed as of 2026-03)
# SPEC:      https://depthfirst.com (no public OpenAPI — mock inferred from product description)
# SANDBOX:   https://depthfirst.com/book-a-demo
# SKILL:     —
# MCP:       —
# LLMS:      —
from mocks.base import BaseMock, route
from models import MockResponse


class DepthfirstMock(BaseMock):
    prefix = "/depthfirst"
    spec_url = "https://depthfirst.com"
    sandbox_base = "https://api.depthfirst.com"

    @route("GET", "/v1/projects", writes=False)
    async def list_projects(self, request, **kw):
        return MockResponse(
            body={
                "projects": [
                    {
                        "id": "proj_mock_001",
                        "name": "acme-api",
                        "provider": "github",
                        "repo_url": "https://github.com/acme/acme-api",
                        "created_at": 1710400000,
                    },
                    {
                        "id": "proj_mock_002",
                        "name": "acme-web",
                        "provider": "gitlab",
                        "repo_url": "https://gitlab.com/acme/acme-web",
                        "created_at": 1710400100,
                    },
                ],
            }
        )

    @route("GET", "/v1/projects/{id}", writes=False)
    async def get_project(self, request, id="", **kw):
        return MockResponse(
            body={
                "id": id or "proj_mock_001",
                "name": "acme-api",
                "provider": "github",
                "repo_url": "https://github.com/acme/acme-api",
                "created_at": 1710400000,
                "last_scan_at": 1710486400,
            }
        )

    @route("GET", "/v1/scans", writes=False)
    async def list_scans(self, request, **kw):
        return MockResponse(
            body={
                "scans": [
                    {
                        "id": "scan_mock_001",
                        "project_id": "proj_mock_001",
                        "status": "completed",
                        "started_at": 1710400000,
                        "completed_at": 1710403600,
                    },
                    {
                        "id": "scan_mock_002",
                        "project_id": "proj_mock_001",
                        "status": "running",
                        "started_at": 1710486400,
                        "completed_at": None,
                    },
                ],
            }
        )

    @route("GET", "/v1/scans/{id}", writes=False)
    async def get_scan(self, request, id="", **kw):
        return MockResponse(
            body={
                "id": id or "scan_mock_001",
                "project_id": "proj_mock_001",
                "status": "completed",
                "started_at": 1710400000,
                "completed_at": 1710403600,
                "findings_count": 3,
            }
        )

    @route("POST", "/v1/scans")
    async def create_scan(self, request, **kw):
        return MockResponse(
            status=201,
            body={
                "id": "scan_mock_new",
                "project_id": "proj_mock_001",
                "status": "queued",
                "started_at": None,
                "completed_at": None,
            },
        )

    @route("GET", "/v1/findings", writes=False)
    async def list_findings(self, request, **kw):
        return MockResponse(
            body={
                "findings": [
                    {
                        "id": "find_mock_001",
                        "scan_id": "scan_mock_001",
                        "severity": "high",
                        "title": "SQL injection in login",
                        "state": "open",
                        "created_at": 1710403600,
                    },
                    {
                        "id": "find_mock_002",
                        "scan_id": "scan_mock_001",
                        "severity": "medium",
                        "title": "Hardcoded secret in config",
                        "state": "open",
                        "created_at": 1710403601,
                    },
                ],
            }
        )

    @route("GET", "/v1/findings/{id}", writes=False)
    async def get_finding(self, request, id="", **kw):
        return MockResponse(
            body={
                "id": id or "find_mock_001",
                "scan_id": "scan_mock_001",
                "severity": "high",
                "title": "SQL injection in login",
                "state": "open",
                "created_at": 1710403600,
                "file_path": "src/auth/login.py",
                "line": 42,
                "remediation": "Use parameterized queries.",
            }
        )

    @route("POST", "/v1/findings/{id}/feedback")
    async def submit_feedback(self, request, id="", **kw):
        return MockResponse(body={"id": id or "find_mock_001", "feedback_received": True})
