# CHANGELOG: https://developers.feedly.com/changelog (no RSS/atom feed as of 2026-03)
# SPEC:      https://developers.feedly.com/reference/introduction
# SANDBOX:   https://feedly.com (API token from account)
# SKILL:     —
# MCP:       —
# LLMS:      —
from mocks.base import BaseMock, route
from models import MockResponse


class FeedlyMock(BaseMock):
    prefix = "/feedly"
    spec_url = "https://developers.feedly.com/reference/introduction"
    sandbox_base = "https://api.feedly.com"

    @route("GET", "/v3/profile", writes=False)
    async def get_profile(self, request, **kw):
        return MockResponse(
            body={
                "id": "user_mock_verifiabl",
                "email": "dev@verifiabl.dev",
                "givenName": "Verifiabl",
                "familyName": "Mock",
                "picture": "https://verifiabl.dev/avatar.png",
                "locale": "en",
                "wave": "feedly_mock_001",
            }
        )

    @route("GET", "/v3/categories", writes=False)
    async def list_categories(self, request, **kw):
        return MockResponse(
            body=[
                {"id": "user/user_mock_verifiabl/category/tech", "label": "Tech"},
                {"id": "user/user_mock_verifiabl/category/design", "label": "Design"},
            ]
        )

    @route("GET", "/v3/subscriptions", writes=False)
    async def list_subscriptions(self, request, **kw):
        return MockResponse(
            body=[
                {
                    "id": "feed/https://verifiabl.dev/feed.xml",
                    "title": "Verifiabl Blog",
                    "website": "https://verifiabl.dev",
                    "categories": [
                        {"id": "user/user_mock_verifiabl/category/tech", "label": "Tech"}
                    ],
                },
                {
                    "id": "feed/https://verifiabl.dev/rss",
                    "title": "Example Feed",
                    "website": "https://verifiabl.dev",
                    "categories": [],
                },
            ]
        )

    @route("GET", "/v3/streams/contents", writes=False)
    async def streams_contents(self, request, **kw):
        return MockResponse(
            body={
                "id": "user/user_mock_verifiabl/category/global.all",
                "updated": 1710400000000,
                "continuation": "180056e12c9:1a7979e:26e2bd2e",
                "items": [
                    {
                        "id": "PSNTZO8gXFUe+cpCZyApw0vEKWPT4b14D6teBEocIAE=_174faa24b8c:18d07f2:2694a93d",
                        "title": "Mock article one",
                        "published": 1710400000000,
                        "origin": {
                            "streamId": "feed/https://verifiabl.dev/feed.xml",
                            "title": "Verifiabl Blog",
                        },
                        "alternate": [
                            {"href": "https://verifiabl.dev/post/1", "type": "text/html"}
                        ],
                    },
                    {
                        "id": "entry_mock_002_verifiabl",
                        "title": "Mock article two",
                        "published": 1710399000000,
                        "origin": {
                            "streamId": "feed/https://verifiabl.dev/rss",
                            "title": "Example Feed",
                        },
                        "alternate": [{"href": "https://verifiabl.dev/2", "type": "text/html"}],
                    },
                ],
            }
        )

    @route("POST", "/v3/search", writes=False)
    async def search(self, request, **kw):
        return MockResponse(
            body={
                "results": [
                    {
                        "query": "verifiabl",
                        "score": 1.0,
                        "id": "feed/https://verifiabl.dev/feed.xml",
                        "title": "Verifiabl Blog",
                        "subscribers": 100,
                    },
                ],
            }
        )

    @route("POST", "/v3/markers")
    async def markers(self, request, **kw):
        return MockResponse(body={"success": True})

    @route("GET", "/v3/enterprise/tags", writes=False)
    async def enterprise_tags(self, request, **kw):
        return MockResponse(
            body=[
                "user/user_mock_verifiabl/board/board_mock_001",
                "user/user_mock_verifiabl/board/board_mock_002",
            ]
        )
