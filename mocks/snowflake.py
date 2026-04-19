# CHANGELOG: https://data-docs.snowflake.com/foundations/changelog/  (no RSS/atom feed as of 2026-03)
# SPEC:      https://github.com/snowflakedb/snowflake-rest-api-specs
# SANDBOX:   https://api.developers.snowflake.com/
# SKILL:     —
# MCP:       https://docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-agents-mcp
# LLMS:      —
from mocks.base import BaseMock, route
from models import MockResponse


def _result_set(statement_handle: str, data: list = None):
    return {
        "resultSetMetaData": {
            "numRows": len(data) if data else 0,
            "format": "jsonv2",
            "rowType": [
                {"name": "ID", "type": "fixed", "precision": 19, "scale": 0, "nullable": False}
            ],
            "partitionInfo": [{"rowCount": len(data) if data else 0, "uncompressedSize": 256}],
        },
        "data": data or [["1"], ["2"]],
        "code": "090001",
        "statementStatusUrl": f"/api/v2/statements/{statement_handle}",
        "sqlState": "00000",
        "statementHandle": statement_handle,
        "message": "Statement executed successfully.",
        "createdOn": 1710400000000,
    }


class SnowflakeMock(BaseMock):
    prefix = "/snowflake"
    spec_url = "https://github.com/snowflakedb/snowflake-rest-api-specs"
    sandbox_base = "https://mock_account.snowflakecomputing.com"

    @route("GET", "/api/v2/databases", writes=False)
    async def list_databases(self, request, **kw):
        return MockResponse(
            body={
                "items": [
                    {"name": "MOCK_DB", "owner": "ACCOUNTADMIN", "createdOn": "1710400000000"},
                    {"name": "SAMPLE_DB", "owner": "ACCOUNTADMIN", "createdOn": "1710400001000"},
                ],
            }
        )

    @route("GET", "/api/v2/databases/{database}/schemas", writes=False)
    async def list_schemas(self, request, database="", **kw):
        return MockResponse(
            body={
                "items": [
                    {
                        "name": "PUBLIC",
                        "databaseName": database or "MOCK_DB",
                        "owner": "ACCOUNTADMIN",
                    },
                    {
                        "name": "INFO_SCHEMA",
                        "databaseName": database or "MOCK_DB",
                        "owner": "ACCOUNTADMIN",
                    },
                ],
            }
        )

    @route("GET", "/api/v2/databases/{database}/schemas/{schema}/tables", writes=False)
    async def list_tables(self, request, database="", schema="", **kw):
        return MockResponse(
            body={
                "items": [
                    {
                        "name": "MOCK_TABLE",
                        "schemaName": schema or "PUBLIC",
                        "databaseName": database or "MOCK_DB",
                        "rowCount": 100,
                    },
                    {
                        "name": "USERS",
                        "schemaName": schema or "PUBLIC",
                        "databaseName": database or "MOCK_DB",
                        "rowCount": 42,
                    },
                ],
            }
        )

    @route("GET", "/api/v2/warehouses", writes=False)
    async def list_warehouses(self, request, **kw):
        return MockResponse(
            body={
                "items": [
                    {"name": "COMPUTE_WH", "size": "SMALL", "state": "STARTED"},
                    {"name": "REPORTING_WH", "size": "MEDIUM", "state": "SUSPENDED"},
                ],
            }
        )

    @route("POST", "/api/v2/statements")
    async def submit_statement(self, request, **kw):
        return MockResponse(body=_result_set("019c06a4-0000-df4f-0000-00100006589e"))

    @route("GET", "/api/v2/statements/{statementHandle}", writes=False)
    async def get_statement(self, request, statementHandle="", **kw):
        return MockResponse(
            body=_result_set(statementHandle or "019c06a4-0000-df4f-0000-00100006589e")
        )

    @route("POST", "/api/v2/statements/{statementHandle}/cancel")
    async def cancel_statement(self, request, statementHandle="", **kw):
        return MockResponse(body={"code": "090011", "message": "Statement execution cancelled."})
