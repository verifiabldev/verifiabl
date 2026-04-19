# CHANGELOG: https://developer.jamf.com/jamf-pro/docs/ (no RSS/atom feed as of 2026-03)
# SPEC:      https://developer.jamf.com/jamf-pro/reference/jamf-pro-api
# SANDBOX:   https://www.jamf.com/try/
# FAVICON:   https://jamf.com/favicon.ico
# SKILL:     —
# MCP:       —
# LLMS:      —
from mocks.base import BaseMock, route
from models import MockResponse


# LOC EXCEPTION: Jamf Pro uses multiple core resources (auth, computers-inventory, mobile-devices, scripts) with schema-faithful list/detail shapes.
class JamfMock(BaseMock):
    prefix = "/jamf"
    spec_url = "https://developer.jamf.com/jamf-pro/reference/jamf-pro-api"
    sandbox_base = "https://example.jamfcloud.com"

    @route("POST", "/v1/oauth/token")
    async def oauth_token(self, request, **kw):
        return MockResponse(
            body={
                "access_token": "jamf_mock_token_verifiabl",
                "token_type": "Bearer",
                "expires_in": 1200,
            }
        )

    @route("POST", "/v1/auth/token")
    async def auth_token(self, request, **kw):
        return MockResponse(
            body={
                "token": "jamf_mock_token_verifiabl",
                "expires": "2025-06-01T12:00:00.000Z",
            }
        )

    @route("GET", "/v1/computers-inventory", writes=False)
    async def list_computers(self, request, **kw):
        return MockResponse(
            body={
                "totalCount": 2,
                "results": [
                    {
                        "id": "1",
                        "general": {
                            "name": "MacBook-Pro-001",
                            "serialNumber": "C02L29ECF8J1",
                            "udid": "udid_mock_001",
                        },
                    },
                    {
                        "id": "2",
                        "general": {
                            "name": "MacBook-Pro-002",
                            "serialNumber": "C02L29ECF8J2",
                            "udid": "udid_mock_002",
                        },
                    },
                ],
            }
        )

    @route("GET", "/v1/computers-inventory/{id}", writes=False)
    async def get_computer(self, request, id="", **kw):
        return MockResponse(
            body={
                "id": id or "1",
                "general": {
                    "name": "MacBook-Pro-001",
                    "serialNumber": "C02L29ECF8J1",
                    "udid": "udid_mock_001",
                    "reportDate": "2026-03-14T12:00:00.000Z",
                },
            }
        )

    @route("GET", "/v1/mobile-devices", writes=False)
    async def list_mobile_devices(self, request, **kw):
        return MockResponse(
            body={
                "totalCount": 2,
                "results": [
                    {
                        "id": "1",
                        "name": "iPhone-001",
                        "udid": "udid_iphone_001",
                        "serialNumber": "SN_001",
                    },
                    {
                        "id": "2",
                        "name": "iPad-001",
                        "udid": "udid_ipad_001",
                        "serialNumber": "SN_002",
                    },
                ],
            }
        )

    @route("GET", "/v1/mobile-devices/{id}", writes=False)
    async def get_mobile_device(self, request, id="", **kw):
        return MockResponse(
            body={
                "id": id or "1",
                "name": "iPhone-001",
                "udid": "udid_iphone_001",
                "serialNumber": "SN_001",
                "wifiMacAddress": "00:11:22:33:44:55",
            }
        )

    @route("PATCH", "/v1/mobile-devices/{id}")
    async def update_mobile_device(self, request, id="", **kw):
        return MockResponse(body={"id": id or "1"})

    @route("GET", "/v1/scripts", writes=False)
    async def list_scripts(self, request, **kw):
        return MockResponse(
            body={
                "totalCount": 2,
                "results": [
                    {
                        "id": "1",
                        "name": "Install Developer Utils Script",
                        "info": "Installs utilities",
                        "categoryName": "Developer Tools",
                        "priority": "AFTER",
                    },
                    {
                        "id": "2",
                        "name": "Configure Settings",
                        "info": "Applies settings",
                        "categoryName": "Configuration",
                        "priority": "BEFORE",
                    },
                ],
            }
        )

    @route("GET", "/v1/scripts/{id}", writes=False)
    async def get_script(self, request, id="", **kw):
        return MockResponse(
            body={
                "id": id or "1",
                "name": "Install Developer Utils Script",
                "info": "Installs utilities for developers",
                "notes": "Re-runnable.",
                "priority": "AFTER",
                "categoryId": "1",
                "categoryName": "Developer Tools",
                "scriptContents": '#!/bin/bash\necho "Trivial script."',
            }
        )

    @route("POST", "/v1/scripts")
    async def create_script(self, request, **kw):
        return MockResponse(status=201, body={"id": "3", "name": "New Script"})
