import os
import sys
import subprocess
from pathlib import Path

def write_file(path: str, content: str):
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding="utf-8")
    print(f"📝 Wrote {path}")

def main():
    print("🚀 Running Hardened Slides→Notion Builder")

    # Step 1. Clean old files
    print("🧹 Cleaning old files...")
    for target in [
        "slides_to_notion_converter",
        "slide_to_notion_converter",
        "google_slides_to_notion",
        "test_parser.py",
        "old_notion_api.py",
        "demo_cli.py"
    ]:
        if Path(target).exists():
            if Path(target).is_dir():
                subprocess.run(f"rmdir /s /q {target}", shell=True)
            else:
                Path(target).unlink()
    Path("workspace").mkdir(exist_ok=True)
    print("✅ Cleanup done.")

    # Step 2. Write hardened files
    write_file("workspace/google_slides_parser.py", """\
import logging
from typing import List, Dict, Any

class GoogleSlidesParser:
    def __init__(self, slides_service): self.slides_service = slides_service
    def fetch_presentation(self, presentation_id: str) -> Dict[str, Any]:
        try:
            return self.slides_service.presentations().get(presentationId=presentation_id).execute()
        except Exception as e:
            logging.error(f"Failed to fetch presentation: {e}")
            raise
    def parse_slides(self, presentation: Dict[str, Any]) -> List[Dict[str, Any]]:
        slides_data = []
        for slide in presentation.get("slides", []):
            elements = []
            for element in slide.get("pageElements", []):
                if "shape" in element:
                    text = self._extract_text(element)
                    if text: elements.append({"type": "text", "content": text})
                elif "image" in element:
                    elements.append({"type": "image", "content": element["image"]["contentUrl"]})
            slides_data.append({"elements": elements})
        return slides_data
    def _extract_text(self, element: Dict[str, Any]) -> str:
        return "".join(te["textRun"]["content"]
                       for te in element["shape"]["text"]["textElements"]
                       if "textRun" in te).strip()
""")

    write_file("workspace/notion_converter.py", """\
from typing import List, Dict

class NotionConverter:
    def convert(self, slides_data: List[Dict]) -> List[Dict]:
        blocks = []
        for slide in slides_data:
            for el in slide["elements"]:
                if el["type"] == "text": blocks.append(self._text_block(el["content"]))
                elif el["type"] == "image": blocks.append(self._image_block(el["content"]))
        return blocks
    def _text_block(self, text: str) -> Dict:
        return {"object":"block","type":"paragraph",
                "paragraph":{"text":[{"type":"text","text":{"content":text}}]}}
    def _image_block(self, url: str) -> Dict:
        return {"object":"block","type":"image",
                "image":{"type":"external","external":{"url":url}}}
""")

    write_file("workspace/batch_converter.py", """\
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
""")

    write_file("workspace/ui.py", """\
class UI:
    def prompt_presentation_ids(self): 
        return [x.strip() for x in input("Enter Google Slides IDs: ").split(",") if x.strip()]
    def prompt_notion_page_id(self): 
        return input("Enter target Notion page ID: ").strip()
    def show_progress(self, i, total): 
        print(f"Processing {i}/{total} presentations...")
    def show_done(self): 
        print("✅ Conversion complete! Your slides are now in Notion.")
""")

    write_file("workspace/main.py", """\
import logging
from googleapiclient.discovery import build
from notion_client import Client
from google_slides_parser import GoogleSlidesParser
from notion_converter import NotionConverter
from batch_converter import BatchConverter
from ui import UI

def main():
    logging.basicConfig(level=logging.INFO)
    slides_service = build("slides", "v1")
    notion_client = Client(auth="YOUR_NOTION_API_TOKEN")
    parser, converter = GoogleSlidesParser(slides_service), NotionConverter()
    batch, ui = BatchConverter(parser, converter, notion_client), UI()
    ids, page = ui.prompt_presentation_ids(), ui.prompt_notion_page_id()
    for i, pid in enumerate(ids, 1):
        ui.show_progress(i, len(ids))
        batch.process_presentations([pid], page)
    ui.show_done()

if __name__ == "__main__":
    main()
""")

    write_file("workspace/README.md", "# Google Slides to Notion Converter\nRun `python main.py` to get started.\n")
    write_file("workspace/ONBOARDING.md", "# Onboarding Guide\n1. Get Slides IDs.\n2. Create Notion integration.\n3. Run `python main.py`.\n")
    write_file("workspace/requirements.txt", "google-api-python-client==2.115.0\nnotion-client==2.0.0\n")

    # Step 3. Install dependencies
    print("📦 Installing dependencies...")
    subprocess.run("pip install -r workspace/requirements.txt", shell=True, check=True)

    # Step 4. Smoke test (Windows-safe)
    print("🚦 Running smoke test...")
    import py_compile
    for pyfile in Path("workspace").glob("*.py"):
        try:
            py_compile.compile(pyfile, doraise=True)
            print(f"✅ Compiled {pyfile}")
        except py_compile.PyCompileError as e:
            print(f"❌ Compilation failed: {pyfile}\n{e}")
            sys.exit(1)

    # Step 5. Zip
    print("📦 Creating zip...")
    import zipfile
    with zipfile.ZipFile("workspace_cleaned.zip", "w", zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk("workspace"):
            for file in files:
                fp = os.path.join(root, file)
                zipf.write(fp, os.path.relpath(fp, "workspace"))
    print("✅ Created workspace_cleaned.zip")

if __name__ == "__main__":
    main()
