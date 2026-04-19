# CHANGELOG: https://help.otter.ai (no RSS/atom feed as of 2026-03)
# SPEC:      https://help.otter.ai (REST ref; no public OpenAPI — mock inferred)
# SANDBOX:   https://api.otter.ai (OAuth token from account manager)
# SKILL:     —
# MCP:       —
# LLMS:      —
# AUTH:      Bearer token in Authorization header (OAuth 2.0 client credentials)
from mocks.base import BaseMock, route
from models import MockResponse


# LOC EXCEPTION: 9 endpoints for meetings, transcript, summary, action_items, highlights exceed 80 LOC.
class OtterMock(BaseMock):
    prefix = "/otter"
    spec_url = "https://help.otter.ai"
    sandbox_base = "https://api.otter.ai"

    @route("GET", "/v1/meetings", writes=False)
    async def list_meetings(self, request, **kw):
        return MockResponse(
            body={
                "meetings": [
                    {
                        "id": "meet_mock_verifiabl_001",
                        "title": "Q1 Planning",
                        "start_time": 1710400000,
                        "duration_seconds": 3600,
                        "participant_count": 4,
                    },
                    {
                        "id": "meet_mock_verifiabl_002",
                        "title": "Standup",
                        "start_time": 1710486400,
                        "duration_seconds": 900,
                        "participant_count": 6,
                    },
                ],
                "next_cursor": None,
            }
        )

    @route("POST", "/v1/meetings")
    async def create_meeting(self, request, **kw):
        return MockResponse(
            status=201,
            body={
                "id": "meet_mock_verifiabl_new",
                "title": "New Meeting",
                "start_time": 1710400000,
                "duration_seconds": 0,
                "participant_count": 0,
            },
        )

    @route("GET", "/v1/meetings/{id}", writes=False)
    async def get_meeting(self, request, id="", **kw):
        mid = id or "meet_mock_verifiabl_001"
        return MockResponse(
            body={
                "id": mid,
                "title": "Q1 Planning",
                "start_time": 1710400000,
                "duration_seconds": 3600,
                "participant_count": 4,
                "created_at": "2024-03-14T12:00:00Z",
            }
        )

    @route("PATCH", "/v1/meetings/{id}")
    async def update_meeting(self, request, id="", **kw):
        return MockResponse(
            body={
                "id": id or "meet_mock_verifiabl_001",
                "title": "Updated Title",
                "start_time": 1710400000,
                "duration_seconds": 3600,
                "participant_count": 4,
            }
        )

    @route("DELETE", "/v1/meetings/{id}")
    async def delete_meeting(self, request, id="", **kw):
        return MockResponse(body={"deleted": True, "id": id or "meet_mock_verifiabl_001"})

    @route("GET", "/v1/meetings/{id}/transcript", writes=False)
    async def get_transcript(self, request, id="", **kw):
        mid = id or "meet_mock_verifiabl_001"
        return MockResponse(
            body={
                "meeting_id": mid,
                "utterances": [
                    {
                        "speaker_id": "spk_1",
                        "text": "Welcome to the call.",
                        "start_ms": 0,
                        "end_ms": 1200,
                    },
                    {
                        "speaker_id": "spk_2",
                        "text": "Thanks. Let's review the roadmap.",
                        "start_ms": 1500,
                        "end_ms": 4200,
                    },
                ],
            }
        )

    @route("GET", "/v1/meetings/{id}/summary", writes=False)
    async def get_summary(self, request, id="", **kw):
        mid = id or "meet_mock_verifiabl_001"
        return MockResponse(
            body={
                "meeting_id": mid,
                "summary": "The team discussed Q1 goals and next steps.",
                "topics": ["Q1 planning", "roadmap", "priorities"],
            }
        )

    @route("GET", "/v1/meetings/{id}/action_items", writes=False)
    async def get_action_items(self, request, id="", **kw):
        mid = id or "meet_mock_verifiabl_001"
        return MockResponse(
            body={
                "meeting_id": mid,
                "action_items": [
                    {"text": "Send follow-up deck by Friday", "assignee": None, "due": None},
                    {"text": "Schedule design review", "assignee": None, "due": None},
                ],
            }
        )

    @route("GET", "/v1/meetings/{id}/highlights", writes=False)
    async def get_highlights(self, request, id="", **kw):
        mid = id or "meet_mock_verifiabl_001"
        return MockResponse(
            body={
                "meeting_id": mid,
                "highlights": [
                    {
                        "text": "Launch target set for March 30.",
                        "start_ms": 120000,
                        "end_ms": 125000,
                    },
                ],
            }
        )
