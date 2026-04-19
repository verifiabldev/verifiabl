# CHANGELOG: https://help.zscaler.com/legacy-apis/getting-started-zia-api  (no RSS/atom feed as of 2026-03)
# SPEC:      https://help.zscaler.com/legacy-apis/understanding-zia-api
# SANDBOX:   https://help.zscaler.com/zia/getting-started-zia-api
# SKILL:     —
# MCP:       —
# LLMS:      —
from mocks.base import BaseMock, route
from models import MockResponse

_USER = {
    "id": 49916183,
    "name": "Mock User",
    "email": "mock@verifiabl.dev",
    "department": {"id": 49814321, "name": "Engineering"},
    "groups": [{"id": 49916184, "name": "All Users"}],
    "deleted": False,
}
_GROUP = {"id": 49916184, "name": "All Users", "idpId": None, "comments": ""}
_DEPT = {"id": 49814321, "name": "Engineering", "comments": ""}
_LOC = {
    "id": 49814322,
    "name": "HQ",
    "country": "US",
    "ipAddresses": ["192.0.2.0/24"],
    "subLocation": False,
}
_RULE = {
    "id": 977463,
    "name": "Allow Social Media",
    "action": "ALLOW",
    "state": "ENABLED",
    "order": 1,
    "protocols": ["ANY_RULE"],
}


class ZscalerMock(BaseMock):
    prefix = "/zscaler"
    spec_url = "https://help.zscaler.com/legacy-apis/understanding-zia-api"
    sandbox_base = "https://admin.zscaler.com"

    @route("GET", "/users", writes=False)
    async def list_users(self, request, **kw):
        return MockResponse(
            body=[_USER, {**_USER, "id": 49916185, "name": "Alice", "email": "alice@verifiabl.dev"}]
        )

    @route("POST", "/users")
    async def create_user(self, request, **kw):
        return MockResponse(status=201, body={**_USER, "id": 49916199})

    @route("GET", "/users/{userId}", writes=False)
    async def get_user(self, request, userId="", **kw):
        uid = userId or "49916183"
        return MockResponse(body={**_USER, "id": int(uid) if uid.isdigit() else _USER["id"]})

    @route("PUT", "/users/{userId}")
    async def update_user(self, request, userId="", **kw):
        uid = userId or "49916183"
        return MockResponse(body={**_USER, "id": int(uid) if uid.isdigit() else _USER["id"]})

    @route("GET", "/groups", writes=False)
    async def list_groups(self, request, **kw):
        return MockResponse(body=[_GROUP, {**_GROUP, "id": 49916185, "name": "Finance"}])

    @route("GET", "/departments", writes=False)
    async def list_departments(self, request, **kw):
        return MockResponse(body=[_DEPT, {**_DEPT, "id": 49814322, "name": "Sales"}])

    @route("GET", "/locations", writes=False)
    async def list_locations(self, request, **kw):
        return MockResponse(body=[_LOC, {**_LOC, "id": 49814323, "name": "Branch"}])

    @route("GET", "/urlFilteringRules", writes=False)
    async def list_url_filtering_rules(self, request, **kw):
        return MockResponse(
            body=[_RULE, {**_RULE, "id": 977464, "name": "Block Malware", "action": "BLOCK"}]
        )

    @route("POST", "/urlFilteringRules")
    async def create_url_filtering_rule(self, request, **kw):
        return MockResponse(status=201, body={**_RULE, "id": 977469})

    @route("GET", "/urlFilteringRules/{ruleId}", writes=False)
    async def get_url_filtering_rule(self, request, ruleId="", **kw):
        rid = ruleId or "977463"
        return MockResponse(body={**_RULE, "id": int(rid) if rid.isdigit() else _RULE["id"]})

    @route("PUT", "/urlFilteringRules/{ruleId}")
    async def update_url_filtering_rule(self, request, ruleId="", **kw):
        rid = ruleId or "977463"
        return MockResponse(body={**_RULE, "id": int(rid) if rid.isdigit() else _RULE["id"]})
