from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
import os.path
import pickle
import httpx
from notion_client import Client
import json
from datetime import datetime, timezone, timedelta

# --- CONFIG ---
SCOPES = ['https://www.googleapis.com/auth/presentations.readonly']
DECK_ID = '1BftmE4rYIMuyDDpFY3DYCMQ2G5Nm_BIY7JkoeYds6bI'
PAGE_ID = "240c3514fb56805c9484d1e7b3d0164a"
NOTION_TOKEN = "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"
REVISION_FILE = "revision_state.json"
FORCE_UPDATE = False
BATCH_SIZE = 20

# --- Notion Client ---
notion = Client(auth=NOTION_TOKEN, client=httpx.Client(timeout=20.0))

# --- Google Slides Auth ---
creds = None
if os.path.exists('token.pickle'):
    with open('token.pickle', 'rb') as token:
        creds = pickle.load(token)

if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
    with open('token.pickle', 'wb') as token:
        pickle.dump(creds, token)

service = build('slides', 'v1', credentials=creds)

# --- Fetch Presentation ---
presentation = service.presentations().get(presentationId=DECK_ID).execute()
slides = presentation.get('slides', [])
revision_id = presentation.get("revisionId")
print(f"✅ Found {len(slides)} slides (Revision {revision_id})")

# --- Revision Sync Check ---
now = datetime.now(timezone.utc)
last_revision, last_checked = None, None
if os.path.exists(REVISION_FILE):
    with open(REVISION_FILE, "r") as f:
        data = json.load(f)
        last_revision = data.get("revisionId")
        last_checked = datetime.fromisoformat(data.get("timestamp"))

# --- Helpers ---
def slides_alignment_to_notion(alignment: str) -> str:
    return {"CENTER": "center", "RIGHT": "right", "JUSTIFIED": "justify"}.get(alignment, "left")

def rgb_to_notion_color(rgb: dict, theme_color: str = None) -> str:
    if rgb:
        r = int(rgb.get("red", 0) * 255)
        g = int(rgb.get("green", 0) * 255)
        b = int(rgb.get("blue", 0) * 255)
        return "default" if (r + g + b) / 3 > 128 else "gray"
    if theme_color:
        return {"DARK1": "gray", "LIGHT1": "default", "ACCENT1": "blue",
                "ACCENT2": "red", "ACCENT3": "green"}.get(theme_color, "default")
    return "default"

def append_with_batch(parent_id, blocks):
    for i in range(0, len(blocks), BATCH_SIZE):
        notion.blocks.children.append(parent_id, children=blocks[i:i+BATCH_SIZE])

def notion_page_slides(page_id: str) -> dict:
    slides_dict = {}
    has_more, start_cursor = True, None
    while has_more:
        resp = notion.blocks.children.list(page_id, page_size=100, start_cursor=start_cursor)
        children = resp.get("results", [])
        has_more = resp.get("has_more", False)
        start_cursor = resp.get("next_cursor")
        for c in children:
            if c["type"] == "toggle":
                title = "".join(
                    t.get("text", {}).get("content", "")
                    for t in c.get("toggle", {}).get("rich_text", [])
                )
                if "🗑️" in title:
                    slides_dict[title] = c["id"]
    return slides_dict

def add_slide_to_notion(slide, slide_title, parent_page_id):
    toggle_block = notion.blocks.children.append(
        parent_page_id,
        children=[{
            "object": "block",
            "type": "toggle",
            "toggle": {"rich_text": [{"type": "text", "text": {"content": slide_title}}]}
        }]
    )["results"][0]
    toggle_id = toggle_block["id"]

    slide_id = slide.get('objectId')
    slide_url = f"https://docs.google.com/presentation/d/{DECK_ID}/edit#slide=id.{slide_id}"

    blocks_to_add = []

    # Google Slides link
    blocks_to_add.append({
        "object": "block",
        "type": "paragraph",
        "paragraph": {
            "rich_text": [{
                "type": "text",
                "text": {"content": "🔗 Open in Google Slides", "link": {"url": slide_url}},
                "annotations": {"bold": True}
            }]
        }
    })

    # Thumbnail
    try:
        thumb = service.presentations().pages().getThumbnail(
            presentationId=DECK_ID,
            pageObjectId=slide_id
        ).execute()
        content_url = thumb.get('contentUrl')
        if content_url:
            blocks_to_add.append({
                "object": "block",
                "type": "image",
                "image": {"type": "external", "external": {"url": content_url}}
            })
            print(f"[{slide_title}] Added thumbnail via external URL")
    except Exception as e:
        print(f"[{slide_title}] Error fetching thumbnail: {e}")

    # Text elements
    for element in slide.get('pageElements', []):
        shape = element.get('shape')
        if not shape:
            continue

        for para in shape.get('text', {}).get('textElements', []):
            run = para.get('textRun')
            if not run:
                continue
            content = run.get('content').strip()
            if not content:
                continue

            para_marker = para.get("paragraphMarker", {})
            bullet = para_marker.get("bullet", {})
            bullet_preset = bullet.get("bulletPreset")

            style = run.get("style", {})
            font_size = style.get("fontSize", {}).get("magnitude", 12)
            rgb = style.get("foregroundColor", {}).get("opaqueColor", {}).get("rgbColor")
            theme_color = style.get("foregroundColor", {}).get("opaqueColor", {}).get("themeColor")
            notion_color = rgb_to_notion_color(rgb, theme_color)
            href = style.get("link", {}).get("url") if "link" in style else None

            rich_text = {
                "type": "text",
                "text": {"content": content, "link": {"url": href} if href else None},
                "annotations": {
                    "bold": style.get("bold", False),
                    "italic": style.get("italic", False),
                    "underline": style.get("underline", False),
                    "strikethrough": style.get("strikethrough", False),
                    "code": False,
                    "color": notion_color
                }
            }

            if font_size >= 32:
                block_type = "heading_1"
                block_data = {"rich_text": [rich_text], "text_alignment": "center"}
            elif font_size >= 24:
                block_type = "heading_2"
                block_data = {"rich_text": [rich_text], "text_alignment": "center"}
            elif font_size >= 18:
                block_type = "heading_3"
                block_data = {"rich_text": [rich_text], "text_alignment": "center"}
            elif bullet_preset and "NUMBERED" in bullet_preset:
                block_type = "numbered_list_item"
                block_data = {"rich_text": [rich_text]}
            elif bullet_preset:
                block_type = "bulleted_list_item"
                block_data = {"rich_text": [rich_text]}
            else:
                block_type = "paragraph"
                block_data = {"rich_text": [rich_text]}

            blocks_to_add.append({
                "object": "block",
                "type": block_type,
                block_type: block_data
            })

    if blocks_to_add:
        append_with_batch(toggle_id, blocks_to_add)

    return toggle_id

# --- Sync Report ---
notion_slides = notion_page_slides(PAGE_ID)
deck_slides = [f"🗑️ Slide {i+1}" for i in range(len(slides))]

missing_in_notion = [s for s in deck_slides if s not in notion_slides]
extra_in_notion = [s for s in notion_slides if s not in deck_slides]
matched = [s for s in deck_slides if s in notion_slides]

print("📊 Slide Sync Report")
print(f"  ✅ Matched: {len(matched)}")
print(f"  ❌ Missing in Notion: {len(missing_in_notion)}")
print(f"  ❌ Extra in Notion: {len(extra_in_notion)}")

if not FORCE_UPDATE:
    if last_revision == revision_id and not missing_in_notion and not extra_in_notion:
        print("⏸️ Deck unchanged and Notion already in sync — skipping update.")
        exit()

for slide_title in extra_in_notion:
    block_id = notion_slides[slide_title]
    print(f"🗑️ Removing extra slide in Notion: {slide_title}")
    notion.blocks.delete(block_id)

for i, slide_title in enumerate(deck_slides):
    if slide_title in missing_in_notion:
        slide = slides[i]
        print(f"➕ Adding missing slide: {slide_title}")
        add_slide_to_notion(slide, slide_title, PAGE_ID)

with open(REVISION_FILE, "w") as f:
    json.dump({"revisionId": revision_id, "timestamp": now.isoformat()}, f)
print("✅ Notion updated and revision saved")
