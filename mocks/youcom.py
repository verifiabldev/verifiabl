# CHANGELOG: https://docs.you.com (no RSS/atom feed as of 2026-03)
# SPEC:      https://docs.you.com/openapi.json
# SANDBOX:   https://you.com/platform/api-keys
# FAVICON:   https://you.com/favicon.ico
# SKILL:     —
# MCP:       —
# LLMS:      —
from mocks.base import BaseMock, route
from models import MockResponse


class YoucomMock(BaseMock):
    prefix = "/youcom"
    spec_url = "https://docs.you.com/openapi.json"
    sandbox_base = "https://ydc-index.io"

    @route("GET", "/v1/search", writes=False)
    async def search(self, request, **kw):
        return MockResponse(
            body={
                "results": {
                    "web": [
                        {
                            "url": "https://verifiabl.dev/page1",
                            "title": "Example Page 1",
                            "description": "A sample result.",
                            "snippets": ["Snippet one."],
                            "favicon_url": "https://verifiabl.dev/favicon.ico",
                        },
                        {
                            "url": "https://verifiabl.dev/page2",
                            "title": "Example Page 2",
                            "description": "Another result.",
                            "snippets": ["Snippet two."],
                            "favicon_url": "https://verifiabl.dev/favicon.ico",
                        },
                    ],
                    "news": [],
                },
                "metadata": {
                    "search_uuid": "you_mock_uuid_001",
                    "query": "test query",
                    "latency": 0.15,
                },
            }
        )

    @route("GET", "/search", writes=False)
    async def search_legacy(self, request, **kw):
        return MockResponse(
            body={
                "hits": [
                    {
                        "url": "https://verifiabl.dev/hit1",
                        "title": "Legacy Hit 1",
                        "description": "Legacy result.",
                        "snippets": ["Snippet."],
                        "favicon_url": "https://verifiabl.dev/favicon.ico",
                    },
                ],
                "latency": 0.12,
            }
        )

    @route("POST", "/v1/contents")
    async def contents(self, request, **kw):
        return MockResponse(
            body=[
                {
                    "url": "https://verifiabl.dev/doc",
                    "title": "Mock Page",
                    "html": "<p>Mock HTML</p>",
                    "markdown": "Mock Markdown",
                    "metadata": None,
                },
            ]
        )

    @route("POST", "/v1/research", writes=False)
    async def research(self, request, **kw):
        return MockResponse(
            body={
                "output": {
                    "content": "Mock research answer with [1] citation.",
                    "content_type": "text",
                    "sources": [
                        {
                            "url": "https://verifiabl.dev/source1",
                            "title": "Source 1",
                            "snippets": ["Relevant excerpt."],
                        }
                    ],
                },
            }
        )

    @route("GET", "/images", writes=False)
    async def images(self, request, **kw):
        return MockResponse(
            body={
                "images": {
                    "results": [
                        {
                            "title": "Mock Image",
                            "page_url": "https://verifiabl.dev/img",
                            "image_url": "https://verifiabl.dev/img/1.jpg",
                        }
                    ]
                },
                "metadata": {"query": "test", "search_uuid": "you_img_mock_001"},
            }
        )

    @route("GET", "/livenews", writes=False)
    async def livenews(self, request, **kw):
        return MockResponse(
            body={
                "news": {
                    "query": {"original": "news query", "spellcheck_off": False},
                    "results": [
                        {
                            "title": "Mock News Article",
                            "url": "https://verifiabl.dev/news/1",
                            "description": "Summary.",
                            "source_name": "Mock News",
                            "page_age": "2026-03-14T12:00:00Z",
                            "age": "2 hours ago",
                            "thumbnail": {"src": "https://verifiabl.dev/thumb.jpg"},
                        },
                    ],
                    "metadata": {"request_uuid": "you_news_mock_001"},
                },
            }
        )
