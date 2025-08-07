import logging
from typing import List

class BatchConverter:
    def __init__(self, parser, converter, notion_client):
        self.parser, self.converter, self.notion_client = parser, converter, notion_client
    def process_presentations(self, ids: List[str], page: str):
        for pid in ids:
            try:
                pres = self.parser.fetch_presentation(pid)
                slides = self.parser.parse_slides(pres)
                blocks = self.converter.convert(slides)
                for b in blocks: self.notion_client.blocks.children.append(page, b)
            except Exception as e:
                logging.error(f"Error processing {pid}: {e}")
