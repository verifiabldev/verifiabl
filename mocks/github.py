# CHANGELOG: https://github.blog/changelog/feed
# SKILL:     —
# MCP:       https://api.githubcopilot.com/mcp/
# LLMS:      —
from mocks.base import BaseMock, route
from models import MockResponse


class GitHubMock(BaseMock):
    prefix = "/github"
    spec_url = "https://github.com/github/rest-api-description"
    sandbox_base = "https://api.github.com"

    @route("GET", "/user")
    async def get_user(self, request, **kw):
        return MockResponse(body={"login": "mockuser", "id": 1, "type": "User"})

    @route("GET", "/repos/{owner}/{repo}")
    async def get_repo(self, request, owner="", repo="", **kw):
        return MockResponse(
            body={"full_name": f"{owner}/{repo}", "private": False, "default_branch": "main"}
        )

    @route("GET", "/repos/{owner}/{repo}/issues")
    async def list_issues(self, request, owner="", repo="", **kw):
        return MockResponse(body=[{"number": 1, "title": "Mock issue", "state": "open"}])

    @route("POST", "/repos/{owner}/{repo}/issues")
    async def create_issue(self, request, owner="", repo="", **kw):
        return MockResponse(status=201, body={"number": 42, "title": "New issue", "state": "open"})
