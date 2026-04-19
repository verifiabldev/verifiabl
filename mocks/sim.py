# CHANGELOG: https://www.sim.ai/changelog  (no RSS/atom feed as of 2026-03)
# SPEC:      https://docs.sim.ai/api-reference/getting-started
# SANDBOX:   https://www.sim.ai
# SKILL:     —
# MCP:       —
# LLMS:      —
from mocks.base import BaseMock, route
from models import MockResponse

_limits = {
    "workflowExecutionRateLimit": {
        "sync": {
            "requestsPerMinute": 60,
            "maxBurst": 10,
            "remaining": 59,
            "resetAt": "2025-06-20T14:16:00Z",
        },
        "async": {
            "requestsPerMinute": 30,
            "maxBurst": 5,
            "remaining": 30,
            "resetAt": "2025-06-20T14:16:00Z",
        },
    },
    "usage": {"currentPeriodCost": 1.25, "limit": 50, "plan": "pro", "isExceeded": False},
}


class SimMock(BaseMock):
    prefix = "/sim"
    spec_url = "https://docs.sim.ai/api-reference/getting-started"
    sandbox_base = "https://www.sim.ai"

    @route("GET", "/api/v1/workflows", writes=False)
    async def list_workflows(self, request, **kw):
        return MockResponse(
            body={
                "data": [
                    {
                        "id": "wf_mock_verifiabl_1",
                        "name": "Support Agent",
                        "description": "Routes tickets",
                        "color": "#33c482",
                        "folderId": "folder_mock_1",
                        "workspaceId": "ws_mock_1",
                        "isDeployed": True,
                        "deployedAt": "2025-06-15T10:30:00Z",
                        "runCount": 142,
                        "lastRunAt": "2025-06-20T14:15:22Z",
                        "createdAt": "2025-01-10T09:00:00Z",
                        "updatedAt": "2025-06-18T16:45:00Z",
                    },
                    {
                        "id": "wf_mock_verifiabl_2",
                        "name": "Data Pipeline",
                        "description": "ETL workflow",
                        "color": "#4a90d9",
                        "folderId": "folder_mock_1",
                        "workspaceId": "ws_mock_1",
                        "isDeployed": True,
                        "deployedAt": "2025-06-14T08:00:00Z",
                        "runCount": 56,
                        "lastRunAt": "2025-06-19T09:00:00Z",
                        "createdAt": "2025-02-01T09:00:00Z",
                        "updatedAt": "2025-06-17T12:00:00Z",
                    },
                ],
                "nextCursor": None,
                "limits": _limits,
            }
        )

    @route("GET", "/api/v1/workflows/{id}", writes=False)
    async def get_workflow(self, request, id="", **kw):
        return MockResponse(
            body={
                "data": {
                    "id": id or "wf_mock_verifiabl_1",
                    "name": "Support Agent",
                    "description": "Routes incoming support tickets and drafts responses",
                    "color": "#33c482",
                    "folderId": "folder_mock_1",
                    "workspaceId": "ws_mock_1",
                    "isDeployed": True,
                    "deployedAt": "2025-06-15T10:30:00Z",
                    "runCount": 142,
                    "lastRunAt": "2025-06-20T14:15:22Z",
                    "variables": {},
                    "inputs": {"fields": {}},
                    "createdAt": "2025-01-10T09:00:00Z",
                    "updatedAt": "2025-06-18T16:45:00Z",
                },
                "limits": _limits,
            }
        )

    @route("POST", "/api/workflows/{workflowId}/execute")
    async def execute_workflow(self, request, workflowId="", **kw):
        return MockResponse(
            body={
                "success": True,
                "output": {"result": "Hello, world!"},
                "limits": _limits,
            }
        )

    @route("GET", "/api/jobs/{jobId}", writes=False)
    async def get_job(self, request, jobId="", **kw):
        return MockResponse(
            body={
                "success": True,
                "taskId": jobId or "job_mock_verifiabl",
                "status": "completed",
                "metadata": {
                    "startedAt": "2025-06-20T14:15:22Z",
                    "completedAt": "2025-06-20T14:15:23Z",
                    "duration": 1250,
                },
                "output": {"result": "Hello, world!"},
                "error": None,
                "estimatedDuration": 2000,
            }
        )

    @route("GET", "/api/v1/logs", writes=False)
    async def list_logs(self, request, **kw):
        return MockResponse(
            body={
                "data": [
                    {
                        "id": "log_mock_001",
                        "workflowId": "wf_mock_verifiabl_1",
                        "executionId": "exec_mock_001",
                        "level": "info",
                        "trigger": "api",
                        "startedAt": "2025-01-01T12:34:56.789Z",
                        "endedAt": "2025-01-01T12:34:57.123Z",
                        "totalDurationMs": 334,
                        "cost": {"total": 0.00234},
                        "files": None,
                    },
                    {
                        "id": "log_mock_002",
                        "workflowId": "wf_mock_verifiabl_1",
                        "executionId": "exec_mock_002",
                        "level": "info",
                        "trigger": "api",
                        "startedAt": "2025-01-01T12:35:00.000Z",
                        "endedAt": "2025-01-01T12:35:00.500Z",
                        "totalDurationMs": 500,
                        "cost": {"total": 0.00112},
                        "files": None,
                    },
                ],
                "nextCursor": None,
                "limits": _limits,
            }
        )

    @route("GET", "/api/v1/logs/{id}", writes=False)
    async def get_log(self, request, id="", **kw):
        return MockResponse(
            body={
                "data": {
                    "id": id or "log_mock_001",
                    "workflowId": "wf_mock_verifiabl_1",
                    "executionId": "exec_mock_001",
                    "level": "info",
                    "trigger": "api",
                    "startedAt": "2025-01-01T12:34:56.789Z",
                    "endedAt": "2025-01-01T12:34:57.123Z",
                    "totalDurationMs": 334,
                    "workflow": {
                        "id": "wf_mock_verifiabl_1",
                        "name": "Support Agent",
                        "description": "Routes tickets",
                    },
                    "executionData": {"traceSpans": [], "finalOutput": {}},
                    "cost": {
                        "total": 0.00234,
                        "tokens": {"prompt": 123, "completion": 456, "total": 579},
                        "models": {
                            "gpt-4o": {
                                "input": 0.001,
                                "output": 0.00134,
                                "total": 0.00234,
                                "tokens": {"prompt": 123, "completion": 456, "total": 579},
                            }
                        },
                    },
                    "limits": _limits,
                }
            }
        )

    @route("GET", "/api/v1/logs/executions/{executionId}", writes=False)
    async def get_execution(self, request, executionId="", **kw):
        return MockResponse(
            body={
                "executionId": executionId or "exec_mock_001",
                "workflowId": "wf_mock_verifiabl_1",
                "workflowState": {"blocks": {}, "edges": [], "loops": {}, "parallels": {}},
                "executionMetadata": {
                    "trigger": "api",
                    "startedAt": "2025-01-01T12:34:56.789Z",
                    "endedAt": "2025-01-01T12:34:57.123Z",
                    "totalDurationMs": 334,
                    "cost": {"total": 0.00234},
                },
            }
        )
