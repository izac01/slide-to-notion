from google_slides_parser import GoogleSlidesParser
from notion_converter import NotionConverter
from typing import List

class BatchConverter:
    def __init__(self, google_slides_parser: GoogleSlidesParser, notion_converter: NotionConverter):
        """
        Initialize the BatchConverter with a GoogleSlidesParser and a NotionConverter.

        Args:
            google_slides_parser (GoogleSlidesParser): The GoogleSlidesParser to be used for parsing the Google Slides.
            notion_converter (NotionConverter): The NotionConverter to be used for converting the parsed content to Notion format.
        """
        self.google_slides_parser = google_slides_parser
        self.notion_converter = notion_converter

    def batch_convert(self, slide_ids: List[str]) -> List[str]:
        """
        This function converts multiple Google Slides to Notion format at once.

        Args:
            slide_ids (List[str]): The IDs of the Google Slides to be converted.

        Returns:
            List[str]: The IDs of the created Notion pages.

        Raises:
            Exception: If an error occurs while converting the slides.
        """
        notion_page_ids = []

        for slide_id in slide_ids:
            try:
                # Parse the Google Slides content
                parsed_content = self.google_slides_parser.parse_slides(slide_id)

                # Convert the parsed content to Notion format and create a new Notion page
                notion_page_id = self.notion_converter.convert_to_notion(parsed_content)

                notion_page_ids.append(notion_page_id)

            except Exception as e:
                print(f"An error occurred while converting the slide with ID {slide_id}: {e}")
                continue

        return notion_page_ids
