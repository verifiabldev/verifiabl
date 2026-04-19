# CHANGELOG: https://learn.microsoft.com/en-us/power-bi/rest-api/changelog (no RSS/atom feed as of 2026-03)
# SPEC:      https://learn.microsoft.com/en-us/rest/api/power-bi/
# SANDBOX:   https://app.powerbi.com/
# SKILL:     —
# MCP:       —
# LLMS:      —
from mocks.base import BaseMock, route
from models import MockResponse


class PowerBIMock(BaseMock):
    prefix = "/powerbi"
    spec_url = "https://learn.microsoft.com/en-us/rest/api/power-bi/"
    sandbox_base = "https://api.powerbi.com"

    @route("GET", "/v1.0/myorg/groups", writes=False)
    async def list_groups(self, request, **kw):
        return MockResponse(
            body={
                "value": [
                    {
                        "id": "f089354e-8366-4e18-aea3-4cb4a3a50b48",
                        "isReadOnly": False,
                        "isOnDedicatedCapacity": False,
                        "name": "sample group",
                    },
                    {
                        "id": "3d9b93c6-7b6d-4801-a491-1738910904fd",
                        "isReadOnly": False,
                        "isOnDedicatedCapacity": True,
                        "capacityId": "0f084df7-c13d-451b-af5f-ed0c466403b2",
                        "name": "marketing group",
                    },
                ]
            }
        )

    @route("GET", "/v1.0/myorg/groups/{groupId}", writes=False)
    async def get_group(self, request, groupId="", **kw):
        return MockResponse(
            body={
                "id": groupId or "f089354e-8366-4e18-aea3-4cb4a3a50b48",
                "isReadOnly": False,
                "isOnDedicatedCapacity": False,
                "name": "sample group",
            }
        )

    @route("GET", "/v1.0/myorg/reports", writes=False)
    async def list_reports(self, request, **kw):
        return MockResponse(
            body={
                "value": [
                    {
                        "id": "5b218778-e7a5-4d73-8187-f10824047715",
                        "datasetId": "cfafbeb1-8037-4d0c-896e-a46fb27ff229",
                        "name": "SalesMarketing",
                        "webUrl": "https://app.powerbi.com/reports/5b218778-e7a5-4d73-8187-f10824047715",
                        "embedUrl": "https://app.powerbi.com/reportEmbed?reportId=5b218778-e7a5-4d73-8187-f10824047715",
                    },
                ]
            }
        )

    @route("GET", "/v1.0/myorg/reports/{reportId}", writes=False)
    async def get_report(self, request, reportId="", **kw):
        return MockResponse(
            body={
                "id": reportId or "5b218778-e7a5-4d73-8187-f10824047715",
                "datasetId": "cfafbeb1-8037-4d0c-896e-a46fb27ff229",
                "name": "SalesMarketing",
                "webUrl": "https://app.powerbi.com/reports/5b218778-e7a5-4d73-8187-f10824047715",
                "embedUrl": "https://app.powerbi.com/reportEmbed?reportId=5b218778-e7a5-4d73-8187-f10824047715",
            }
        )

    @route("GET", "/v1.0/myorg/datasets", writes=False)
    async def list_datasets(self, request, **kw):
        return MockResponse(
            body={
                "value": [
                    {
                        "id": "cfafbeb1-8037-4d0c-896e-a46fb27ff229",
                        "name": "SalesMarketing",
                        "addRowsAPIEnabled": False,
                        "configuredBy": "john@verifiabl.dev",
                        "isRefreshable": True,
                        "isEffectiveIdentityRequired": False,
                        "isEffectiveIdentityRolesRequired": False,
                        "isOnPremGatewayRequired": False,
                    },
                ]
            }
        )

    @route("GET", "/v1.0/myorg/datasets/{datasetId}", writes=False)
    async def get_dataset(self, request, datasetId="", **kw):
        return MockResponse(
            body={
                "id": datasetId or "cfafbeb1-8037-4d0c-896e-a46fb27ff229",
                "name": "SalesMarketing",
                "addRowsAPIEnabled": False,
                "configuredBy": "john@verifiabl.dev",
                "isRefreshable": True,
                "isEffectiveIdentityRequired": False,
                "isEffectiveIdentityRolesRequired": False,
                "isOnPremGatewayRequired": False,
            }
        )

    @route("GET", "/v1.0/myorg/dashboards", writes=False)
    async def list_dashboards(self, request, **kw):
        return MockResponse(
            body={
                "value": [
                    {
                        "id": "69ffaa6c-b36d-4d01-96f5-1ed67c64d4af",
                        "displayName": "SalesMarketing",
                        "embedUrl": "https://app.powerbi.com/dashboardEmbed?dashboardId=69ffaa6c-b36d-4d01-96f5-1ed67c64d4af",
                        "isReadOnly": False,
                    },
                ]
            }
        )

    @route("GET", "/v1.0/myorg/dashboards/{dashboardId}", writes=False)
    async def get_dashboard(self, request, dashboardId="", **kw):
        return MockResponse(
            body={
                "id": dashboardId or "69ffaa6c-b36d-4d01-96f5-1ed67c64d4af",
                "displayName": "SalesMarketing",
                "embedUrl": "https://app.powerbi.com/dashboardEmbed?dashboardId=69ffaa6c-b36d-4d01-96f5-1ed67c64d4af",
                "isReadOnly": False,
            }
        )

    @route("GET", "/v1.0/myorg/groups/{groupId}/reports", writes=False)
    async def list_reports_in_group(self, request, groupId="", **kw):
        return MockResponse(
            body={
                "value": [
                    {
                        "id": "5b218778-e7a5-4d73-8187-f10824047715",
                        "datasetId": "cfafbeb1-8037-4d0c-896e-a46fb27ff229",
                        "name": "SalesMarketing",
                        "webUrl": "https://app.powerbi.com/reports/5b218778-e7a5-4d73-8187-f10824047715",
                        "embedUrl": "https://app.powerbi.com/reportEmbed?reportId=5b218778-e7a5-4d73-8187-f10824047715",
                    }
                ]
            }
        )

    @route("POST", "/v1.0/myorg/groups")
    async def create_group(self, request, **kw):
        return MockResponse(
            status=201,
            body={
                "id": "a2f89923-421a-464e-bf4c-25eab39bb09f",
                "isReadOnly": False,
                "isOnDedicatedCapacity": False,
                "name": "New workspace",
            },
        )

    @route("POST", "/v1.0/myorg/GenerateToken")
    async def generate_token(self, request, **kw):
        return MockResponse(
            body={
                "token": "H4sIAAAAAAAA_mock_embed_token_verifiabl",
                "expiration": "2025-04-14T12:00:00Z",
                "tokenId": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
            }
        )
