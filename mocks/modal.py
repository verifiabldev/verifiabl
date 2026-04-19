# CHANGELOG: https://modal.com/docs (no RSS/atom feed as of 2026-03)
# SPEC:      https://modal.com/docs/reference (Python SDK; no public REST/OpenAPI — mock derived from CLI/SDK)
# SANDBOX:   https://modal.com
# SKILL:     —
# MCP:       —
# LLMS:      —
from mocks.base import BaseMock, route
from models import MockResponse


class ModalMock(BaseMock):
    prefix = "/modal"
    spec_url = "https://modal.com/docs/reference"
    sandbox_base = "https://api.modal.com"

    @route("GET", "/v1/apps", writes=False)
    async def list_apps(self, request, **kw):
        return MockResponse(
            body={
                "apps": [
                    {
                        "app_id": "ap_mock_verifiabl01",
                        "name": "whisper-pod-transcriber",
                        "state": "deployed",
                        "created_at": 1710400000,
                    },
                    {
                        "app_id": "ap_mock_verifiabl02",
                        "name": "my-shared-app",
                        "state": "deployed",
                        "created_at": 1710400100,
                    },
                ]
            }
        )

    @route("GET", "/v1/apps/{app_id}", writes=False)
    async def get_app(self, request, app_id="", **kw):
        return MockResponse(
            body={
                "app_id": app_id or "ap_mock_verifiabl01",
                "name": "whisper-pod-transcriber",
                "state": "deployed",
                "created_at": 1710400000,
                "web_endpoints": [
                    {
                        "label": "fastapi_app",
                        "url": "https://modal-labs-whisper-pod-transcriber-fastapi-app.modal.run",
                    }
                ],
            }
        )

    @route("GET", "/v1/apps/{app_id}/deployments", writes=False)
    async def list_deployments(self, request, app_id="", **kw):
        return MockResponse(
            body={
                "deployments": [
                    {"version": 2, "deployed_at": 1710400000, "state": "active"},
                    {"version": 1, "deployed_at": 1710300000, "state": "replaced"},
                ]
            }
        )

    @route("POST", "/v1/apps/{app_id}/stop")
    async def stop_app(self, request, app_id="", **kw):
        return MockResponse(body={"app_id": app_id or "ap_mock_verifiabl01", "state": "stopped"})

    @route("GET", "/v1/runs/{run_id}", writes=False)
    async def get_run(self, request, run_id="", **kw):
        return MockResponse(
            body={
                "run_id": run_id or "fc_mock_001",
                "status": "completed",
                "function_name": "square",
                "app_name": "my-shared-app",
                "created_at": 1710400000,
                "finished_at": 1710400001,
            }
        )

    @route("POST", "/v1/apps/{app_name}/functions/{function_name}/spawn")
    async def spawn_function(self, request, app_name="", function_name="", **kw):
        return MockResponse(
            status=202,
            body={
                "run_id": "fc_mock_new",
                "status": "pending",
                "app_name": app_name or "my-shared-app",
                "function_name": function_name or "square",
            },
        )
