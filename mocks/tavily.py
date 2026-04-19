# CHANGELOG: https://docs.tavily.com/changelog  (no RSS/atom feed as of 2026-03)
# SPEC:      https://docs.tavily.com/documentation/api-reference/openapi.json
# SANDBOX:   https://app.tavily.com
# SKILL:     —
# MCP:       —
# LLMS:      —
from mocks.base import BaseMock, route
from models import MockResponse


class TavilyMock(BaseMock):
    prefix = "/tavily"
    spec_url = "https://docs.tavily.com/documentation/api-reference/openapi.json"
    sandbox_base = "https://api.tavily.com"

    @route("POST", "/search", writes=False)
    async def search(self, request, **kw):
        return MockResponse(
            body={
                "query": "who is Leo Messi?",
                "results": [
                    {
                        "title": "Lionel Messi Facts | Britannica",
                        "url": "https://www.britannica.com/facts/Lionel-Messi",
                        "content": "Lionel Messi, an Argentine footballer, is widely regarded as one of the greatest players of his generation.",
                        "score": 0.81,
                    },
                    {
                        "title": "Lionel Messi - Wikipedia",
                        "url": "https://en.wikipedia.org/wiki/Lionel_Messi",
                        "content": "Lionel Andrés Messi is an Argentine professional footballer who plays as a forward.",
                        "score": 0.79,
                    },
                ],
                "images": [],
                "response_time": 1.67,
                "answer": "Lionel Messi, born in 1987, is an Argentine footballer widely regarded as one of the greatest players of his generation.",
                "request_id": "123e4567-e89b-12d3-a456-426614174111",
            }
        )

    @route("GET", "/usage", writes=False)
    async def get_usage(self, request, **kw):
        return MockResponse(
            body={
                "key": {
                    "usage": 150,
                    "limit": 1000,
                    "search_usage": 100,
                    "extract_usage": 25,
                    "crawl_usage": 15,
                    "map_usage": 7,
                    "research_usage": 3,
                },
                "account": {
                    "current_plan": "Bootstrap",
                    "plan_usage": 500,
                    "plan_limit": 15000,
                    "paygo_usage": 25,
                    "paygo_limit": 100,
                    "search_usage": 350,
                    "extract_usage": 75,
                    "crawl_usage": 50,
                    "map_usage": 15,
                    "research_usage": 10,
                },
            }
        )

    @route("POST", "/extract", writes=False)
    async def extract(self, request, **kw):
        return MockResponse(
            body={
                "results": [
                    {
                        "url": "https://en.wikipedia.org/wiki/Artificial_intelligence",
                        "raw_content": "Artificial intelligence (AI), in its broadest sense, is intelligence exhibited by machines.",
                        "images": [],
                        "favicon": "https://en.wikipedia.org/static/favicon/wikipedia.ico",
                    },
                ],
                "failed_results": [],
                "response_time": 0.02,
                "request_id": "123e4567-e89b-12d3-a456-426614174111",
            }
        )

    @route("POST", "/crawl", writes=False)
    async def crawl(self, request, **kw):
        return MockResponse(
            body={
                "request_id": "crawl_mock_verifiabl",
                "response_time": 2.1,
                "results": [
                    {
                        "url": "https://verifiabl.dev",
                        "raw_content": "Mock extracted content.",
                        "title": "Example",
                    }
                ],
            }
        )

    @route("POST", "/map", writes=False)
    async def map(self, request, **kw):
        return MockResponse(
            body={
                "request_id": "map_mock_verifiabl",
                "response_time": 1.5,
                "urls": ["https://verifiabl.dev", "https://verifiabl.dev/about"],
            }
        )

    @route("POST", "/research", writes=False)
    async def create_research(self, request, **kw):
        return MockResponse(
            status=201,
            body={
                "request_id": "research_mock_verifiabl",
                "status": "pending",
            },
        )
