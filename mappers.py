"""Map Google Slides -> Notion blocks."""
from typing import Dict, Any, List

def google_slides_to_notion(slide: Dict[str, Any]) -> Dict[str, Any]:
    texts: List[str] = []
    for el in slide.get("elements", []):
        t = el.get("text")
        if isinstance(t, str):
            texts.append(t)
    content = "\n".join(texts) if texts else " "
    return {"type": "paragraph", "paragraph": {"text": [{"content": content}]}}
