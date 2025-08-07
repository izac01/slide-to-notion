import os
import logging
from notion_client import Client
from googleapiclient.discovery import build
from google.oauth2 import service_account
from google_slides_parser import GoogleSlidesParser
from notion_converter import NotionConverter

logging.basicConfig(level=logging.INFO)

def main():
    try:
        creds = service_account.Credentials.from_service_account_file(
            "service_account.json",
            scopes=["https://www.googleapis.com/auth/presentations.readonly"]
        )
        slides_service = build("slides", "v1", credentials=creds)
        logging.info("✅ Authenticated with service_account.json")
    except Exception as e:
        logging.error(f"❌ Failed to authenticate with Google: {e}")
        return

    notion_token = os.getenv("NOTION_TOKEN")
    notion_page_id = os.getenv("NOTION_PAGE_ID")
    if not notion_token or not notion_page_id:
        logging.error("❌ NOTION_TOKEN or NOTION_PAGE_ID not set")
        return

    notion_client = Client(auth=notion_token)
    logging.info("✅ Notion client initialized")

    links = input("Paste one or more Google Slides links (comma-separated):\n").strip().split(",")
    parser = GoogleSlidesParser(slides_service)
    converter = NotionConverter(notion_client, notion_page_id)

    for i, link in enumerate(links, start=1):
        link = link.strip()
        logging.info(f"Processing {i}/{len(links)} presentations...")

        presentation_id = parser.extract_presentation_id(link)
        if not presentation_id:
            logging.warning(f"⚠️ Skipping invalid link: {link}")
            continue

        presentation = parser.fetch_presentation(presentation_id)
        if not presentation:
            continue

        slides = parser.parse_slides(presentation)
        if not slides:
            continue

        try:
            converter.push_slides(slides)
            logging.info(f"✅ Successfully pushed slides to Notion")
        except Exception as e:
            logging.error(f"Error processing {presentation_id}: {e}")

    logging.info("✅ Conversion complete! Your slides are now in Notion.")

if __name__ == "__main__":
    main()
