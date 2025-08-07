import logging

class GoogleSlidesParser:
    def __init__(self, service):
        self.service = service

    def extract_presentation_id(self, link: str) -> str:
        """Extracts the Google Slides presentation ID from a full link."""
        try:
            if "docs.google.com/presentation/d/" not in link:
                raise ValueError("Not a valid Google Slides link")
            return link.split("/d/")[1].split("/")[0]
        except Exception as e:
            logging.error(f"❌ Invalid Google Slides link provided: {link} ({e})")
            return None

    def fetch_presentation(self, presentation_id: str):
        """Fetch presentation details using the Google Slides API."""
        try:
            return self.service.presentations().get(presentationId=presentation_id).execute()
        except Exception as e:
            logging.error(f"❌ Failed to fetch presentation {presentation_id}: {e}")
            return None

    def parse_slides(self, presentation: dict):
        """Extract slide information from the presentation."""
        try:
            slides = presentation.get("slides", [])
            logging.info(f"📝 Parsed {len(slides)} slides")
            return slides
        except Exception as e:
            logging.error(f"❌ Error parsing presentation: {e}")
            return []
