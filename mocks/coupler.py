# CHANGELOG: https://docs.coupler.io  (no RSS/atom feed as of 2026-03)
# SPEC:      https://docs.coupler.io (no public OpenAPI — mock inferred from product)
# SANDBOX:   https://app.coupler.io
# SKILL:     —
# MCP:       —
# LLMS:      —
from mocks.base import BaseMock, route
from models import MockResponse


# LOC EXCEPTION: Importers, runs, and webhooks resources required for data-integration agent workflows.
class CouplerMock(BaseMock):
    prefix = "/coupler"
    spec_url = "https://docs.coupler.io"
    sandbox_base = "https://api.coupler.io"

    @route("GET", "/v1/importers", writes=False)
    async def list_importers(self, request, **kw):
        return MockResponse(
            body={
                "data": [
                    {
                        "id": "imp_mock_001",
                        "name": "Sales to Sheets",
                        "source_type": "salesforce",
                        "destination_type": "google_sheets",
                        "status": "active",
                        "created_at": 1710400000,
                    },
                    {
                        "id": "imp_mock_002",
                        "name": "HubSpot Export",
                        "source_type": "hubspot",
                        "destination_type": "google_sheets",
                        "status": "active",
                        "created_at": 1710400100,
                    },
                ],
                "next_cursor": None,
            }
        )

    @route("GET", "/v1/importers/{id}", writes=False)
    async def get_importer(self, request, id="", **kw):
        return MockResponse(
            body={
                "id": id or "imp_mock_001",
                "name": "Sales to Sheets",
                "source_type": "salesforce",
                "source_config": {"object": "Lead"},
                "destination_type": "google_sheets",
                "destination_config": {"spreadsheet_id": "sheet_mock_001"},
                "status": "active",
                "schedule": "0 */6 * * *",
                "created_at": 1710400000,
                "updated_at": 1710486400,
            }
        )

    @route("POST", "/v1/importers")
    async def create_importer(self, request, **kw):
        return MockResponse(
            status=201,
            body={
                "id": "imp_mock_new",
                "name": "New Importer",
                "source_type": "custom_api",
                "destination_type": "google_sheets",
                "status": "active",
                "created_at": 1710400000,
            },
        )

    @route("PATCH", "/v1/importers/{id}")
    async def update_importer(self, request, id="", **kw):
        return MockResponse(
            body={
                "id": id or "imp_mock_001",
                "name": "Sales to Sheets",
                "status": "active",
                "updated_at": 1710486400,
            }
        )

    @route("GET", "/v1/importers/{id}/runs", writes=False)
    async def list_importer_runs(self, request, id="", **kw):
        return MockResponse(
            body={
                "data": [
                    {
                        "id": "run_mock_001",
                        "importer_id": id or "imp_mock_001",
                        "status": "completed",
                        "started_at": 1710400000,
                        "finished_at": 1710400120,
                        "rows_imported": 150,
                    },
                    {
                        "id": "run_mock_002",
                        "importer_id": id or "imp_mock_001",
                        "status": "completed",
                        "started_at": 1710396400,
                        "finished_at": 1710396520,
                        "rows_imported": 148,
                    },
                ],
                "next_cursor": None,
            }
        )

    @route("GET", "/v1/runs/{id}", writes=False)
    async def get_run(self, request, id="", **kw):
        return MockResponse(
            body={
                "id": id or "run_mock_001",
                "importer_id": "imp_mock_001",
                "status": "completed",
                "started_at": 1710400000,
                "finished_at": 1710400120,
                "rows_imported": 150,
                "error_message": None,
            }
        )

    @route("POST", "/v1/importers/{id}/run")
    async def trigger_run(self, request, id="", **kw):
        return MockResponse(
            status=202,
            body={
                "id": "run_mock_triggered",
                "importer_id": id or "imp_mock_001",
                "status": "queued",
                "started_at": None,
                "finished_at": None,
            },
        )

    @route("GET", "/v1/webhooks", writes=False)
    async def list_webhooks(self, request, **kw):
        return MockResponse(
            body={
                "data": [
                    {
                        "id": "wh_mock_001",
                        "url": "https://verifiabl.dev/coupler",
                        "events": ["run.completed"],
                        "active": True,
                        "created_at": 1710400000,
                    },
                ],
            }
        )

    @route("POST", "/v1/webhooks")
    async def create_webhook(self, request, **kw):
        return MockResponse(
            status=201,
            body={
                "id": "wh_mock_new",
                "url": "https://verifiabl.dev/coupler",
                "events": ["run.completed"],
                "active": True,
                "created_at": 1710400000,
            },
        )
