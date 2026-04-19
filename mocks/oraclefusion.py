# CHANGELOG: https://docs.oracle.com/en/cloud/saas/financials/ (no RSS/atom feed found as of 2026-03)
# SPEC:      https://docs.oracle.com/en/cloud/saas/financials/26a/farfa/rest-endpoints.html
# SANDBOX:   https://xxx.fa.us2.oraclecloud.com (instance-specific)
# SKILL:     —
# MCP:       —
# LLMS:      —
from mocks.base import BaseMock, route
from models import MockResponse

_V = "11.13.18.05"
_BASE = f"/fscmRestApi/resources/{_V}"


class OracleFusionMock(BaseMock):
    prefix = "/oraclefusion"
    spec_url = "https://docs.oracle.com/en/cloud/saas/financials/26a/farfa/rest-endpoints.html"
    sandbox_base = "https://xxx.fa.us2.oraclecloud.com"

    @route("GET", f"{_BASE}/invoices", writes=False)
    async def list_invoices(self, request, **kw):
        return MockResponse(
            body={
                "items": [
                    {
                        "InvoicesUniqID": "inv_mock_001",
                        "InvoiceNumber": "INV-001",
                        "InvoiceAmount": 2000,
                        "Status": "Validated",
                    },
                    {
                        "InvoicesUniqID": "inv_mock_002",
                        "InvoiceNumber": "INV-002",
                        "InvoiceAmount": 1500,
                        "Status": "Draft",
                    },
                ],
                "count": 2,
            }
        )

    @route("POST", f"{_BASE}/invoices")
    async def create_invoice(self, request, **kw):
        return MockResponse(
            status=201,
            body={
                "InvoicesUniqID": "inv_mock_new",
                "InvoiceNumber": "INV-NEW",
                "InvoiceAmount": 0,
                "Status": "Draft",
            },
        )

    @route("GET", f"{_BASE}/invoices/{{invoicesUniqID}}", writes=False)
    async def get_invoice(self, request, invoicesUniqID="", **kw):
        return MockResponse(
            body={
                "InvoicesUniqID": invoicesUniqID or "inv_mock_001",
                "InvoiceNumber": "INV-001",
                "InvoiceAmount": 2000,
                "Status": "Validated",
                "InvoiceDate": "2024-03-14T00:00:00",
            }
        )

    @route("PATCH", f"{_BASE}/invoices/{{invoicesUniqID}}")
    async def update_invoice(self, request, invoicesUniqID="", **kw):
        return MockResponse(
            body={
                "InvoicesUniqID": invoicesUniqID or "inv_mock_001",
                "InvoiceNumber": "INV-001",
                "InvoiceAmount": 2000,
                "Status": "Validated",
            }
        )

    @route("GET", f"{_BASE}/cashBankAccounts", writes=False)
    async def list_bank_accounts(self, request, **kw):
        return MockResponse(
            body={
                "items": [
                    {
                        "BankAccountId": 300100123456789,
                        "BankAccountName": "Operating Account",
                        "CurrencyCode": "USD",
                    },
                    {
                        "BankAccountId": 300100123456790,
                        "BankAccountName": "Payables Account",
                        "CurrencyCode": "USD",
                    },
                ],
                "count": 2,
            }
        )

    @route("POST", f"{_BASE}/cashBankAccounts")
    async def create_bank_account(self, request, **kw):
        return MockResponse(
            status=201,
            body={
                "BankAccountId": 300100123456791,
                "BankAccountName": "Mock Account",
                "CurrencyCode": "USD",
            },
        )

    @route("GET", f"{_BASE}/cashBankAccounts/{{BankAccountId}}", writes=False)
    async def get_bank_account(self, request, BankAccountId="", **kw):
        return MockResponse(
            body={
                "BankAccountId": int(BankAccountId) if BankAccountId.isdigit() else 300100123456789,
                "BankAccountName": "Operating Account",
                "CurrencyCode": "USD",
            }
        )

    @route("GET", f"{_BASE}/journalBatches", writes=False)
    async def list_journal_batches(self, request, **kw):
        return MockResponse(
            body={
                "items": [
                    {"JeBatchId": 400100123456789, "BatchName": "MAR-2024-01", "Status": "Posted"},
                    {
                        "JeBatchId": 400100123456790,
                        "BatchName": "MAR-2024-02",
                        "Status": "Complete",
                    },
                ],
                "count": 2,
            }
        )

    @route("GET", f"{_BASE}/journalBatches/{{JeBatchId}}", writes=False)
    async def get_journal_batch(self, request, JeBatchId="", **kw):
        return MockResponse(
            body={
                "JeBatchId": int(JeBatchId) if JeBatchId.isdigit() else 400100123456789,
                "BatchName": "MAR-2024-01",
                "Status": "Posted",
            }
        )
