# CHANGELOG: https://posthog.com/changelog  (no RSS/atom feed as of 2026-03)
# SPEC:      https://posthog.com/docs/api/overview (OpenAPI at app.posthog.com/api/schema/ when logged in)
# SANDBOX:   https://us.posthog.com
# SKILL:     —
# MCP:       —
# LLMS:      —
from mocks.base import BaseMock, route
from models import MockResponse


class PosthogMock(BaseMock):
    prefix = "/posthog"
    spec_url = "https://posthog.com/docs/api/overview"
    sandbox_base = "https://us.posthog.com"

    @route("GET", "/api/organizations/{organization_id}/projects/", writes=False)
    async def list_projects(self, request, organization_id="", **kw):
        return MockResponse(
            body={
                "count": 2,
                "next": None,
                "previous": None,
                "results": [
                    {
                        "id": 1,
                        "uuid": "proj_mock_001",
                        "name": "Production",
                        "api_token": "phc_mock_001",
                    },
                    {
                        "id": 2,
                        "uuid": "proj_mock_002",
                        "name": "Staging",
                        "api_token": "phc_mock_002",
                    },
                ],
            }
        )

    @route("GET", "/api/projects/{project_id}/events/", writes=False)
    async def list_events(self, request, project_id="", **kw):
        return MockResponse(
            body={
                "next": None,
                "previous": None,
                "results": [
                    {
                        "id": "evt_mock_001",
                        "distinct_id": "user_1",
                        "event": "$pageview",
                        "timestamp": "2026-03-14T12:00:00Z",
                        "properties": {},
                    },
                    {
                        "id": "evt_mock_002",
                        "distinct_id": "user_1",
                        "event": "clicked",
                        "timestamp": "2026-03-14T12:01:00Z",
                        "properties": {},
                    },
                ],
            }
        )

    @route("GET", "/api/projects/{project_id}/events/{id}/", writes=False)
    async def get_event(self, request, project_id="", id="", **kw):
        return MockResponse(
            body={
                "id": id or "evt_mock_001",
                "distinct_id": "user_1",
                "event": "$pageview",
                "timestamp": "2026-03-14T12:00:00Z",
                "properties": {},
                "person": None,
                "elements": None,
                "elements_chain": None,
            }
        )

    @route("GET", "/api/projects/{project_id}/feature_flags/", writes=False)
    async def list_feature_flags(self, request, project_id="", **kw):
        return MockResponse(
            body={
                "count": 2,
                "next": None,
                "previous": None,
                "results": [
                    {
                        "id": 1,
                        "name": "beta-feature",
                        "key": "beta-feature",
                        "active": True,
                        "filters": {},
                        "deleted": False,
                    },
                    {
                        "id": 2,
                        "name": "dark-mode",
                        "key": "dark-mode",
                        "active": True,
                        "filters": {},
                        "deleted": False,
                    },
                ],
            }
        )

    @route("POST", "/api/projects/{project_id}/feature_flags/")
    async def create_feature_flag(self, request, project_id="", **kw):
        return MockResponse(
            status=201,
            body={
                "id": 3,
                "name": "new-flag",
                "key": "new-flag",
                "active": True,
                "filters": {},
                "deleted": False,
            },
        )

    @route("GET", "/api/projects/{project_id}/feature_flags/{id}/", writes=False)
    async def get_feature_flag(self, request, project_id="", id="", **kw):
        return MockResponse(
            body={
                "id": int(id) if id.isdigit() else 1,
                "name": "beta-feature",
                "key": "beta-feature",
                "active": True,
                "filters": {},
                "deleted": False,
            }
        )

    @route("PATCH", "/api/projects/{project_id}/feature_flags/{id}/")
    async def update_feature_flag(self, request, project_id="", id="", **kw):
        return MockResponse(
            body={
                "id": int(id) if id.isdigit() else 1,
                "name": "beta-feature",
                "key": "beta-feature",
                "active": False,
                "filters": {},
                "deleted": False,
            }
        )

    @route("DELETE", "/api/projects/{project_id}/feature_flags/{id}/")
    async def delete_feature_flag(self, request, project_id="", id="", **kw):
        return MockResponse(body={"deleted": True})

    @route("GET", "/api/environments/{environment_id}/persons/", writes=False)
    async def list_persons(self, request, environment_id="", **kw):
        return MockResponse(
            body={
                "count": 2,
                "next": None,
                "previous": None,
                "results": [
                    {
                        "id": 1,
                        "name": "Alice",
                        "distinct_ids": ["user_1"],
                        "properties": {},
                        "created_at": "2026-03-14T12:00:00Z",
                        "uuid": "095be615-a8ad-4c33-8e9c-c7612fbf6c9f",
                        "last_seen_at": "2026-03-14T12:00:00Z",
                    },
                    {
                        "id": 2,
                        "name": "Bob",
                        "distinct_ids": ["user_2"],
                        "properties": {},
                        "created_at": "2026-03-14T11:00:00Z",
                        "uuid": "195be615-a8ad-4c33-8e9c-c7612fbf6c9g",
                        "last_seen_at": "2026-03-14T11:30:00Z",
                    },
                ],
            }
        )

    @route("GET", "/api/environments/{environment_id}/persons/{id}/", writes=False)
    async def get_person(self, request, environment_id="", id="", **kw):
        return MockResponse(
            body={
                "id": int(id) if id.isdigit() else 1,
                "name": "Alice",
                "distinct_ids": ["user_1"],
                "properties": {},
                "created_at": "2026-03-14T12:00:00Z",
                "uuid": "095be615-a8ad-4c33-8e9c-c7612fbf6c9f",
                "last_seen_at": "2026-03-14T12:00:00Z",
            }
        )
