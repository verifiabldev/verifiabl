# CHANGELOG: https://help.mirage.app/help/docs/api/overview (no RSS/atom feed as of 2026-03)
# SPEC:      https://help.mirage.app/api-reference/videos/create-video
# SANDBOX:   https://platform.mirage.app
# SKILL:     —
# MCP:       —
# LLMS:      —
from typing import Optional

from mocks.base import BaseMock, route
from models import MockResponse


def _video(
    id_: str = "video_mock_verifiabl",
    status: str = "COMPLETE",
    created_at: int = 1710400000,
    completed_at: Optional[int] = 1710400060,
    progress: Optional[int] = 100,
    source_video_id: Optional[str] = None,
    caption_template_id: Optional[str] = None,
):
    return {
        "id": id_,
        "status": status,
        "created_at": created_at,
        "video_id": id_,
        "object": "video",
        "completed_at": completed_at,
        "progress": progress,
        "error": None,
        "model": "mirage-video-1-latest",
        "source_video_id": source_video_id,
        "caption_template_id": caption_template_id,
    }


class MirageMock(BaseMock):
    prefix = "/mirage"
    spec_url = "https://help.mirage.app/api-reference/videos/create-video"
    sandbox_base = "https://api.mirage.app"

    @route("GET", "/v1/videos", writes=False)
    async def list_videos(self, request, **kw):
        return MockResponse(
            body=[
                _video("video_mock_001", "COMPLETE"),
                _video("video_mock_002", "PROCESSING", completed_at=None, progress=45),
            ]
        )

    @route("POST", "/v1/videos")
    async def create_video(self, request, **kw):
        return MockResponse(
            status=201, body=_video("video_mock_new", "PROCESSING", completed_at=None, progress=0)
        )

    @route("GET", "/v1/videos/{video_id}", writes=False)
    async def get_video(self, request, video_id="", **kw):
        return MockResponse(body=_video(video_id or "video_mock_verifiabl"))

    @route("GET", "/v1/videos/{video_id}/content", writes=False)
    async def get_video_content(self, request, video_id="", **kw):
        return MockResponse(
            body={
                "url": f"https://api.mirage.app/v1/videos/{(video_id or 'video_mock_verifiabl')}/content/download",
            }
        )

    @route("GET", "/v1/videos/captions/templates", writes=False)
    async def list_caption_templates(self, request, **kw):
        return MockResponse(
            body={
                "data": [
                    {
                        "id": "ctpl_mock_001",
                        "name": "Default",
                        "created_at": 1710400000,
                        "object": "caption_template",
                        "preview_url": "https://captions-cdn.xyz/preview/001.mp4",
                    },
                    {
                        "id": "ctpl_mock_002",
                        "name": "Minimal",
                        "created_at": 1710400100,
                        "object": "caption_template",
                        "preview_url": "https://captions-cdn.xyz/preview/002.mp4",
                    },
                ],
                "has_more": False,
                "object": "list",
            }
        )

    @route("POST", "/v1/videos/captions")
    async def add_captions(self, request, **kw):
        return MockResponse(
            status=201,
            body=_video(
                "video_mock_captioned",
                "PROCESSING",
                completed_at=None,
                progress=0,
                source_video_id="video_mock_001",
                caption_template_id="ctpl_mock_001",
            ),
        )
