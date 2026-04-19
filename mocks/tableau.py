# CHANGELOG: https://help.tableau.com/current/api/rest_api/en-us/REST/rest_api_whats_new.htm  (no RSS/atom feed as of 2026-03)
# SPEC:      https://help.tableau.com/current/api/rest_api/en-us/REST/rest_api_ref.htm
# SANDBOX:   https://10ay.online.tableau.com
# SKILL:     —
# MCP:       —
# LLMS:      —
from mocks.base import BaseMock, route
from models import MockResponse


class TableauMock(BaseMock):
    prefix = "/tableau"
    spec_url = "https://help.tableau.com/current/api/rest_api/en-us/REST/rest_api_ref.htm"
    sandbox_base = "https://10ay.online.tableau.com"

    @route("POST", "/api/3.28/auth/signin")
    async def signin(self, request, **kw):
        return MockResponse(
            body={
                "credentials": {
                    "token": "mock_token_verifiabl",
                    "estimatedTimeToExpiration": "2:00:00",
                    "site": {"id": "site_mock_001", "contentUrl": "mock"},
                    "user": {"id": "user_mock_001"},
                },
            }
        )

    @route("GET", "/api/3.28/sites/{site_id}/workbooks", writes=False)
    async def list_workbooks(self, request, site_id="", **kw):
        return MockResponse(
            body={
                "pagination": {"pageNumber": 1, "pageSize": 100, "totalAvailable": 2},
                "workbooks": [
                    {"id": "wb_mock_001", "name": "Sales Dashboard", "projectId": "proj_mock_001"},
                    {"id": "wb_mock_002", "name": "Finance Views", "projectId": "proj_mock_001"},
                ],
            }
        )

    @route("GET", "/api/3.28/sites/{site_id}/workbooks/{workbook_id}", writes=False)
    async def get_workbook(self, request, site_id="", workbook_id="", **kw):
        return MockResponse(
            body={
                "workbook": {
                    "id": workbook_id or "wb_mock_001",
                    "name": "Sales Dashboard",
                    "projectId": "proj_mock_001",
                    "views": [{"id": "view_mock_001", "name": "Overview"}],
                },
            }
        )

    @route("GET", "/api/3.28/sites/{site_id}/views", writes=False)
    async def list_views(self, request, site_id="", **kw):
        return MockResponse(
            body={
                "pagination": {"pageNumber": 1, "pageSize": 100, "totalAvailable": 2},
                "views": [
                    {"id": "view_mock_001", "name": "Overview", "workbookId": "wb_mock_001"},
                    {"id": "view_mock_002", "name": "Detail", "workbookId": "wb_mock_001"},
                ],
            }
        )

    @route("GET", "/api/3.28/sites/{site_id}/views/{view_id}", writes=False)
    async def get_view(self, request, site_id="", view_id="", **kw):
        return MockResponse(
            body={
                "view": {
                    "id": view_id or "view_mock_001",
                    "name": "Overview",
                    "workbookId": "wb_mock_001",
                },
            }
        )

    @route("GET", "/api/3.28/sites/{site_id}/projects", writes=False)
    async def list_projects(self, request, site_id="", **kw):
        return MockResponse(
            body={
                "pagination": {"pageNumber": 1, "pageSize": 100, "totalAvailable": 1},
                "projects": [{"id": "proj_mock_001", "name": "Default"}],
            }
        )

    @route("GET", "/api/3.28/sites/{site_id}/datasources", writes=False)
    async def list_datasources(self, request, site_id="", **kw):
        return MockResponse(
            body={
                "pagination": {"pageNumber": 1, "pageSize": 100, "totalAvailable": 1},
                "datasources": [
                    {"id": "ds_mock_001", "name": "Sample", "projectId": "proj_mock_001"}
                ],
            }
        )

    @route("POST", "/api/3.28/sites/{site_id}/workbooks")
    async def publish_workbook(self, request, site_id="", **kw):
        return MockResponse(
            status=201,
            body={
                "workbook": {
                    "id": "wb_mock_new",
                    "name": "New Workbook",
                    "projectId": "proj_mock_001",
                },
            },
        )
