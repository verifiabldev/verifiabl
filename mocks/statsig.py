# CHANGELOG: https://www.statsig.com/updates (no RSS/atom feed as of 2026-03)
# SPEC:      https://api.statsig.com/openapi/20240601.json
# SANDBOX:   https://console.statsig.com
# FAVICON:   https://statsig.com/favicon.ico
# SKILL:     —
# MCP:       —
# LLMS:      —
from mocks.base import BaseMock, route
from models import MockResponse

_PAGINATION = {
    "itemsPerPage": 10,
    "pageNumber": 1,
    "nextPage": None,
    "previousPage": None,
    "totalItems": 2,
    "all": "/console/v1",
}


class StatsigMock(BaseMock):
    prefix = "/statsig"
    spec_url = "https://api.statsig.com/openapi/20240601.json"
    sandbox_base = "https://statsigapi.net"

    def _gate(self, id_: str = "gate_mock_001"):
        return {
            "id": id_,
            "name": "Example Gate",
            "description": "Feature gate for agent testing",
            "idType": "userID",
            "lastModifierID": "mock_uid",
            "lastModifiedTime": 1710400000000,
            "lastModifierName": "Verifiabl",
            "lastModifierEmail": None,
            "creatorID": "mock_uid",
            "createdTime": 1710300000000,
            "creatorName": "Verifiabl",
            "creatorEmail": None,
            "targetApps": [],
            "holdoutIDs": [],
            "tags": [],
            "isEnabled": True,
            "status": "In Progress",
            "rules": [],
            "checksPerHour": 0,
            "type": "PERMANENT",
            "typeReason": "NONE",
            "team": None,
        }

    def _experiment(self, id_: str = "exp_mock_001"):
        return {
            "id": id_,
            "name": "Example Experiment",
            "description": "A/B test for agent workflow",
            "status": "active",
            "idType": "userID",
            "createdTime": 1710300000000,
            "creatorName": "Verifiabl",
            "lastModifiedTime": 1710400000000,
            "lastModifierName": "Verifiabl",
            "variants": [
                {"id": "control", "name": "Control", "description": ""},
                {"id": "treatment", "name": "Treatment", "description": ""},
            ],
        }

    def _dynamic_config(self, id_: str = "config_mock_001"):
        return {
            "id": id_,
            "name": "Example Config",
            "description": "Dynamic config for testing",
            "idType": "userID",
            "lastModifierID": "mock_uid",
            "lastModifiedTime": 1710400000000,
            "lastModifierName": "Verifiabl",
            "lastModifierEmail": None,
            "creatorID": "mock_uid",
            "createdTime": 1710300000000,
            "creatorName": "Verifiabl",
            "creatorEmail": None,
            "targetApps": [],
            "holdoutIDs": [],
            "tags": [],
            "team": None,
            "isEnabled": True,
            "rules": [],
            "defaultValue": {},
            "defaultValueJson5": "{}",
            "version": 1,
        }

    @route("GET", "/console/v1/gates", writes=False)
    async def list_gates(self, request, **kw):
        return MockResponse(
            body={
                "message": "Gates listed successfully.",
                "data": [self._gate("gate_mock_001"), self._gate("gate_mock_002")],
                "pagination": {**_PAGINATION, "all": "/console/v1/gates"},
            }
        )

    @route("GET", "/console/v1/gates/{id}", writes=False)
    async def get_gate(self, request, id="", **kw):
        return MockResponse(
            body={"message": "Gate read successfully.", "data": self._gate(id or "gate_mock_001")}
        )

    @route("GET", "/console/v1/experiments", writes=False)
    async def list_experiments(self, request, **kw):
        return MockResponse(
            body={
                "message": "Experiments listed successfully.",
                "data": [self._experiment("exp_mock_001"), self._experiment("exp_mock_002")],
                "pagination": {**_PAGINATION, "all": "/console/v1/experiments"},
            }
        )

    @route("GET", "/console/v1/experiments/{id}", writes=False)
    async def get_experiment(self, request, id="", **kw):
        return MockResponse(
            body={
                "message": "Experiment read successfully.",
                "data": self._experiment(id or "exp_mock_001"),
            }
        )

    @route("GET", "/console/v1/dynamic_configs", writes=False)
    async def list_dynamic_configs(self, request, **kw):
        return MockResponse(
            body={
                "message": "Dynamic Configs listed successfully.",
                "data": [
                    self._dynamic_config("config_mock_001"),
                    self._dynamic_config("config_mock_002"),
                ],
                "pagination": {**_PAGINATION, "all": "/console/v1/dynamic_configs"},
            }
        )

    @route("GET", "/console/v1/dynamic_configs/{id}", writes=False)
    async def get_dynamic_config(self, request, id="", **kw):
        return MockResponse(
            body={
                "message": "Dynamic config read successfully.",
                "data": self._dynamic_config(id or "config_mock_001"),
            }
        )

    @route("GET", "/console/v1/layers", writes=False)
    async def list_layers(self, request, **kw):
        return MockResponse(
            body={
                "message": "Layers listed successfully.",
                "data": [
                    {
                        "id": "layer_mock_001",
                        "description": "",
                        "idType": "userID",
                        "createdTime": 1710300000000,
                        "creatorName": "Verifiabl",
                        "creatorEmail": None,
                        "lastModifierID": "mock_uid",
                        "lastModifiedTime": 1710400000000,
                        "lastModifierName": "Verifiabl",
                        "lastModifierEmail": None,
                        "creatorID": "mock_uid",
                        "targetApps": [],
                        "holdoutIDs": [],
                        "tags": [],
                        "team": None,
                        "isImplicitLayer": False,
                        "parameters": [
                            {"name": "param1", "type": "string", "defaultValue": "default"}
                        ],
                    },
                    {
                        "id": "layer_mock_002",
                        "description": "Test layer",
                        "idType": "userID",
                        "createdTime": 1710300000000,
                        "creatorName": "Verifiabl",
                        "creatorEmail": None,
                        "lastModifierID": "mock_uid",
                        "lastModifiedTime": 1710400000000,
                        "lastModifierName": "Verifiabl",
                        "lastModifierEmail": None,
                        "creatorID": "mock_uid",
                        "targetApps": [],
                        "holdoutIDs": [],
                        "tags": [],
                        "team": None,
                        "isImplicitLayer": False,
                        "parameters": [],
                    },
                ],
                "pagination": {**_PAGINATION, "all": "/console/v1/layers"},
            }
        )

    @route("GET", "/console/v1/metrics/list", writes=False)
    async def list_metrics(self, request, **kw):
        return MockResponse(
            body={
                "message": "Metrics listed successfully.",
                "data": [
                    {
                        "id": "metric_mock_001",
                        "name": "purchase_count",
                        "type": "count",
                        "createdTime": 1710300000000,
                    },
                    {
                        "id": "metric_mock_002",
                        "name": "revenue",
                        "type": "revenue",
                        "createdTime": 1710300000000,
                    },
                ],
                "pagination": {**_PAGINATION, "all": "/console/v1/metrics/list"},
            }
        )

    @route("POST", "/console/v1/gates")
    async def create_gate(self, request, **kw):
        return MockResponse(
            status=201,
            body={"message": "Gate created successfully.", "data": self._gate("gate_mock_new")},
        )

    @route("POST", "/console/v1/experiments")
    async def create_experiment(self, request, **kw):
        return MockResponse(
            status=201,
            body={
                "message": "Experiment created successfully.",
                "data": self._experiment("exp_mock_new"),
            },
        )
