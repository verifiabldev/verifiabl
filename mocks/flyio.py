# CHANGELOG: https://fly.io/changelog.xml
# SPEC:      https://docs.machines.dev
# SANDBOX:   https://fly.io/dashboard
# FAVICON:   https://fly.io/favicon.ico
# SKILL:     —
# MCP:       —
# LLMS:      —
from mocks.base import BaseMock, route
from models import MockResponse


class FlyioMock(BaseMock):
    prefix = "/flyio"
    spec_url = "https://docs.machines.dev"
    sandbox_base = "https://api.machines.dev"

    @route("GET", "/v1/apps", writes=False)
    async def list_apps(self, request, **kw):
        return MockResponse(
            body={
                "total_apps": 2,
                "apps": [
                    {
                        "id": "682kqp6pdno9d543",
                        "name": "my-app-1",
                        "machine_count": 1,
                        "volume_count": 0,
                        "network": "default",
                    },
                    {
                        "id": "z4k69dxd8r31p5mx",
                        "name": "my-app-2",
                        "machine_count": 0,
                        "volume_count": 1,
                        "network": "default",
                    },
                ],
            }
        )

    @route("POST", "/v1/apps")
    async def create_app(self, request, **kw):
        return MockResponse(
            status=201, body={"id": "app_mock_verifiabl", "created_at": 1710400000000}
        )

    @route("GET", "/v1/apps/{app_name}", writes=False)
    async def get_app(self, request, app_name="", **kw):
        return MockResponse(
            body={
                "id": "jlyv9r5d56v18xrg",
                "name": app_name or "my-app-1",
                "status": "running",
                "organization": {"name": "My Org", "slug": "personal"},
            }
        )

    @route("DELETE", "/v1/apps/{app_name}")
    async def delete_app(self, request, app_name="", **kw):
        return MockResponse(status=202)

    @route("GET", "/v1/apps/{app_name}/machines", writes=False)
    async def list_machines(self, request, app_name="", **kw):
        return MockResponse(
            body=[
                {
                    "id": "a5c5de9ce64ca12",
                    "name": "aged-wind-2649",
                    "state": "started",
                    "region": "ord",
                    "instance_id": "1RREBN3T5K95DK9IVP4XHTTPEY2",
                    "private_ip": "fdaa:0:18:a7b:196:e274:9ce1:2",
                    "created_at": "2023-10-31T02:30:10Z",
                    "updated_at": "2023-10-31T02:35:26Z",
                    "image_ref": {
                        "registry": "registry-1.docker.io",
                        "repository": "library/ubuntu",
                        "tag": "latest",
                    },
                },
            ]
        )

    @route("POST", "/v1/apps/{app_name}/machines")
    async def create_machine(self, request, app_name="", **kw):
        return MockResponse(
            body={
                "id": "machine_mock_001",
                "name": "verifiabl-machine",
                "state": "starting",
                "region": "ord",
                "instance_id": "1RREBN3T5K95DK9IVP4XHTTPEY2",
                "created_at": "2023-10-31T02:30:10Z",
                "updated_at": "2023-10-31T02:30:10Z",
                "config": {"image": "registry-1.docker.io/library/ubuntu:latest"},
            }
        )

    @route("GET", "/v1/apps/{app_name}/machines/{machine_id}", writes=False)
    async def get_machine(self, request, app_name="", machine_id="", **kw):
        return MockResponse(
            body={
                "id": machine_id or "a5c5de9ce64ca12",
                "name": "aged-wind-2649",
                "state": "started",
                "region": "ord",
                "instance_id": "1RREBN3T5K95DK9IVP4XHTTPEY2",
                "private_ip": "fdaa:0:18:a7b:196:e274:9ce1:2",
                "created_at": "2023-10-31T02:30:10Z",
                "updated_at": "2023-10-31T02:35:26Z",
                "config": {
                    "image": "registry-1.docker.io/library/ubuntu:latest",
                    "guest": {"cpus": 1, "memory_mb": 256},
                },
            }
        )

    @route("POST", "/v1/apps/{app_name}/machines/{machine_id}/start")
    async def start_machine(self, request, app_name="", machine_id="", **kw):
        return MockResponse(body={"ok": True})

    @route("POST", "/v1/apps/{app_name}/machines/{machine_id}/stop")
    async def stop_machine(self, request, app_name="", machine_id="", **kw):
        return MockResponse(body={"ok": True})

    @route("DELETE", "/v1/apps/{app_name}/machines/{machine_id}")
    async def delete_machine(self, request, app_name="", machine_id="", **kw):
        return MockResponse(body={"ok": True})

    @route("GET", "/v1/apps/{app_name}/volumes", writes=False)
    async def list_volumes(self, request, app_name="", **kw):
        return MockResponse(
            body=[
                {
                    "id": "vol_9vw681egy1jj5xm4",
                    "name": "disk",
                    "state": "created",
                    "size_gb": 3,
                    "region": "yul",
                    "zone": "09cd",
                    "encrypted": True,
                    "attached_machine_id": "908057ef21e487",
                    "created_at": "2023-09-01T19:47:14.774Z",
                },
            ]
        )

    @route("POST", "/v1/apps/{app_name}/volumes")
    async def create_volume(self, request, app_name="", **kw):
        return MockResponse(
            body={
                "id": "vol_mock_verifiabl",
                "name": "disk",
                "state": "created",
                "size_gb": 3,
                "region": "ord",
                "zone": "84d3",
                "encrypted": True,
                "attached_machine_id": None,
                "created_at": "2023-11-27T21:47:06.837Z",
            }
        )

    @route("GET", "/v1/apps/{app_name}/volumes/{volume_id}", writes=False)
    async def get_volume(self, request, app_name="", volume_id="", **kw):
        return MockResponse(
            body={
                "id": volume_id or "vol_9vw681egy1jj5xm4",
                "name": "disk",
                "state": "created",
                "size_gb": 3,
                "region": "yul",
                "zone": "09cd",
                "encrypted": True,
                "attached_machine_id": "908057ef21e487",
                "created_at": "2023-09-01T19:47:14.774Z",
            }
        )

    @route("DELETE", "/v1/apps/{app_name}/volumes/{volume_id}")
    async def delete_volume(self, request, app_name="", volume_id="", **kw):
        return MockResponse(body={"id": volume_id or "vol_9vw681egy1jj5xm4", "state": "destroyed"})
