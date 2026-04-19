# CHANGELOG: https://developers.google.com/feeds/admin-sdk-release-notes.xml
# SPEC:      https://admin.googleapis.com/$discovery/rest?version=directory_v1
# SANDBOX:   https://admin.google.com
# FAVICON:   https://google.com/favicon.ico
# SKILL:     —
# MCP:       —
# LLMS:      —
from mocks.base import BaseMock, route
from models import MockResponse


class GoogleWorkspaceMock(BaseMock):
    prefix = "/googleworkspace"
    spec_url = "https://admin.googleapis.com/$discovery/rest?version=directory_v1"
    sandbox_base = "https://admin.googleapis.com"

    @route("GET", "/admin/directory/v1/users", writes=False)
    async def users_list(self, request, **kw):
        return MockResponse(
            body={
                "kind": "admin#directory#users",
                "users": [
                    {
                        "id": "user_mock_001",
                        "primaryEmail": "alice@verifiabl.dev",
                        "kind": "admin#directory#user",
                        "name": {
                            "givenName": "Alice",
                            "familyName": "User",
                            "fullName": "Alice User",
                        },
                    },
                    {
                        "id": "user_mock_002",
                        "primaryEmail": "bob@verifiabl.dev",
                        "kind": "admin#directory#user",
                        "name": {"givenName": "Bob", "familyName": "User", "fullName": "Bob User"},
                    },
                ],
                "nextPageToken": None,
            }
        )

    @route("GET", "/admin/directory/v1/users/{userKey}", writes=False)
    async def users_get(self, request, userKey="", **kw):
        return MockResponse(
            body={
                "id": userKey if userKey.isdigit() or "@" in userKey else "user_mock_001",
                "primaryEmail": "alice@verifiabl.dev",
                "kind": "admin#directory#user",
                "name": {"givenName": "Alice", "familyName": "User", "fullName": "Alice User"},
            }
        )

    @route("POST", "/admin/directory/v1/users")
    async def users_insert(self, request, **kw):
        return MockResponse(
            status=201,
            body={
                "id": "user_mock_new",
                "primaryEmail": "newuser@verifiabl.dev",
                "kind": "admin#directory#user",
                "name": {"givenName": "New", "familyName": "User", "fullName": "New User"},
            },
        )

    @route("PATCH", "/admin/directory/v1/users/{userKey}")
    async def users_patch(self, request, userKey="", **kw):
        return MockResponse(
            body={
                "id": userKey if userKey.isdigit() or "@" in userKey else "user_mock_001",
                "primaryEmail": "alice@verifiabl.dev",
                "kind": "admin#directory#user",
                "name": {"givenName": "Alice", "familyName": "User", "fullName": "Alice User"},
            }
        )

    @route("GET", "/admin/directory/v1/groups", writes=False)
    async def groups_list(self, request, **kw):
        return MockResponse(
            body={
                "kind": "admin#directory#groups",
                "groups": [
                    {
                        "id": "group_mock_001",
                        "email": "team@verifiabl.dev",
                        "name": "Team",
                        "kind": "admin#directory#group",
                    },
                    {
                        "id": "group_mock_002",
                        "email": "eng@verifiabl.dev",
                        "name": "Engineering",
                        "kind": "admin#directory#group",
                    },
                ],
                "nextPageToken": None,
            }
        )

    @route("GET", "/admin/directory/v1/groups/{groupKey}", writes=False)
    async def groups_get(self, request, groupKey="", **kw):
        return MockResponse(
            body={
                "id": "group_mock_001",
                "email": "team@verifiabl.dev",
                "name": "Team",
                "kind": "admin#directory#group",
            }
        )

    @route("POST", "/admin/directory/v1/groups")
    async def groups_insert(self, request, **kw):
        return MockResponse(
            status=201,
            body={
                "id": "group_mock_new",
                "email": "newgroup@verifiabl.dev",
                "name": "New Group",
                "kind": "admin#directory#group",
            },
        )

    @route("PUT", "/admin/directory/v1/groups/{groupKey}")
    async def groups_update(self, request, groupKey="", **kw):
        return MockResponse(
            body={
                "id": "group_mock_001",
                "email": "team@verifiabl.dev",
                "name": "Team Updated",
                "kind": "admin#directory#group",
            }
        )

    @route("GET", "/admin/directory/v1/groups/{groupKey}/members", writes=False)
    async def members_list(self, request, groupKey="", **kw):
        return MockResponse(
            body={
                "kind": "admin#directory#members",
                "members": [
                    {"id": "user_mock_001", "email": "alice@verifiabl.dev", "role": "MEMBER"},
                    {"id": "user_mock_002", "email": "bob@verifiabl.dev", "role": "MEMBER"},
                ],
                "nextPageToken": None,
            }
        )

    @route("POST", "/admin/directory/v1/groups/{groupKey}/members")
    async def members_insert(self, request, groupKey="", **kw):
        return MockResponse(
            status=201,
            body={
                "id": "user_mock_001",
                "email": "alice@verifiabl.dev",
                "role": "MEMBER",
                "kind": "admin#directory#member",
            },
        )
