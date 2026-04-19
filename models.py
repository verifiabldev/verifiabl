from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional, Union


class Tier(str, Enum):
    ANON = "anon"
    FREE = "free"
    PAID = "paid"
    ADMIN = "admin"


@dataclass
class Route:
    method: str
    path_pattern: str
    handler: str
    writes: bool = True


@dataclass
class MockResponse:
    status: int = 200
    body: Optional[Union[dict, list, bytes]] = None
    headers: dict = field(default_factory=dict)
    content_type: Optional[str] = None


@dataclass
class Account:
    account_id: str
    email: str


@dataclass
class Credential:
    key: str  # vrf_free_... or vrf_paid_...
    account_id: str
    tier: Tier
    revoked: bool = False


@dataclass
class UsageRecord:
    account_id: str
    requests: int = 0
    cost_cents: int = 0  # $0.01 units
