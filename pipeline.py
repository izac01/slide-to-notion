from typing import List
from slides_client import fetch_presentations, parse_slide
from mappers import google_slides_to_notion
from notion_client import upsert
from utils import calculate_hash
from logs import log_info

def run(auth: str, database_id: str) -> List[str]:
    hashes: List[str] = []
    for pres in fetch_presentations(auth):
        for raw_slide in pres.get("slides", []):
            parsed = parse_slide(raw_slide)
            notion_block = google_slides_to_notion(parsed)
            h = calculate_hash(notion_block)
            upsert(database_id, {**notion_block, "hash": h})
            hashes.append(h)
            log_info(f"upserted slide hash={h}")
    return hashes
