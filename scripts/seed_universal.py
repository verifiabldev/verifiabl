#!/usr/bin/env python3
"""Load fixtures/*.json into store.universal for local development."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from store import store

fixtures_dir = Path(__file__).resolve().parent.parent / "fixtures"
store.load_fixtures(fixtures_dir)
print(
    f"Loaded {len(store.universal)} entries from {sum(1 for _ in fixtures_dir.glob('*.json'))} fixture files"
)
