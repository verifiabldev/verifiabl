# CHANGELOG: https://serpapi.com/blog/tag/changelog/ (no RSS/atom feed as of 2026-03)
# SPEC:      https://serpapi.com/search-api (REST ref, no OpenAPI)
# SANDBOX:   https://serpapi.com/dashboard
# SKILL:     —
# MCP:       —
# LLMS:      —
from mocks.base import BaseMock, route
from models import MockResponse


class SerpapiMock(BaseMock):
    prefix = "/serpapi"
    spec_url = "https://serpapi.com/search-api"
    sandbox_base = "https://serpapi.com"

    @route("GET", "/search", writes=False)
    async def search(self, request, **kw):
        return MockResponse(body=self._search_body())

    @route("GET", "/search.json", writes=False)
    async def search_json(self, request, **kw):
        return MockResponse(body=self._search_body())

    def _search_body(self):
        return {
            "search_metadata": {
                "id": "serp_mock_verifiabl_001",
                "status": "Success",
                "created_at": "2026-03-14 12:00:00 UTC",
                "processed_at": "2026-03-14 12:00:00 UTC",
                "total_time_taken": 1.0,
            },
            "search_parameters": {"engine": "google", "q": "coffee", "device": "desktop"},
            "search_information": {
                "organic_results_state": "Results for exact spelling",
                "query_displayed": "coffee",
                "total_results": 1340000000,
            },
            "organic_results": [
                {
                    "position": 1,
                    "title": "Coffee - Wikipedia",
                    "link": "https://en.wikipedia.org/wiki/Coffee",
                    "snippet": "Coffee is a brewed drink...",
                },
                {
                    "position": 2,
                    "title": "Coffee Recipes",
                    "link": "https://verifiabl.dev/coffee",
                    "snippet": "Best coffee recipes.",
                },
            ],
        }

    @route("GET", "/locations.json", writes=False)
    async def locations(self, request, **kw):
        return MockResponse(
            body=[
                {
                    "id": "585069b8ee19ad271e9ba949",
                    "name": "Austin",
                    "canonical_name": "Austin,Texas,United States",
                    "country_code": "US",
                    "target_type": "City",
                    "reach": 4870000,
                    "gps": [-97.7430608, 30.267153],
                },
                {
                    "id": "585069bdee19ad271e9bc072",
                    "name": "Austin, TX",
                    "canonical_name": "Austin, TX,Texas,United States",
                    "country_code": "US",
                    "target_type": "DMA Region",
                    "reach": 5560000,
                    "gps": [-97.7430608, 30.267153],
                },
            ]
        )

    @route("GET", "/account", writes=False)
    async def account(self, request, **kw):
        return MockResponse(body=self._account_body())

    @route("GET", "/account.json", writes=False)
    async def account_json(self, request, **kw):
        return MockResponse(body=self._account_body())

    def _account_body(self):
        return {
            "account_id": "serp_mock_account_001",
            "account_email": "demo@serpapi.com",
            "plan_id": "bigdata",
            "plan_name": "Big Data Plan",
            "searches_per_month": 30000,
            "plan_searches_left": 5958,
            "this_month_usage": 24042,
            "last_hour_searches": 42,
            "account_rate_limit_per_hour": 6000,
        }

    @route("GET", "/searches/{search_id}", writes=False)
    async def search_archive(self, request, search_id="", **kw):
        body = self._search_body()
        body["search_metadata"]["id"] = search_id or "serp_mock_verifiabl_001"
        return MockResponse(body=body)
