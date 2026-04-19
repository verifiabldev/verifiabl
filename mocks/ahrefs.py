# CHANGELOG: https://ahrefs.com/api/docs/changelog (no RSS/atom feed as of 2026-03)
# SPEC:      https://ahrefs.com/api/documentation
# SANDBOX:   https://ahrefs.com/user-api
# SKILL:     —
# MCP:       —
# LLMS:      —
from mocks.base import BaseMock, route
from models import MockResponse


class AhrefsMock(BaseMock):
    prefix = "/ahrefs"
    spec_url = "https://ahrefs.com/api/documentation"
    sandbox_base = "https://api.ahrefs.com"

    @route("GET", "/v3/site-explorer/domain-rating", writes=False)
    async def domain_rating(self, request, **kw):
        return MockResponse(
            body={
                "domain_rating": 72.0,
                "ahrefs_rank": 125000,
                "ref_domains": 1842,
                "target": "ahrefs.com",
            }
        )

    @route("GET", "/v3/site-explorer/backlinks-stats", writes=False)
    async def backlinks_stats(self, request, **kw):
        return MockResponse(
            body={
                "backlinks": 45200,
                "ref_domains": 1842,
                "ref_ips": 1200,
                "target": "ahrefs.com",
            }
        )

    @route("GET", "/v3/site-explorer/all-backlinks", writes=False)
    async def all_backlinks(self, request, **kw):
        return MockResponse(
            body={
                "backlinks": [
                    {
                        "url_from": "https://verifiabl.dev/page1",
                        "url_to": "https://ahrefs.com/blog",
                        "url_rating_from": 45,
                        "domain_rating_from": 62,
                    },
                    {
                        "url_from": "https://app.verifiabl.dev/post",
                        "url_to": "https://ahrefs.com/docs",
                        "url_rating_from": 38,
                        "domain_rating_from": 55,
                    },
                ],
                "rows_used": 1,
            }
        )

    @route("GET", "/v3/site-explorer/metrics-overview", writes=False)
    async def metrics_overview(self, request, **kw):
        return MockResponse(
            body={
                "domain_rating": 72.0,
                "organic_traffic": 1250000,
                "organic_keywords": 4200,
                "target": "ahrefs.com",
            }
        )

    @route("GET", "/v3/keywords-explorer/overview", writes=False)
    async def keywords_overview(self, request, **kw):
        return MockResponse(
            body={
                "keywords": [
                    {
                        "keyword": "ahrefs",
                        "volume": 135000,
                        "traffic_potential": 82000,
                        "difficulty": 72,
                    },
                    {
                        "keyword": "seo tools",
                        "volume": 90000,
                        "traffic_potential": 45000,
                        "difficulty": 85,
                    },
                ],
                "rows_used": 1,
            }
        )

    @route("GET", "/v3/serp-overview/serp-overview", writes=False)
    async def serp_overview(self, request, **kw):
        return MockResponse(
            body={
                "serp_results": [
                    {
                        "position": 1,
                        "url": "https://ahrefs.com",
                        "title": "Ahrefs - SEO Tool",
                        "domain_rating": 72,
                    },
                    {
                        "position": 2,
                        "url": "https://competitor.com",
                        "title": "Competitor SEO",
                        "domain_rating": 68,
                    },
                ],
                "keyword": "ahrefs",
                "country": "us",
            }
        )
