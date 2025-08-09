"""Notion client (stubbed)."""
from typing import Dict, Any

def upsert(database_id: str, notion_block: Dict[str, Any]) -> None:
    if not isinstance(notion_block, dict):
        raise TypeError("notion_block must be a dict")
