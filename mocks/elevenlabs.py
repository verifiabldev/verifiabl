# CHANGELOG: https://elevenlabs.io/docs/changelog (no RSS/atom feed as of 2026-03)
# SPEC:      https://elevenlabs.io/docs/api-reference/introduction
# SANDBOX:   https://elevenlabs.io
# SKILL:     —
# MCP:       —
# LLMS:      https://elevenlabs.io/docs/llms.txt
from mocks.base import BaseMock, route
from models import MockResponse


def _voice(voice_id: str = "voice_mock_001", name: str = "Mock Voice"):
    return {
        "voice_id": voice_id,
        "name": name,
        "category": "generated",
        "labels": {},
        "description": "",
        "preview_url": "https://storage.elevenlabs.io/mock_preview.mp3",
        "available_for_tiers": ["free", "starter"],
        "settings": {"stability": 0.5, "similarity_boost": 0.75},
        "samples": [
            {
                "sample_id": "samp_mock_001",
                "file_name": "sample.mp3",
                "mime_type": "audio/mpeg",
                "size_bytes": 1024,
                "hash": "mock_hash",
            }
        ],
        "fine_tuning": {
            "model_id": "eleven_multilingual_v2",
            "is_allowed_to_fine_tune": False,
            "fine_tuning_requested": False,
            "finetuning_state": "not_started",
            "verification_attempts": [],
            "verification_failures": [],
            "verification_attempts_count": 0,
            "slice_ids": [],
        },
    }


def _history_item(history_item_id: str = "hist_mock_001"):
    return {
        "history_item_id": history_item_id,
        "request_id": "req_mock_verifiabl",
        "voice_id": "voice_mock_001",
        "voice_name": "Mock Voice",
        "text": "Hello world.",
        "date_unix": 1710400000,
        "character_count_change_from": 0,
        "character_count_change_to": 12,
        "content_type": "audio/mpeg",
        "state": "created",
        "settings": {},
        "feedback": {
            "thumbs_up": True,
            "feedback": "",
            "emotions": False,
            "inaccurate_clone": False,
            "glitches": False,
            "audio_quality": False,
            "other": False,
        },
    }


class ElevenlabsMock(BaseMock):
    prefix = "/elevenlabs"
    spec_url = "https://elevenlabs.io/docs/api-reference/introduction"
    sandbox_base = "https://api.elevenlabs.io"

    @route("GET", "/v1/voices", writes=False)
    async def list_voices(self, request, **kw):
        return MockResponse(
            body={
                "voices": [
                    _voice("voice_mock_001", "Mock Voice"),
                    _voice("voice_mock_002", "Mock Voice Two"),
                ]
            }
        )

    @route("GET", "/v1/voices/{voice_id}", writes=False)
    async def get_voice(self, request, voice_id="", **kw):
        return MockResponse(body=_voice(voice_id or "voice_mock_001"))

    @route("GET", "/v1/voices/settings/default", writes=False)
    async def default_voice_settings(self, request, **kw):
        return MockResponse(body={"stability": 0.5, "similarity_boost": 0.75})

    @route("GET", "/v1/voices/{voice_id}/settings", writes=False)
    async def get_voice_settings(self, request, voice_id="", **kw):
        return MockResponse(body={"stability": 0.5, "similarity_boost": 0.75})

    @route("GET", "/v1/user", writes=False)
    async def get_user(self, request, **kw):
        return MockResponse(
            body={
                "xi_api_key": "mock_key_verifiabl",
                "is_new_user": False,
                "subscription": {
                    "tier": "free",
                    "character_count": 1000,
                    "character_limit": 10000,
                    "can_extend_character_limit": False,
                    "allowed_to_extend_character_limit": False,
                    "next_character_count_reset_unix": 1710486400,
                    "voice_limit": 3,
                    "professional_voice_limit": 1,
                    "can_extend_voice_limit": False,
                    "can_use_instant_voice_cloning": True,
                    "can_use_professional_voice_cloning": False,
                    "can_use_delayed_payment_methods": False,
                    "currency": "usd",
                    "status": "active",
                    "available_models": [
                        {
                            "model_id": "eleven_multilingual_v2",
                            "display_name": "Eleven Multilingual v2",
                            "supported_language": [{"iso_code": "en", "display_name": "English"}],
                        }
                    ],
                },
            }
        )

    @route("GET", "/v1/user/subscription", writes=False)
    async def get_subscription(self, request, **kw):
        return MockResponse(
            body={
                "tier": "free",
                "character_count": 1000,
                "character_limit": 10000,
                "can_extend_character_limit": False,
                "allowed_to_extend_character_limit": False,
                "next_character_count_reset_unix": 1710486400,
                "voice_limit": 3,
                "professional_voice_limit": 1,
                "can_extend_voice_limit": False,
                "can_use_instant_voice_cloning": True,
                "can_use_professional_voice_cloning": False,
                "can_use_delayed_payment_methods": False,
                "currency": "usd",
                "status": "active",
                "next_invoice": {"amount_due_cents": 0, "next_payment_attempt_unix": 1710486400},
                "available_models": [
                    {
                        "model_id": "eleven_multilingual_v2",
                        "display_name": "Eleven Multilingual v2",
                        "supported_language": [{"iso_code": "en", "display_name": "English"}],
                    }
                ],
            }
        )

    @route("GET", "/v1/history", writes=False)
    async def list_history(self, request, **kw):
        return MockResponse(
            body={"history": [_history_item("hist_mock_001"), _history_item("hist_mock_002")]}
        )

    @route("POST", "/v1/text-to-speech/{voice_id}")
    async def text_to_speech(self, request, voice_id="", **kw):
        return MockResponse(status=200, body={})

    @route("POST", "/v1/voices/add")
    async def add_voice(self, request, **kw):
        return MockResponse(status=200, body={"voice_id": "voice_mock_new"})

    @route("DELETE", "/v1/voices/{voice_id}")
    async def delete_voice(self, request, voice_id="", **kw):
        return MockResponse(status=200, body={})

    @route("DELETE", "/v1/history/{history_item_id}")
    async def delete_history_item(self, request, history_item_id="", **kw):
        return MockResponse(status=200, body={})
