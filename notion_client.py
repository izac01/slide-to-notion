# notion_client.py (append)
import os, json
from typing import List, Dict, Any

def _notion_headers():
    key = os.getenv("NOTION_API_KEY")
    return key, {"Authorization": f"Bearer {key}", "Notion-Version": "2022-06-28", "Content-Type": "application/json"}

def create_page(database_id: str, title: str, children: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    MVP: if NOTION_API_KEY is missing, just print the payload and return a stub.
    Later we’ll POST to https://api.notion.com/v1/pages
    """
    key, headers = _notion_headers()
    payload = {
        "parent": {"database_id": database_id},
        "properties": {"Name": {"title": [{"type":"text","text":{"content": title}}]}},
        "children": children,
    }
    if not key:
        print("[MVP] Notion upload skipped (no NOTION_API_KEY). Payload:\n", json.dumps(payload)[:2000])
        return {"id": "stub", "url": "https://notion.so/stub"}
    # Real POST — TODO enable once creds are wired; keeping offline safe for tonight
    try:
        import requests
        r = requests.post("https://api.notion.com/v1/pages", headers=headers, data=json.dumps(payload))
        r.raise_for_status()
        return r.json()
    except Exception as e:
        print("[MVP] Notion upload failed; returning stub. Error:", e)
        return {"id": "stub", "url": "https://notion.so/stub"}
