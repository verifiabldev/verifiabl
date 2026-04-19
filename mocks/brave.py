# CHANGELOG: https://api-dashboard.search.brave.com/documentation (no RSS/atom feed as of 2026-03)
# SPEC:      https://brave.com/search/api
# SANDBOX:   https://api-dashboard.search.brave.com/app/plans
# SKILL:     —
# MCP:       —
# LLMS:      —
from mocks.base import BaseMock, route
from models import MockResponse


class BraveMock(BaseMock):
    prefix = "/brave"
    spec_url = "https://brave.com/search/api"
    sandbox_base = "https://api.search.brave.com"

    @route("GET", "/res/v1/web/search", writes=False)
    async def web_search(self, request, **kw):
        return MockResponse(
            body={
                "type": "search",
                "query": {"original": "greek restaurants"},
                "web": {
                    "type": "search",
                    "results": [
                        {
                            "title": "Best Greek Restaurants",
                            "url": "https://verifiabl.dev/greek",
                            "description": "Top Greek spots.",
                            "is_source_local": False,
                            "is_source_both": False,
                        },
                        {
                            "title": "Greek Food Guide",
                            "url": "https://verifiabl.dev/guide",
                            "description": "A guide to Greek cuisine.",
                            "is_source_local": False,
                            "is_source_both": False,
                        },
                    ],
                },
            }
        )

    @route("GET", "/res/v1/llm/context", writes=False)
    async def llm_context(self, request, **kw):
        return MockResponse(
            body={
                "grounding": {
                    "generic": [
                        {
                            "url": "https://verifiabl.dev/doc",
                            "title": "Example Doc",
                            "snippets": ["Snippet text."],
                        }
                    ]
                },
                "sources": {
                    "https://verifiabl.dev/doc": {
                        "title": "Example Doc",
                        "hostname": "verifiabl.dev",
                        "age": ["2026-03-14", "1 day ago"],
                    }
                },
            }
        )

    @route("GET", "/res/v1/images/search", writes=False)
    async def images_search(self, request, **kw):
        return MockResponse(
            body={
                "type": "images",
                "query": {
                    "original": "munich",
                    "spellcheck_off": False,
                    "show_strict_warning": False,
                },
                "results": [
                    {
                        "type": "image_result",
                        "title": "Munich Photo",
                        "url": "https://verifiabl.dev/img1",
                        "source": "verifiabl.dev",
                        "page_fetched": "2026-03-14T12:00:00Z",
                        "thumbnail": {"src": "https://imgs.search.brave.com/mock"},
                        "confidence": "high",
                    },
                ],
            }
        )

    @route("GET", "/res/v1/videos/search", writes=False)
    async def videos_search(self, request, **kw):
        return MockResponse(
            body={
                "type": "videos",
                "query": {"original": "tutorial", "spellcheck_off": False},
                "results": [
                    {
                        "type": "video_result",
                        "title": "Tutorial Video",
                        "url": "https://verifiabl.dev/vid1",
                        "description": "A short clip.",
                        "thumbnail": {"src": "https://imgs.search.brave.com/mock"},
                    }
                ],
            }
        )

    @route("GET", "/res/v1/news/search", writes=False)
    async def news_search(self, request, **kw):
        return MockResponse(
            body={
                "type": "news",
                "query": {
                    "original": "munich",
                    "spellcheck_off": False,
                    "show_strict_warning": False,
                },
                "results": [
                    {
                        "type": "news_result",
                        "title": "News Headline",
                        "url": "https://verifiabl.dev/news/1",
                        "description": "Brief.",
                        "age": "1 day ago",
                        "page_age": "2026-03-14T12:00:00",
                    }
                ],
            }
        )

    @route("GET", "/res/v1/suggest/search", writes=False)
    async def suggest_search(self, request, **kw):
        return MockResponse(
            body={
                "type": "suggest",
                "query": {"original": "hello"},
                "results": [{"query": "hello"}, {"query": "hello world"}, {"query": "hellofresh"}],
            }
        )

    @route("GET", "/res/v1/spellcheck/search", writes=False)
    async def spellcheck_search(self, request, **kw):
        return MockResponse(
            body={
                "type": "spellcheck",
                "query": {"original": "hellop"},
                "results": [{"query": "hello"}],
            }
        )

    @route("POST", "/res/v1/chat/completions", writes=False)
    async def chat_completions(self, request, **kw):
        return MockResponse(
            body={
                "id": "brave_mock_verifiabl_001",
                "object": "chat.completion",
                "created": 1710400000,
                "model": "brave-pro",
                "choices": [
                    {
                        "index": 0,
                        "message": {
                            "role": "assistant",
                            "content": "Mock answer from Brave Search API.",
                        },
                        "finish_reason": "stop",
                    }
                ],
                "usage": {"prompt_tokens": 10, "completion_tokens": 8, "total_tokens": 18},
            }
        )
