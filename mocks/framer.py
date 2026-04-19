# CHANGELOG: https://www.framer.com/updates  (no RSS/atom feed as of 2026-03)
# SPEC:      https://www.framer.com/developers/server-api-reference
# SANDBOX:   https://framer.com (API key in Site Settings; Server API is WebSocket/SDK, no public REST)
# SKILL:     —
# MCP:       —
# LLMS:      —
from mocks.base import BaseMock, route
from models import MockResponse


class FramerMock(BaseMock):
    prefix = "/framer"
    spec_url = "https://www.framer.com/developers/server-api-reference"
    sandbox_base = "https://api.framer.com"

    @route("GET", "/v1/project", writes=False)
    async def get_project_info(self, request, **kw):
        return MockResponse(body={"name": "Mock Project", "id": "proj_mock_verifiabl"})

    @route("GET", "/v1/publish-info", writes=False)
    async def get_publish_info(self, request, **kw):
        return MockResponse(
            body={
                "staging": {
                    "deploymentTime": 1710400000,
                    "optimizationStatus": "optimized",
                    "url": "https://mock.framer.website",
                    "currentPageUrl": "https://mock.framer.website/",
                },
                "production": {
                    "deploymentTime": 1710300000,
                    "optimizationStatus": "optimized",
                    "url": "https://mock.framer.site",
                    "currentPageUrl": "https://mock.framer.site/",
                },
            }
        )

    @route("GET", "/v1/changed-paths", writes=False)
    async def get_changed_paths(self, request, **kw):
        return MockResponse(body={"added": ["/about"], "removed": [], "modified": ["/index"]})

    @route("GET", "/v1/change-contributors", writes=False)
    async def get_change_contributors(self, request, **kw):
        return MockResponse(body=["mock@verifiabl.dev"])

    @route("POST", "/v1/publish")
    async def publish(self, request, **kw):
        return MockResponse(
            status=201,
            body={
                "deployment": {"id": "dep_mock_001"},
                "hostnames": ["https://preview-mock.framer.website"],
            },
        )

    @route("POST", "/v1/deploy")
    async def deploy(self, request, **kw):
        return MockResponse(body={"deployment": {"id": "dep_mock_001"}})

    @route("GET", "/v1/collections", writes=False)
    async def get_collections(self, request, **kw):
        return MockResponse(
            body={
                "collections": [
                    {
                        "id": "col_mock_001",
                        "name": "Blog Posts",
                        "managedBy": None,
                        "readonly": False,
                    },
                    {
                        "id": "col_mock_002",
                        "name": "Team",
                        "managedBy": "plugin",
                        "readonly": False,
                    },
                ],
            }
        )

    @route("POST", "/v1/collections")
    async def create_managed_collection(self, request, **kw):
        return MockResponse(
            status=201,
            body={
                "id": "col_mock_003",
                "name": "New Collection",
                "managedBy": "plugin",
                "readonly": False,
            },
        )
