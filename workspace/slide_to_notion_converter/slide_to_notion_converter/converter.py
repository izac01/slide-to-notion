from typing import Dict
from file_manager import FileManager
from environment_manager import EnvironmentManager
from notion.client import NotionClient
from notion.block import TextBlock

class Converter:
    """
    This class is responsible for converting PowerPoint slides to Notion pages.
    """
    def __init__(self, file_manager: FileManager, environment_manager: EnvironmentManager):
        """
        Initialize the Converter with a FileManager and an EnvironmentManager.
        """
        self.file_manager = file_manager
        self.environment_manager = environment_manager

    def convert(self, slide_path: str, notion_path: str, token: str, page_url: str) -> str:
        """
        Convert the PowerPoint slides to Notion pages.
        """
        # Set up the environment
        self.environment_manager.setup_environment()

        # Read the slide data
        slide_data = self.file_manager.read_file(slide_path)

        # Convert the slide data to Notion data
        notion_data = self._convert_to_notion(slide_data, token, page_url)

        # Write the Notion data to a file
        self.file_manager.write_file(notion_path, notion_data)

        # Clean up the environment
        self.environment_manager.cleanup_environment()

        return 'Conversion successful'

    def _convert_to_notion(self, slide_data: Dict, token: str, page_url: str) -> Dict:
        """
        Convert the slide data to Notion data.
        """
        notion_data = {}
        client = NotionClient(token_v2=token)
        page = client.get_block(page_url)

        for i, slide in slide_data.items():
            new_child = page.children.add_new(TextBlock, title=f"Slide {i+1}")
            for text in slide:
                new_child.children.add_new(TextBlock, title=text)
            notion_data[i] = new_child.get_browseable_url()

        return notion_data
