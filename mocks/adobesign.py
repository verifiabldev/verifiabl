# CHANGELOG: https://developer.adobe.com/acrobat-sign/docs/overview/releasenotes/ (no RSS/atom feed as of 2026-03)
# SPEC:      https://developer.adobe.com/document-services/docs/apis/
# SANDBOX:   https://developer.adobe.com
# SKILL:     —
# MCP:       —
# LLMS:      —
from mocks.base import BaseMock, route
from models import MockResponse


class AdobeSignMock(BaseMock):
    prefix = "/adobesign"
    spec_url = "https://developer.adobe.com/document-services/docs/apis/"
    sandbox_base = "https://api.na1.adobesign.com"

    @route("GET", "/api/rest/v6/baseUris", writes=False)
    async def base_uris(self, request, **kw):
        return MockResponse(
            body={
                "api_access_point": "https://api.na1.adobesign.com",
                "web_access_point": "https://secure.na1.adobesign.com",
            }
        )

    @route("GET", "/api/rest/v6/users/me", writes=False)
    async def me(self, request, **kw):
        return MockResponse(
            body={"id": "mock_user", "email": "mock@verifiabl.dev", "status": "ACTIVE"}
        )

    @route("POST", "/api/rest/v6/transientDocuments")
    async def create_transient_document(self, request, **kw):
        return MockResponse(
            body={"transientDocumentId": "3AAABLblqZhBVYbgJbl_mock_verifiabl_zjaBYK"}
        )

    @route("POST", "/api/rest/v6/agreements")
    async def create_agreement(self, request, **kw):
        return MockResponse(status=201, body={"id": "agr_mock_001"})

    @route("GET", "/api/rest/v6/agreements", writes=False)
    async def list_agreements(self, request, **kw):
        return MockResponse(
            body={
                "userAgreementList": [
                    {
                        "agreementId": "agr_mock_001",
                        "name": "Mock Agreement",
                        "status": "SIGNED",
                        "displayDate": "2018-07-23T08:13:16Z",
                    },
                    {
                        "agreementId": "agr_mock_002",
                        "name": "Mock Draft",
                        "status": "OUT_FOR_SIGNATURE",
                        "displayDate": "2018-07-24T09:00:00Z",
                    },
                ],
                "page": {"nextCursor": "qJXXj2UAUX1X9rTSqoUOlkhsdo"},
            }
        )

    @route("GET", "/api/rest/v6/agreements/{id}", writes=False)
    async def get_agreement(self, request, id="", **kw):
        return MockResponse(
            body={
                "id": id or "agr_mock_001",
                "name": "Mock Agreement",
                "status": "SIGNED",
                "createdDate": "2018-07-23T08:13:16Z",
                "signatureType": "ESIGN",
                "senderEmail": "sender@verifiabl.dev",
            }
        )

    @route("GET", "/api/rest/v6/agreements/{id}/signingUrls", writes=False)
    async def get_signing_urls(self, request, id="", **kw):
        return MockResponse(
            body={
                "signingUrlSetInfos": [
                    {
                        "signingUrls": [
                            {
                                "email": "signer@verifiabl.dev",
                                "esignUrl": "https://secure.na1.adobesign.com/public/apiesign?pid=mock_verifiabl",
                            }
                        ],
                    }
                ],
            }
        )

    @route("GET", "/api/rest/v6/agreements/{id}/documents", writes=False)
    async def list_agreement_documents(self, request, id="", **kw):
        return MockResponse(
            body={"documents": [{"id": "doc_mock_001", "name": "Mock Document.pdf"}]}
        )

    @route("GET", "/api/rest/v6/libraryDocuments", writes=False)
    async def list_library_documents(self, request, **kw):
        return MockResponse(
            body={
                "libraryDocumentList": [
                    {"id": "lib_mock_001", "name": "Template NDA", "scope": "SHARED"},
                    {"id": "lib_mock_002", "name": "Template SOW", "scope": "SHARED"},
                ],
            }
        )

    @route("POST", "/api/rest/v6/agreements/{id}/reminders")
    async def create_reminder(self, request, id="", **kw):
        return MockResponse(status=201, body={"id": "rem_mock_001"})
