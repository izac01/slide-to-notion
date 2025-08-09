"""Notion client (stubbed, no Notion SDK yet)."""
from typing import Dict, Any

def upsert(database_id: str, notion_block: Dict[str, Any]) -> None:
    # TODO: replace with Notion API write; assume idempotent by "hash"
    if not isinstance(notion_block, dict):
        raise TypeError("notion_block must be a dict")
