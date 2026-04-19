# CHANGELOG: https://pan.dev/scm/docs/release-notes/changelog  (no RSS/atom feed as of 2026-03)
# SPEC:      https://pan.dev/access/api/prisma-access-config/
# SANDBOX:   https://api.sase.paloaltonetworks.com (SASE auth / TSG)
# SKILL:     —
# MCP:       —
# LLMS:      —
from mocks.base import BaseMock, route
from models import MockResponse

_JOB = {
    "id": "job_mock_verifiabl",
    "status": "SUCCESS",
    "created_at": 1710400000,
    "updated_at": 1710400100,
}
_RUNNING = {"version": "running_mock_001", "folders": [{"folder": "Shared", "config": {}}]}
_CONFIG = {"version": "cfg_mock_001", "created_at": 1710400000, "data": {}}


class PrismaAccessMock(BaseMock):
    prefix = "/prisma_access"
    spec_url = "https://pan.dev/access/api/prisma-access-config/"
    sandbox_base = "https://api.sase.paloaltonetworks.com"

    @route("GET", "/sse/config/v1/jobs", writes=False)
    async def list_jobs(self, request, **kw):
        return MockResponse(
            body={"data": [_JOB, {**_JOB, "id": "job_mock_002", "status": "PENDING"}]}
        )

    @route("GET", "/sse/config/v1/jobs/{id}", writes=False)
    async def get_job(self, request, id="", **kw):
        return MockResponse(body={**_JOB, "id": id or _JOB["id"]})

    @route("GET", "/sse/config/v1/config-versions/running", writes=False)
    async def get_running_config(self, request, **kw):
        return MockResponse(body=_RUNNING)

    @route("GET", "/sse/config/v1/config-versions/{version}", writes=False)
    async def get_config_version(self, request, version="", **kw):
        return MockResponse(body={**_CONFIG, "version": version or _CONFIG["version"]})

    @route("POST", "/sse/config/v1/config-versions/candidate:push")
    async def push_candidate(self, request, **kw):
        return MockResponse(status=201, body={"data": {"id": "job_mock_new", "status": "PENDING"}})

    @route("POST", "/sse/config/v1/config-versions:load")
    async def load_config(self, request, **kw):
        return MockResponse(body={"data": {**_CONFIG, "version": "candidate_mock"}})
