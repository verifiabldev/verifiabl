# CHANGELOG: https://buildwithfern.com/learn/docs/changelog (no RSS/atom feed as of 2026-03)
# SPEC:      https://buildwithfern.com/learn/docs/ai-features/ask-fern/api-reference/overview
# SANDBOX:   https://app.buildwithfern.com
# SKILL:     —
# MCP:       —
# LLMS:      https://buildwithfern.com/learn/docs/llms.txt
from mocks.base import BaseMock, route
from models import MockResponse


class FernMock(BaseMock):
    prefix = "/fern"
    spec_url = "https://buildwithfern.com/learn/docs/ai-features/ask-fern/api-reference/overview"
    sandbox_base = "https://fai.buildwithfern.com"

    @route("GET", "/conversation/{domain}/{conversation_id}", writes=False)
    async def get_conversation(self, request, domain="", conversation_id="", **kw):
        return MockResponse(
            body={
                "conversation": {
                    "conversation_id": conversation_id or "conv_mock_verifiabl",
                    "created_at": "2026-03-14T12:00:00.000Z",
                    "turns": [
                        {
                            "role": "user",
                            "text": "How do I get started?",
                            "created_at": "2026-03-14T12:00:00.000Z",
                            "feedback": None,
                        },
                        {
                            "role": "assistant",
                            "text": "See the quickstart guide.",
                            "created_at": "2026-03-14T12:00:01.000Z",
                            "feedback": {"is_helpful": True, "feedback_message": None},
                        },
                    ],
                },
            }
        )

    @route("GET", "/queries/{domain}", writes=False)
    async def get_queries(self, request, domain="", **kw):
        return MockResponse(
            body={
                "queries": [
                    {
                        "query_id": "q_mock_001",
                        "conversation_id": "conv_mock_001",
                        "domain": domain or "docs",
                        "text": "How do I authenticate?",
                        "role": "user",
                        "source": "widget",
                        "created_at": "2026-03-14T12:00:00.000Z",
                        "time_to_first_token": 0.5,
                        "subqueries": None,
                    },
                ],
                "pagination": {"total": 1, "page": 1, "limit": 100},
            }
        )

    @route("GET", "/sources/website/{domain}", writes=False)
    async def get_websites(self, request, domain="", **kw):
        return MockResponse(
            body={
                "websites": [
                    {
                        "website_id": "web_mock_001",
                        "domain": domain or "docs",
                        "base_url": "https://docs.verifiabl.dev",
                        "page_url": "https://docs.verifiabl.dev/intro",
                        "chunk": "Get started with the API.",
                        "document": "intro",
                        "title": "Introduction",
                        "version": None,
                        "product": None,
                        "keywords": None,
                        "authed": None,
                        "created_at": "2026-03-14T12:00:00.000Z",
                        "updated_at": "2026-03-14T12:00:00.000Z",
                    },
                ],
                "pagination": {"total": 1, "page": 1, "limit": 100},
            }
        )

    @route("GET", "/sources/website/{domain}/status", writes=False)
    async def get_website_status(self, request, domain="", **kw):
        return MockResponse(
            body={
                "job_id": "job_mock_verifiabl",
                "status": "COMPLETED",
                "base_url": "https://docs.verifiabl.dev",
                "pages_indexed": 42,
                "pages_failed": 0,
                "error": None,
            }
        )

    @route("POST", "/chat/{domain}")
    async def post_chat_completion(self, request, domain="", **kw):
        return MockResponse(
            body={
                "turns": [{"role": "assistant", "content": "See the quickstart guide for setup."}],
                "citations": ["https://docs.verifiabl.dev/quickstart"],
            }
        )

    @route("POST", "/sources/website/{domain}/index")
    async def index_website(self, request, domain="", **kw):
        return MockResponse(
            body={"job_id": "job_mock_new", "base_url": "https://docs.verifiabl.dev"}
        )
