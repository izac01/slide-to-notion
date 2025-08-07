import logging

class NotionConverter:
    def __init__(self, notion_client, page_id):
        self.notion = notion_client
        self.page_id = page_id

    def push_slides(self, slides: list):
        """Pushes Google Slides content into Notion blocks."""
        children = []

        for idx, slide in enumerate(slides, 1):
            try:
                slide_elements = slide.get("pageElements", [])
                text_content = []

                for element in slide_elements:
                    shape = element.get("shape", {})
                    text = shape.get("text", {}).get("textElements", [])

                    for t in text:
                        if "textRun" in t:
                            text_content.append(t["textRun"].get("content", "").strip())

                if not text_content:
                    text_content = [f"Slide {idx}: (no text found)"]

                children.append({
                    "object": "block",
                    "type": "paragraph",
                    "paragraph": {
                        "rich_text": [{"type": "text", "text": {"content": " ".join(text_content)}}]
                    },
                })

            except Exception as e:
                logging.error(f"❌ Failed to process slide {idx}: {e}")

        try:
            self.notion.blocks.children.append(
                self.page_id,
                children=children,
            )
            logging.info("✅ Successfully pushed slides to Notion")
        except Exception as e:
            logging.error(f"❌ Failed to push slides to Notion: {e}")
