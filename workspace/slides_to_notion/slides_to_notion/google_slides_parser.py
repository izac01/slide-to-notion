import gspread
from typing import Dict

class GoogleSlidesParser:
    def __init__(self):
        self.gspread = gspread.service_account()

    def parse_slides(self, slide_id: str) -> Dict:
        """
        This function fetches the Google Slides content using the Google Slides API and parses it into a dictionary.

        Args:
            slide_id (str): The ID of the Google Slides to be parsed.

        Returns:
            dict: The parsed content of the Google Slides.

        Raises:
            Exception: If an error occurs while parsing the slides.
        """
        try:
            slide = self.gspread.open_by_key(slide_id)
            parsed_content = {}

            for i, individual_slide in enumerate(slide.slides):
                elements = individual_slide.get_all_elements()
                parsed_content[i] = [element.text for element in elements]

            return parsed_content

        except Exception as e:
            print(f"An error occurred while parsing the slides: {e}")
            raise e
