from notion.client import NotionClient
from notion.block import HeaderBlock, TextBlock
from typing import Dict

class NotionConverter:
    def __init__(self, token_v2: str):
        """
        Initialize the NotionConverter with a Notion token.

        Args:
            token_v2 (str): The token_v2 of the Notion account.
        """
        try:
            self.notion = NotionClient(token_v2=token_v2)
        except Exception as e:
            print(f"An error occurred while creating the NotionClient object: {e}")
            raise e

    def convert_to_notion(self, parsed_content: Dict) -> str:
        """
        This function converts the parsed Google Slides content into a Notion-compatible format and creates a new Notion page with the converted content.

        Args:
            parsed_content (Dict): The parsed content of the Google Slides.

        Returns:
            str: The ID of the created Notion page.

        Raises:
            Exception: If an error occurs while converting the content or creating the Notion page.
        """
        try:
            # Create a new Notion page
            page = self.notion.pages.add(parent=self.notion.root_page, title="Converted Google Slides")

            # Convert the parsed content into a Notion-compatible format and add it to the new Notion page
            for slide_number, slide_content in parsed_content.items():
                page.children.add_new(HeaderBlock, title=f"Slide {slide_number + 1}")
                for element in slide_content:
                    page.children.add_new(TextBlock, title=element)

            return page.id

        except Exception as e:
            print(f"An error occurred while converting the content to Notion format or creating the Notion page: {e}")
            raise e
