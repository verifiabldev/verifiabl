# CHANGELOG: https://www.assemblyai.com/changelog (no RSS/atom feed as of 2026-03)
# SPEC:      https://github.com/AssemblyAI/assemblyai-api-spec/blob/main/openapi.yml
# SANDBOX:   https://www.assemblyai.com/app/account
# SKILL:     —
# MCP:       —
# LLMS:      —
from mocks.base import BaseMock, route
from models import MockResponse


class AssemblyaiMock(BaseMock):
    prefix = "/assemblyai"
    spec_url = "https://github.com/AssemblyAI/assemblyai-api-spec/blob/main/openapi.yml"
    sandbox_base = "https://api.assemblyai.com"

    @route("GET", "/v2/transcript", writes=False)
    async def list_transcripts(self, request, **kw):
        return MockResponse(
            body={
                "page_details": {
                    "limit": 10,
                    "result_count": 2,
                    "current_url": "https://api.assemblyai.com/v2/transcript?limit=10",
                    "prev_url": None,
                    "next_url": None,
                },
                "transcripts": [
                    {
                        "id": "tra_mock_verifiabl_001",
                        "resource_url": "https://api.assemblyai.com/v2/transcript/tra_mock_verifiabl_001",
                        "status": "completed",
                        "created": "2024-03-11T21:29:59.936851",
                        "completed": "2024-03-11T21:30:07.314223",
                        "audio_url": "https://verifiabl.dev/audio.mp3",
                        "error": None,
                    },
                    {
                        "id": "tra_mock_verifiabl_002",
                        "resource_url": "https://api.assemblyai.com/v2/transcript/tra_mock_verifiabl_002",
                        "status": "completed",
                        "created": "2024-03-11T21:12:57.372215",
                        "completed": "2024-03-11T21:13:03.267020",
                        "audio_url": "https://verifiabl.dev/other.mp3",
                        "error": None,
                    },
                ],
            }
        )

    @route("POST", "/v2/transcript")
    async def create_transcript(self, request, **kw):
        return MockResponse(
            body={
                "id": "tra_mock_verifiabl_new",
                "status": "queued",
                "audio_url": "https://verifiabl.dev/uploaded.mp3",
                "created": "2024-03-11T22:00:00.000000",
                "completed": None,
                "error": None,
                "text": None,
            }
        )

    @route("GET", "/v2/transcript/{transcript_id}", writes=False)
    async def get_transcript(self, request, transcript_id="", **kw):
        tid = transcript_id or "tra_mock_verifiabl_001"
        return MockResponse(
            body={
                "id": tid,
                "status": "completed",
                "audio_url": "https://verifiabl.dev/audio.mp3",
                "created": "2024-03-11T21:29:59.936851",
                "completed": "2024-03-11T21:30:07.314223",
                "error": None,
                "text": "Hello world. This is a mock transcript.",
                "confidence": 0.95,
                "audio_duration": 12,
            }
        )

    @route("DELETE", "/v2/transcript/{transcript_id}")
    async def delete_transcript(self, request, transcript_id="", **kw):
        return MockResponse(
            body={
                "id": transcript_id or "tra_mock_verifiabl_001",
                "status": "completed",
                "error": None,
            }
        )

    @route("POST", "/v2/upload")
    async def upload_file(self, request, **kw):
        return MockResponse(
            body={"upload_url": "https://cdn.assemblyai.com/upload/mock_verifiabl_upload_id"}
        )

    @route("GET", "/v2/transcript/{transcript_id}/sentences", writes=False)
    async def get_sentences(self, request, transcript_id="", **kw):
        tid = transcript_id or "tra_mock_verifiabl_001"
        return MockResponse(
            body={
                "id": tid,
                "confidence": 0.95,
                "audio_duration": 12,
                "sentences": [
                    {
                        "text": "Hello world.",
                        "start": 0,
                        "end": 800,
                        "confidence": 0.96,
                        "words": [
                            {
                                "text": "Hello",
                                "start": 0,
                                "end": 400,
                                "confidence": 0.97,
                                "speaker": None,
                            },
                            {
                                "text": "world.",
                                "start": 420,
                                "end": 800,
                                "confidence": 0.95,
                                "speaker": None,
                            },
                        ],
                        "speaker": None,
                    },
                    {
                        "text": "This is a mock transcript.",
                        "start": 850,
                        "end": 2500,
                        "confidence": 0.94,
                        "words": [],
                        "speaker": None,
                    },
                ],
            }
        )

    @route("GET", "/v2/transcript/{transcript_id}/paragraphs", writes=False)
    async def get_paragraphs(self, request, transcript_id="", **kw):
        tid = transcript_id or "tra_mock_verifiabl_001"
        return MockResponse(
            body={
                "id": tid,
                "confidence": 0.95,
                "audio_duration": 12,
                "paragraphs": [
                    {
                        "text": "Hello world. This is a mock transcript.",
                        "start": 0,
                        "end": 2500,
                        "confidence": 0.95,
                        "words": [
                            {
                                "text": "Hello",
                                "start": 0,
                                "end": 400,
                                "confidence": 0.97,
                                "speaker": None,
                            },
                            {
                                "text": "world.",
                                "start": 420,
                                "end": 800,
                                "confidence": 0.95,
                                "speaker": None,
                            },
                        ],
                    },
                ],
            }
        )

    @route("GET", "/v2/transcript/{transcript_id}/word-search", writes=False)
    async def word_search(self, request, transcript_id="", **kw):
        tid = transcript_id or "tra_mock_verifiabl_001"
        return MockResponse(
            body={
                "id": tid,
                "total_count": 2,
                "matches": [
                    {"text": "mock", "count": 1, "timestamps": [[850, 1200]], "indexes": [2]},
                    {
                        "text": "transcript",
                        "count": 1,
                        "timestamps": [[1250, 2500]],
                        "indexes": [4],
                    },
                ],
            }
        )
