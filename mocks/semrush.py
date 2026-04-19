# CHANGELOG: https://developer.semrush.com/api/ (no RSS/atom feed as of 2026-03)
# SPEC:      https://developer.semrush.com/api/seo/overview-reports/
# SANDBOX:   https://www.semrush.com/accounts/subscription-info/api-units
# SKILL:     —
# MCP:       —
# LLMS:      —
# AUTH:      API key in query parameter `key` (required on every request)
from mocks.base import BaseMock, route
from models import MockResponse


# LOC EXCEPTION: Semrush exposes many report types as distinct logical endpoints; RESTified paths require one handler per report.
class SemrushMock(BaseMock):
    prefix = "/semrush"
    spec_url = "https://developer.semrush.com/api/seo/overview-reports/"
    sandbox_base = "https://api.semrush.com"

    @route("GET", "/domain_ranks", writes=False)
    async def domain_ranks(self, request, **kw):
        return MockResponse(
            body={
                "data": [
                    {
                        "Db": "us",
                        "Dn": "semrush.com",
                        "Rk": 1250,
                        "Or": 420000,
                        "Ot": 1850000,
                        "Oc": 9200000,
                        "Ad": 1200,
                        "At": 45000,
                        "Ac": 180000,
                    },
                    {
                        "Db": "uk",
                        "Dn": "semrush.com",
                        "Rk": 980,
                        "Or": 380000,
                        "Ot": 1620000,
                        "Oc": 8100000,
                        "Ad": 900,
                        "At": 32000,
                        "Ac": 140000,
                    },
                ],
            }
        )

    @route("GET", "/domain_rank", writes=False)
    async def domain_rank(self, request, **kw):
        return MockResponse(
            body={
                "data": [
                    {
                        "Dn": "semrush.com",
                        "Rk": 1250,
                        "Or": 420000,
                        "Ot": 1850000,
                        "Oc": 9200000,
                        "Ad": 1200,
                        "At": 45000,
                        "Ac": 180000,
                    }
                ],
            }
        )

    @route("GET", "/domain_rank_history", writes=False)
    async def domain_rank_history(self, request, **kw):
        return MockResponse(
            body={
                "data": [
                    {
                        "Rk": 1248,
                        "Or": 418000,
                        "Ot": 1842000,
                        "Oc": 9150000,
                        "Ad": 1190,
                        "At": 44800,
                        "Ac": 179200,
                        "Dt": "20250315",
                    },
                    {
                        "Rk": 1252,
                        "Or": 421000,
                        "Ot": 1855000,
                        "Oc": 9220000,
                        "Ad": 1210,
                        "At": 45200,
                        "Ac": 181000,
                        "Dt": "20250215",
                    },
                ],
            }
        )

    @route("GET", "/rank", writes=False)
    async def rank(self, request, **kw):
        return MockResponse(
            body={
                "data": [
                    {
                        "Dn": "wikipedia.org",
                        "Rk": 1,
                        "Or": 83084012,
                        "Ot": 1953530514,
                        "Oc": 1766901500,
                        "Ad": 98,
                        "At": 6375,
                        "Ac": 9285,
                    },
                    {
                        "Dn": "youtube.com",
                        "Rk": 2,
                        "Or": 71381392,
                        "Ot": 874589621,
                        "Oc": 496405761,
                        "Ad": 68366,
                        "At": 63473756,
                        "Ac": 29516519,
                    },
                    {
                        "Dn": "semrush.com",
                        "Rk": 1250,
                        "Or": 420000,
                        "Ot": 1850000,
                        "Oc": 9200000,
                        "Ad": 1200,
                        "At": 45000,
                        "Ac": 180000,
                    },
                ],
            }
        )

    @route("GET", "/rank_difference", writes=False)
    async def rank_difference(self, request, **kw):
        return MockResponse(
            body={
                "data": [
                    {
                        "Dn": "semrush.com",
                        "Rk": 1250,
                        "Or": 420000,
                        "Ot": 1850000,
                        "Oc": 9200000,
                        "Om": 2100,
                        "Tm": 85000,
                        "Um": 4200,
                    },
                    {
                        "Dn": "competitor.com",
                        "Rk": 2100,
                        "Or": 280000,
                        "Ot": 1200000,
                        "Oc": 5800000,
                        "Om": -1200,
                        "Tm": -32000,
                        "Um": -1800,
                    },
                ],
            }
        )

    @route("GET", "/domain_organic", writes=False)
    async def domain_organic(self, request, **kw):
        return MockResponse(
            body={
                "data": [
                    {
                        "keyword": "semrush api",
                        "position": 1,
                        "volume": 8100,
                        "traffic_cost": 42000,
                    },
                    {
                        "keyword": "seo tools",
                        "position": 3,
                        "volume": 135000,
                        "traffic_cost": 680000,
                    },
                ],
            }
        )

    @route("GET", "/backlinks_overview", writes=False)
    async def backlinks_overview(self, request, **kw):
        return MockResponse(
            body={
                "backlinks": 125000,
                "ref_domains": 4200,
                "target": "semrush.com",
            }
        )

    @route("GET", "/keyword_overview", writes=False)
    async def keyword_overview(self, request, **kw):
        return MockResponse(
            body={
                "keyword": "semrush",
                "volume": 135000,
                "keyword_difficulty": 72,
                "cpc": 4.20,
                "data": [
                    {
                        "position": 1,
                        "url": "https://www.semrush.com",
                        "title": "Semrush - SEO Software",
                    },
                    {
                        "position": 2,
                        "url": "https://competitor.com",
                        "title": "Competitor SEO Tool",
                        "domain_rating": 68,
                    },
                ],
            }
        )

    @route("GET", "/organic_positions", writes=False)
    async def organic_positions(self, request, **kw):
        return MockResponse(
            body={
                "data": [
                    {
                        "url": "https://www.semrush.com/blog",
                        "keyword": "seo guide",
                        "position": 2,
                        "volume": 22000,
                    },
                    {
                        "url": "https://www.semrush.com/kb",
                        "keyword": "semrush api",
                        "position": 1,
                        "volume": 8100,
                    },
                ],
            }
        )
