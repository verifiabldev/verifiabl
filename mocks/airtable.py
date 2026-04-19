# CHANGELOG: https://www.airtable.com/developers/web/api/changelog (no RSS/atom feed as of 2026-03)
# SPEC:      https://www.airtable.com/developers/web/api/introduction
# SANDBOX:   https://airtable.com/create
# SKILL:     —
# MCP:       https://support.airtable.com/docs/using-the-airtable-mcp-server
# LLMS:      —
# AUTH:      Bearer token in Authorization header (Personal Access Token)
from mocks.base import BaseMock, route
from models import MockResponse


def _record(rid: str, fields: dict):
    return {"id": rid, "createdTime": "2024-03-14T12:00:00.000Z", "fields": fields}


class AirtableMock(BaseMock):
    prefix = "/airtable"
    spec_url = "https://www.airtable.com/developers/web/api/introduction"
    sandbox_base = "https://api.airtable.com"

    @route("GET", "/v0/meta/bases", writes=False)
    async def list_bases(self, request, **kw):
        return MockResponse(
            body={
                "bases": [
                    {
                        "id": "app_mock_verifiabl",
                        "name": "Verifiabl Mock",
                        "permissionLevel": "create",
                    },
                ],
            }
        )

    @route("GET", "/v0/meta/bases/{baseId}/tables", writes=False)
    async def get_base_schema(self, request, baseId="", **kw):
        return MockResponse(
            body={
                "tables": [
                    {
                        "id": "tbl_mock_tasks",
                        "name": "Tasks",
                        "description": "Mock tasks",
                        "fields": [{"id": "fld_name", "name": "Name", "type": "singleLineText"}],
                    },
                ],
            }
        )

    @route("GET", "/v0/{baseId}/{tableIdOrName}", writes=False)
    async def list_records(self, request, baseId="", tableIdOrName="", **kw):
        return MockResponse(
            body={
                "records": [
                    _record("rec_mock_001", {"Name": "First task"}),
                    _record("rec_mock_002", {"Name": "Second task"}),
                ],
            }
        )

    @route("GET", "/v0/{baseId}/{tableIdOrName}/{recordId}", writes=False)
    async def get_record(self, request, baseId="", tableIdOrName="", recordId="", **kw):
        return MockResponse(body=_record(recordId or "rec_mock_001", {"Name": "Mock task"}))

    @route("POST", "/v0/{baseId}/{tableIdOrName}")
    async def create_records(self, request, baseId="", tableIdOrName="", **kw):
        return MockResponse(
            status=201,
            body={
                "records": [_record("rec_mock_new", {"Name": "New record"})],
            },
        )

    @route("PATCH", "/v0/{baseId}/{tableIdOrName}/{recordId}")
    async def update_record(self, request, baseId="", tableIdOrName="", recordId="", **kw):
        return MockResponse(body=_record(recordId or "rec_mock_001", {"Name": "Updated"}))

    @route("PATCH", "/v0/{baseId}/{tableIdOrName}")
    async def update_records(self, request, baseId="", tableIdOrName="", **kw):
        return MockResponse(body={"records": [_record("rec_mock_001", {"Name": "Updated"})]})

    @route("DELETE", "/v0/{baseId}/{tableIdOrName}/{recordId}")
    async def delete_record(self, request, baseId="", tableIdOrName="", recordId="", **kw):
        return MockResponse(body={"id": recordId or "rec_mock_001", "deleted": True})
