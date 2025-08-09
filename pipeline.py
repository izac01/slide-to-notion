# pipeline.py
import json, os
from pathlib import Path
from typing import Sequence
from mappers import google_slide_to_blocks
from notion_client import create_page

def load_slides(slides_path: str) -> dict:
    p = Path(slides_path)
    return json.loads(p.read_text(encoding="utf-8"))

def run_mvp(
    slides_path: str = "workspace/slides.json",
    pick: Sequence[int] = (0,1,2),
    database_id: str | None = None,
) -> list[dict]:
    deck = load_slides(slides_path)
    deck_id = deck.get("deck_id") or "deck"
    slides = deck.get("slides", [])
    out = []
    dbid = database_id or os.getenv("NOTION_DATABASE_ID") or "stub-db"
    for i in pick:
        if i >= len(slides): 
            continue
        slide = slides[i]
        title = slide.get("title") or f"{deck_id} - Slide {i+1}"
        blocks = google_slide_to_blocks(slide)
        res = create_page(dbid, title, blocks)
        out.append({"slide_index": i, "title": title, "result": res})
    return out
