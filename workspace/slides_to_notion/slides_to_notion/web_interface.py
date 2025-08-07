from flask import Flask, request, jsonify
from google_slides_parser import GoogleSlidesParser
from notion_converter import NotionConverter
from batch_converter import BatchConverter

class WebInterface:
    def __init__(self, google_slides_parser: GoogleSlidesParser, notion_converter: NotionConverter, batch_converter: BatchConverter):
        """
        Initialize the WebInterface with a GoogleSlidesParser, a NotionConverter, and a BatchConverter.

        Args:
            google_slides_parser (GoogleSlidesParser): The GoogleSlidesParser to be used for parsing the Google Slides.
            notion_converter (NotionConverter): The NotionConverter to be used for converting the parsed content to Notion format.
            batch_converter (BatchConverter): The BatchConverter to be used for converting multiple slides at once.
        """
        self.google_slides_parser = google_slides_parser
        self.notion_converter = notion_converter
        self.batch_converter = batch_converter
        self.flask = Flask(__name__)

    def run_interface(self):
        """
        This function runs the web interface of the system.
        """
        @self.flask.route('/convert', methods=['POST'])
        def convert():
            """
            This function handles the POST request to convert Google Slides to Notion format.

            Returns:
                str: The ID of the created Notion page.
            """
            slide_id = request.json.get('slide_id')
            parsed_content = self.google_slides_parser.parse_slides(slide_id)
            notion_page_id = self.notion_converter.convert_to_notion(parsed_content)
            return jsonify({'notion_page_id': notion_page_id})

        @self.flask.route('/batch_convert', methods=['POST'])
        def batch_convert():
            """
            This function handles the POST request to convert multiple Google Slides to Notion format at once.

            Returns:
                List[str]: The IDs of the created Notion pages.
            """
            slide_ids = request.json.get('slide_ids')
            notion_page_ids = self.batch_converter.batch_convert(slide_ids)
            return jsonify({'notion_page_ids': notion_page_ids})

        self.flask.run(debug=True)
