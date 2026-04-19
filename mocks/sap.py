# CHANGELOG: https://help.sap.com/docs/SAP_S4HANA_CLOUD (no RSS/atom feed as of 2026-03)
# SPEC:      https://github.com/SAP/openapi-specification
# SANDBOX:   https://api.sap.com/
# SKILL:     —
# MCP:       —
# LLMS:      —
from mocks.base import BaseMock, route
from models import MockResponse


def _odata_list(results: list) -> dict:
    return {"d": {"results": results}}


def _odata_entity(entity_id: str, base_uri: str, **props) -> dict:
    return {
        "d": {
            "__metadata": {"id": f"{base_uri}('{entity_id}')", "uri": f"{base_uri}('{entity_id}')"},
            **props,
        }
    }


class SapMock(BaseMock):
    prefix = "/sap"
    spec_url = "https://github.com/SAP/openapi-specification"
    sandbox_base = "https://api.sap.com"

    @route("GET", "/opu/odata/sap/API_BUSINESS_PARTNER/A_BusinessPartner", writes=False)
    async def list_business_partners(self, request, **kw):
        return MockResponse(
            body=_odata_list(
                [
                    {
                        "BusinessPartner": "bp_mock_001",
                        "FirstName": "Alice",
                        "LastName": "Acme",
                        "CreationDate": "/Date(1710400000000)/",
                    },
                    {
                        "BusinessPartner": "bp_mock_002",
                        "FirstName": "Bob",
                        "LastName": "Builders",
                        "CreationDate": "/Date(1710400000000)/",
                    },
                ]
            )
        )

    @route("POST", "/opu/odata/sap/API_BUSINESS_PARTNER/A_BusinessPartner")
    async def create_business_partner(self, request, **kw):
        return MockResponse(
            status=201,
            body=_odata_entity(
                "bp_mock_new",
                "https://host/sap/opu/odata/sap/API_BUSINESS_PARTNER/A_BusinessPartner",
                BusinessPartner="bp_mock_new",
                FirstName="New",
                LastName="Partner",
                CreationDate="/Date(1710400000000)/",
            ),
        )

    @route("GET", "/opu/odata/sap/API_BUSINESS_PARTNER/A_BusinessPartner('{id}')", writes=False)
    async def get_business_partner(self, request, id="", **kw):
        return MockResponse(
            body=_odata_entity(
                id,
                "https://host/sap/opu/odata/sap/API_BUSINESS_PARTNER/A_BusinessPartner",
                BusinessPartner=id,
                FirstName="Mock",
                LastName="Partner",
                CreationDate="/Date(1710400000000)/",
            )
        )

    @route("GET", "/opu/odata/sap/API_SALES_ORDER_SRV/A_SalesOrder", writes=False)
    async def list_sales_orders(self, request, **kw):
        return MockResponse(
            body=_odata_list(
                [
                    {
                        "SalesOrder": "so_mock_001",
                        "SalesOrderType": "OR",
                        "SoldToParty": "bp_mock_001",
                        "TotalNetAmount": "1200.00",
                        "TransactionCurrency": "USD",
                    },
                    {
                        "SalesOrder": "so_mock_002",
                        "SalesOrderType": "OR",
                        "SoldToParty": "bp_mock_002",
                        "TotalNetAmount": "800.50",
                        "TransactionCurrency": "USD",
                    },
                ]
            )
        )

    @route("POST", "/opu/odata/sap/API_SALES_ORDER_SRV/A_SalesOrder")
    async def create_sales_order(self, request, **kw):
        return MockResponse(
            status=201,
            body=_odata_entity(
                "so_mock_new",
                "https://host/sap/opu/odata/sap/API_SALES_ORDER_SRV/A_SalesOrder",
                SalesOrder="so_mock_new",
                SalesOrderType="OR",
                SoldToParty="bp_mock_001",
                TotalNetAmount="500.00",
                TransactionCurrency="USD",
            ),
        )

    @route("GET", "/opu/odata/sap/API_SALES_ORDER_SRV/A_SalesOrder('{id}')", writes=False)
    async def get_sales_order(self, request, id="", **kw):
        return MockResponse(
            body=_odata_entity(
                id,
                "https://host/sap/opu/odata/sap/API_SALES_ORDER_SRV/A_SalesOrder",
                SalesOrder=id,
                SalesOrderType="OR",
                SoldToParty="bp_mock_001",
                TotalNetAmount="500.00",
                TransactionCurrency="USD",
            )
        )
