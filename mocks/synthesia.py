# CHANGELOG: https://synthesia.noticeable.news/api.rss
# SPEC:      https://docs.synthesia.io/reference/introduction
# SANDBOX:   https://app.synthesia.io
# SKILL:     —
# MCP:       —
# LLMS:      —
# AUTH:      API key in Authorization header (per OpenAPI securitySchemes)
from typing import Optional

from mocks.base import BaseMock, route
from models import MockResponse


def _video(
    id_: str = "video_mock_verifiabl",
    status: str = "complete",
    created_at: int = 1710400000,
    last_updated_at: Optional[int] = 1710400060,
    title: str = "",
    description: str = "",
    visibility: str = "private",
    download: Optional[str] = None,
    duration: Optional[str] = None,
    thumbnail: Optional[dict] = None,
):
    return {
        "id": id_,
        "status": status,
        "createdAt": created_at,
        "lastUpdatedAt": last_updated_at,
        "title": title,
        "description": description,
        "visibility": visibility,
        "download": download,
        "duration": duration,
        "thumbnail": thumbnail or {"image": None, "gif": None},
        "test": False,
        "callbackId": None,
    }


def _template(
    id_: str = "tpl_mock_verifiabl",
    template_id: str = "tpl_mock_verifiabl",
    created_at: int = 1710400000,
    last_updated_at: Optional[int] = 1710400060,
    title: str = "Mock Template",
    variables: Optional[list] = None,
):
    return {
        "id": id_,
        "templateId": template_id,
        "createdAt": created_at,
        "lastUpdatedAt": last_updated_at,
        "title": title,
        "description": "",
        "visibility": "private",
        "variables": variables or [{"name": "name", "variableId": "var_001"}],
        "templateData": {},
    }


# LOC EXCEPTION: Schema-faithful VideoResponse/TemplateResponse and list envelopes require helpers and multi-field bodies for agent testing.
class SynthesiaMock(BaseMock):
    prefix = "/synthesia"
    spec_url = "https://docs.synthesia.io/reference/introduction"
    sandbox_base = "https://api.synthesia.io"

    @route("GET", "/v2/videos", writes=False)
    async def list_videos(self, request, **kw):
        return MockResponse(
            body={
                "videos": [
                    _video(
                        "video_mock_001",
                        "complete",
                        1710400000,
                        1710400060,
                        "Welcome",
                        "",
                        "private",
                        "https://cdn.synthesia.io/v/001.mp4",
                        "0:45",
                    ),
                    _video(
                        "video_mock_002",
                        "in_progress",
                        1710400100,
                        None,
                        "",
                        "",
                        "private",
                        None,
                        None,
                    ),
                ],
                "nextOffset": 2,
            }
        )

    @route("POST", "/v2/videos")
    async def create_video(self, request, **kw):
        return MockResponse(body=_video("video_mock_new", "in_progress", 1710400200, None))

    @route("GET", "/v2/videos/{video_id}", writes=False)
    async def get_video(self, request, video_id="", **kw):
        return MockResponse(body=_video(video_id or "video_mock_verifiabl"))

    @route("PATCH", "/v2/videos/{video_id}")
    async def update_video(self, request, video_id="", **kw):
        return MockResponse(body=_video(video_id or "video_mock_verifiabl", "complete"))

    @route("DELETE", "/v2/videos/{video_id}")
    async def delete_video(self, request, video_id="", **kw):
        return MockResponse(status=204)

    @route("POST", "/v2/videos/fromTemplate")
    async def create_video_from_template(self, request, **kw):
        return MockResponse(
            status=201, body=_video("video_mock_from_tpl", "in_progress", 1710400300, None)
        )

    @route("GET", "/v2/templates", writes=False)
    async def list_templates(self, request, **kw):
        return MockResponse(
            body={
                "templates": [
                    _template("tpl_mock_001", "tpl_mock_001", 1710400000, 1710400000, "Onboarding"),
                    _template(
                        "tpl_mock_002", "tpl_mock_002", 1710400100, 1710400100, "Product Demo"
                    ),
                ],
                "nextOffset": 2,
            }
        )

    @route("GET", "/v2/templates/{template_id}", writes=False)
    async def get_template(self, request, template_id="", **kw):
        return MockResponse(
            body=_template(template_id or "tpl_mock_verifiabl", template_id or "tpl_mock_verifiabl")
        )
