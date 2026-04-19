# CHANGELOG: https://developers.smartsheet.com/api/smartsheet/changelog  (no RSS/atom feed as of 2026-03)
# SPEC:      https://developers.smartsheet.com/_bundle/api/smartsheet/openapi.json
# SANDBOX:   https://app.smartsheet.com/
# SKILL:     —
# MCP:       —
# LLMS:      —
from mocks.base import BaseMock, route
from models import MockResponse


class SmartsheetMock(BaseMock):
    prefix = "/smartsheet"
    spec_url = "https://developers.smartsheet.com/api/smartsheet/openapi/schemas/name"
    sandbox_base = "https://api.smartsheet.com/2.0"

    @route("GET", "/sheets", writes=False)
    async def list_sheets(self, request, **kw):
        return MockResponse(
            body={
                "data": [
                    {"id": 1234567890, "name": "Project Tracker", "owner": "", "ownerId": 0},
                    {"id": 9876543210, "name": "Task List", "owner": "", "ownerId": 0},
                ],
                "pageNumber": 1,
                "pageSize": 100,
                "totalCount": 2,
                "totalPages": 1,
            }
        )

    @route("GET", "/sheets/{sheetId}", writes=False)
    async def get_sheet(self, request, sheetId="", **kw):
        sid = sheetId or "1234567890"
        return MockResponse(
            body={
                "id": int(sid) if sid.isdigit() else 1234567890,
                "name": "Project Tracker",
                "accessLevel": "ADMIN",
                "ownerId": 100,
                "owner": "user@verifiabl.dev",
                "permalink": "https://app.smartsheet.com/sheets/xxx",
                "version": 1,
                "totalRowCount": 2,
                "createdAt": "2019-08-24T14:15:22Z",
                "modifiedAt": "2019-08-24T14:15:22Z",
                "columns": [
                    {"id": 101, "title": "Task", "type": "TEXT_NUMBER", "index": 0},
                    {"id": 102, "title": "Status", "type": "PICKLIST", "index": 1},
                ],
                "rows": [
                    {
                        "id": 201,
                        "rowNumber": 1,
                        "sheetId": int(sid) if sid.isdigit() else 1234567890,
                        "cells": [
                            {"columnId": 101, "value": "Setup"},
                            {"columnId": 102, "value": "Done"},
                        ],
                    },
                    {
                        "id": 202,
                        "rowNumber": 2,
                        "sheetId": int(sid) if sid.isdigit() else 1234567890,
                        "cells": [
                            {"columnId": 101, "value": "Review"},
                            {"columnId": 102, "value": "In Progress"},
                        ],
                    },
                ],
            }
        )

    @route("POST", "/sheets")
    async def create_sheet(self, request, **kw):
        return MockResponse(
            status=201,
            body={
                "message": "SUCCESS",
                "resultCode": 0,
                "data": {"id": 1234567891, "name": "New Sheet", "accessLevel": "ADMIN"},
            },
        )

    @route("DELETE", "/sheets/{sheetId}")
    async def delete_sheet(self, request, sheetId="", **kw):
        return MockResponse(body={"message": "SUCCESS", "resultCode": 0})

    @route("GET", "/sheets/{sheetId}/rows", writes=False)
    async def list_rows(self, request, sheetId="", **kw):
        sid = sheetId or "1234567890"
        return MockResponse(
            body={
                "data": [
                    {
                        "id": 201,
                        "rowNumber": 1,
                        "sheetId": int(sid) if sid.isdigit() else 1234567890,
                        "cells": [
                            {"columnId": 101, "value": "Setup"},
                            {"columnId": 102, "value": "Done"},
                        ],
                    },
                    {
                        "id": 202,
                        "rowNumber": 2,
                        "sheetId": int(sid) if sid.isdigit() else 1234567890,
                        "cells": [
                            {"columnId": 101, "value": "Review"},
                            {"columnId": 102, "value": "In Progress"},
                        ],
                    },
                ],
                "pageNumber": 1,
                "pageSize": 100,
                "totalCount": 2,
                "totalPages": 1,
            }
        )

    @route("POST", "/sheets/{sheetId}/rows")
    async def add_rows(self, request, sheetId="", **kw):
        return MockResponse(
            status=200,
            body={"message": "SUCCESS", "resultCode": 0, "data": [{"id": 203, "rowNumber": 3}]},
        )

    @route("GET", "/sheets/{sheetId}/columns", writes=False)
    async def list_columns(self, request, sheetId="", **kw):
        return MockResponse(
            body={
                "data": [
                    {"id": 101, "title": "Task", "type": "TEXT_NUMBER", "index": 0},
                    {"id": 102, "title": "Status", "type": "PICKLIST", "index": 1},
                ],
                "pageNumber": 1,
                "pageSize": 100,
                "totalCount": 2,
                "totalPages": 1,
            }
        )

    @route("GET", "/users/me", writes=False)
    async def get_current_user(self, request, **kw):
        return MockResponse(
            body={
                "data": {
                    "id": 100,
                    "email": "user@verifiabl.dev",
                    "firstName": "Mock",
                    "lastName": "User",
                    "admin": False,
                    "licensedSheetCreator": True,
                },
            }
        )
