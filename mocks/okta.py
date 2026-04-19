# CHANGELOG: https://developer.okta.com/feed.xml
# SPEC:      https://github.com/okta/okta-management-openapi-spec
# SANDBOX:   https://developer.okta.com/signup/
# SKILL:     —
# MCP:       https://developer.okta.com/docs/concepts/mcp-server
# LLMS:      —
from mocks.base import BaseMock, route
from models import MockResponse

_USER = {
    "id": "usr_mock_verifiabl",
    "status": "ACTIVE",
    "created": "2024-03-14T12:00:00.000Z",
    "lastUpdated": "2024-03-14T12:00:00.000Z",
    "profile": {
        "firstName": "Mock",
        "lastName": "User",
        "email": "mock@verifiabl.dev",
        "login": "mock@verifiabl.dev",
    },
}
_APP = {
    "id": "0oa_mock_verifiabl",
    "name": "oidc_client",
    "label": "Mock OIDC App",
    "status": "ACTIVE",
    "signOnMode": "OPENID_CONNECT",
}


class OktaMock(BaseMock):
    prefix = "/okta"
    spec_url = "https://github.com/okta/okta-management-openapi-spec"
    sandbox_base = "https://example.okta.com"

    @route("GET", "/api/v1/users", writes=False)
    async def list_users(self, request, **kw):
        return MockResponse(
            body=[
                _USER,
                {
                    **_USER,
                    "id": "usr_mock_002",
                    "profile": {
                        **_USER["profile"],
                        "email": "alice@verifiabl.dev",
                        "login": "alice@verifiabl.dev",
                    },
                },
            ]
        )

    @route("POST", "/api/v1/users")
    async def create_user(self, request, **kw):
        return MockResponse(status=201, body={**_USER, "id": "usr_mock_new", "status": "STAGED"})

    @route("GET", "/api/v1/users/{userId}", writes=False)
    async def get_user(self, request, userId="", **kw):
        return MockResponse(body={**_USER, "id": userId or _USER["id"]})

    @route("PUT", "/api/v1/users/{userId}")
    async def update_user(self, request, userId="", **kw):
        return MockResponse(body={**_USER, "id": userId or _USER["id"]})

    @route("GET", "/api/v1/apps", writes=False)
    async def list_apps(self, request, **kw):
        return MockResponse(body=[_APP, {**_APP, "id": "0oa_mock_002", "label": "Mock SAML App"}])

    @route("POST", "/api/v1/apps")
    async def create_app(self, request, **kw):
        return MockResponse(status=201, body={**_APP, "id": "0oa_mock_new", "status": "INACTIVE"})

    @route("GET", "/api/v1/apps/{appId}", writes=False)
    async def get_app(self, request, appId="", **kw):
        return MockResponse(body={**_APP, "id": appId or _APP["id"]})

    @route("GET", "/api/v1/apps/{appId}/users", writes=False)
    async def list_app_users(self, request, appId="", **kw):
        return MockResponse(
            body=[
                {
                    **_USER,
                    "id": "usr_mock_001",
                    "scope": "USER",
                    "credentials": {"userName": "mock@verifiabl.dev"},
                }
            ]
        )

    @route("POST", "/api/v1/apps/{appId}/users")
    async def assign_user_to_app(self, request, appId="", **kw):
        return MockResponse(
            body={
                "id": "aua_mock_001",
                "scope": "USER",
                "credentials": {"userName": "mock@verifiabl.dev"},
                "embedded": {"user": _USER},
            }
        )
