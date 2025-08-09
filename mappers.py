# mappers.py (append)

MVP_STYLE = {
    "header_color": {"color": "blue"},
    "header_size": "heading_2",  # Notion supports heading_1/2/3
    "paragraph_color": {"color": "default"},
    "font_hint": "sans",  # doc hint; Notion API doesn't expose font choice per block
}

def _rich_text(text: str, color: str = "default"):
    return [{"type": "text", "text": {"content": text}, "annotations": {"color": color}}]

def heading_block(text: str):
    # heading_2 to match style; easy to tweak later
    return {"type": "heading_2", "heading_2": {"rich_text": _rich_text(text, "blue")}}

def paragraph_block(text: str):
    return {"type": "paragraph", "paragraph": {"rich_text": _rich_text(text)}}

def image_block_external(url: str):
    # For MVP use external URL; later we’ll upload and switch to "file"
    return {"type": "image", "image": {"type": "external", "external": {"url": url}}}

def google_slide_to_blocks(slide: dict) -> list[dict]:
    """Very dumb mapper: first text element becomes heading; rest paragraphs; images added in order."""
    blocks: list[dict] = []
    title = slide.get("title") or ""
    if title:
        blocks.append(heading_block(title))

    # Elements can be {"type":"text","text":"..."} or {"type":"image","url": "..."} for MVP
    for el in slide.get("elements", []):
        t = el.get("type") or ("text" if "text" in el else "image" if "url" in el else None)
        if t == "text":
            txt = el.get("text", "").strip()
            if txt:
                blocks.append(paragraph_block(txt))
        elif t == "image":
            url = el.get("url")
            if url:
                blocks.append(image_block_external(url))
    if not blocks:
        blocks.append(paragraph_block("(empty slide)"))
    return blocks
