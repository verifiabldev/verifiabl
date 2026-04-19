# CHANGELOG: https://docs.gumloop.com (no RSS/atom feed as of 2026-03)
# SPEC:      https://docs.gumloop.com/api-reference/openapi.yaml
# SANDBOX:   https://www.gumloop.com
# SKILL:     —
# MCP:       —
# LLMS:      —
# AUTH:      Bearer token in Authorization header (per OpenAPI bearerAuth)
from mocks.base import BaseMock, route
from models import MockResponse


class GumloopMock(BaseMock):
    prefix = "/gumloop"
    spec_url = "https://docs.gumloop.com/api-reference/openapi.yaml"
    sandbox_base = "https://api.gumloop.com"

    @route("GET", "/api/v1/list_saved_items", writes=False)
    async def list_saved_items(self, request, **kw):
        return MockResponse(
            body={
                "saved_items": [
                    {
                        "saved_item_id": "saved_mock_verifiabl_1",
                        "name": "Support Triage",
                        "description": "Routes tickets",
                        "created_ts": "2024-01-15T10:00:00+00:00",
                    },
                    {
                        "saved_item_id": "saved_mock_verifiabl_2",
                        "name": "Data Sync",
                        "description": "Syncs warehouse",
                        "created_ts": "2024-02-01T14:30:00+00:00",
                    },
                ]
            }
        )

    @route("GET", "/api/v1/list_workbooks", writes=False)
    async def list_workbooks(self, request, **kw):
        return MockResponse(
            body={
                "workbooks": [
                    {
                        "workbook_id": "wb_mock_verifiabl_1",
                        "name": "Support",
                        "description": "Support flows",
                        "created_ts": "2024-01-10T09:00:00+00:00",
                        "saved_items": [
                            {
                                "saved_item_id": "saved_mock_verifiabl_1",
                                "name": "Support Triage",
                                "description": "Routes tickets",
                                "created_ts": "2024-01-15T10:00:00+00:00",
                            },
                        ],
                    },
                ]
            }
        )

    @route("GET", "/api/v1/get_inputs", writes=False)
    async def get_inputs(self, request, **kw):
        return MockResponse(
            body={
                "inputs": [
                    {"name": "recipient", "data_type": "string", "description": "Email recipient"},
                    {"name": "subject", "data_type": "string", "description": None},
                ]
            }
        )

    @route("POST", "/api/v1/start_pipeline")
    async def start_pipeline(self, request, **kw):
        return MockResponse(
            status=200,
            body={
                "run_id": "run_mock_verifiabl_001",
                "saved_item_id": "saved_mock_verifiabl_1",
                "workbook_id": "wb_mock_verifiabl_1",
                "url": "https://www.gumloop.com/pipeline?run_id=run_mock_verifiabl_001&flow_id=saved_mock_verifiabl_1",
            },
        )

    @route("GET", "/api/v1/get_pl_run", writes=False)
    async def get_pl_run(self, request, **kw):
        return MockResponse(
            body={
                "created_ts": "2024-06-19T18:06:31.102786+00:00",
                "finished_ts": "2024-06-19T18:06:32.500000+00:00",
                "log": ["\u001b[34m__system__: __STARTING__:Read files from GitHub\u001b[0m"],
                "outputs": {"result": "completed"},
                "run_id": "run_mock_verifiabl_001",
                "state": "DONE",
                "user_id": "user_mock_verifiabl",
            }
        )

    @route("POST", "/api/v1/kill_pipeline")
    async def kill_pipeline(self, request, **kw):
        return MockResponse(body={"success": True, "run_id": "run_mock_verifiabl_001"})

    @route("GET", "/api/v1/get_plrun_saved_item_map", writes=False)
    async def get_plrun_saved_item_map(self, request, **kw):
        return MockResponse(
            body={
                "saved_mock_verifiabl_1": [
                    {
                        "run_id": "run_mock_verifiabl_001",
                        "created_ts": "2024-06-19T18:06:31+00:00",
                        "state": "DONE",
                    },
                    {
                        "run_id": "run_mock_verifiabl_002",
                        "created_ts": "2024-06-18T12:00:00+00:00",
                        "state": "DONE",
                    },
                ]
            }
        )
