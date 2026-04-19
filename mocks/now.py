# CHANGELOG: https://developer.servicenow.com/blog.do  (no RSS/atom feed found as of 2026-03)
# SPEC:      https://docs.servicenow.com/bundle/xanadu-api-reference/page/integrate/inbound-rest/concept/c_TableAPI.html
# SANDBOX:   https://developer.servicenow.com/
# SKILL:     —
# MCP:       —
# LLMS:      —
from mocks.base import BaseMock, route
from models import MockResponse


class NowMock(BaseMock):
    prefix = "/now"
    spec_url = "https://docs.servicenow.com/bundle/xanadu-api-reference/page/integrate/inbound-rest/concept/c_TableAPI.html"
    sandbox_base = "https://instance.service-now.com"

    @route("GET", "/api/now/table/incident", writes=False)
    async def list_incidents(self, request, **kw):
        return MockResponse(
            body={
                "result": [
                    {
                        "sys_id": "inc_mock_001",
                        "number": "INC0010001",
                        "short_description": "Mock incident",
                        "state": "2",
                        "sys_created_on": "2024-03-14T12:00:00",
                    },
                    {
                        "sys_id": "inc_mock_002",
                        "number": "INC0010002",
                        "short_description": "Second incident",
                        "state": "1",
                        "sys_created_on": "2024-03-14T13:00:00",
                    },
                ]
            }
        )

    @route("GET", "/api/now/table/incident/{sys_id}", writes=False)
    async def get_incident(self, request, sys_id="", **kw):
        return MockResponse(
            body={
                "result": {
                    "sys_id": sys_id or "inc_mock_001",
                    "number": "INC0010001",
                    "short_description": "Mock incident",
                    "state": "2",
                    "sys_created_on": "2024-03-14T12:00:00",
                }
            }
        )

    @route("POST", "/api/now/table/incident")
    async def create_incident(self, request, **kw):
        return MockResponse(
            status=201,
            body={
                "result": {
                    "sys_id": "inc_mock_new",
                    "number": "INC0010003",
                    "short_description": "New incident",
                    "state": "1",
                    "sys_created_on": "2024-03-14T14:00:00",
                }
            },
        )

    @route("PATCH", "/api/now/table/incident/{sys_id}")
    async def update_incident(self, request, sys_id="", **kw):
        return MockResponse(
            body={
                "result": {
                    "sys_id": sys_id or "inc_mock_001",
                    "number": "INC0010001",
                    "short_description": "Updated incident",
                    "state": "3",
                    "sys_updated_on": "2024-03-14T15:00:00",
                }
            }
        )

    @route("GET", "/api/now/table/change_request", writes=False)
    async def list_change_requests(self, request, **kw):
        return MockResponse(
            body={
                "result": [
                    {
                        "sys_id": "chg_mock_001",
                        "number": "CHG0010001",
                        "short_description": "Mock change",
                        "state": "1",
                        "phase": "build",
                    },
                    {
                        "sys_id": "chg_mock_002",
                        "number": "CHG0010002",
                        "short_description": "Second change",
                        "state": "3",
                        "phase": "closed",
                    },
                ]
            }
        )

    @route("GET", "/api/now/table/change_request/{sys_id}", writes=False)
    async def get_change_request(self, request, sys_id="", **kw):
        return MockResponse(
            body={
                "result": {
                    "sys_id": sys_id or "chg_mock_001",
                    "number": "CHG0010001",
                    "short_description": "Mock change",
                    "state": "1",
                    "phase": "build",
                    "sys_created_on": "2024-03-14T12:00:00",
                }
            }
        )

    @route("POST", "/api/now/table/change_request")
    async def create_change_request(self, request, **kw):
        return MockResponse(
            status=201,
            body={
                "result": {
                    "sys_id": "chg_mock_new",
                    "number": "CHG0010003",
                    "short_description": "New change",
                    "state": "1",
                    "phase": "draft",
                    "sys_created_on": "2024-03-14T14:00:00",
                }
            },
        )

    @route("GET", "/api/now/table/sys_user", writes=False)
    async def list_users(self, request, **kw):
        return MockResponse(
            body={
                "result": [
                    {
                        "sys_id": "user_mock_001",
                        "user_name": "admin",
                        "email": "admin@verifiabl.dev",
                        "name": "Admin User",
                    },
                    {
                        "sys_id": "user_mock_002",
                        "user_name": "jane.doe",
                        "email": "jane@verifiabl.dev",
                        "name": "Jane Doe",
                    },
                ]
            }
        )

    @route("GET", "/api/now/table/sys_user/{sys_id}", writes=False)
    async def get_user(self, request, sys_id="", **kw):
        return MockResponse(
            body={
                "result": {
                    "sys_id": sys_id or "user_mock_001",
                    "user_name": "admin",
                    "email": "admin@verifiabl.dev",
                    "name": "Admin User",
                }
            }
        )
