# file: google_slides_to_notion.py
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
import os.path
import pickle
import httpx
from notion_client import Client
import json
from datetime import datetime, timedelta

# --- CONFIG ---
SCOPES = ['https://www.googleapis.com/auth/presentations.readonly']
DECK_ID = '1BftmE4rYIMuyDDpFY3DYCMQ2G5Nm_BIY7JkoeYds6bI'
PAGE_ID = "240c3514fb56805c9484d1e7b3d0164a"
NOTION_TOKEN = "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"
REVISION_FILE = "revision_state.json"
FORCE_UPDATE = False

# --- Notion Client ---
notion = Client(auth=NOTION_TOKEN, client=httpx.Client(timeout=15.0))

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

# --- Check Refresh Limit ---
now = datetime.utcnow()
last_revision = None
last_checked = None

if os.path.exists(REVISION_FILE):
    with open(REVISION_FILE, "r") as f:
        data = json.load(f)
        last_revision = data.get("revisionId")
        last_checked = datetime.fromisoformat(data.get("timestamp"))

# --- Helpers ---
def slides_alignment_to_notion(alignment: str) -> str:
    mapping = {"CENTER": "center", "RIGHT": "right", "JUSTIFIED": "justify"}
    return mapping.get(alignment, "left")

def rgb_to_notion_color(rgb: dict, theme_color: str) -> str:
    if rgb:
        r = int(rgb.get("red", 0) * 255)
        g = int(rgb.get("green", 0) * 255)
        b = int(rgb.get("blue", 0) * 255)
        return "default" if (r + g + b) / 3 > 128 else "gray"
    if theme_color:
        theme_mapping = {
            "DARK1": "gray",
            "LIGHT1": "default",
            "ACCENT1": "blue",
            "ACCENT2": "red",
            "ACCENT3": "green",
        }
        return theme_mapping.get(theme_color, "default")
    return "default"

def background_to_callout_color(bg_color: dict) -> str:
    if not bg_color:
        return "default"
    rgb = bg_color.get("opaqueColor", {}).get("rgbColor")
    if rgb:
        r = int(rgb.get("red", 1) * 255)
        g = int(rgb.get("green", 1) * 255)
        b = int(rgb.get("blue", 1) * 255)
        return "gray" if (r + g + b) / 3 < 128 else "default"
    return "default"

def notion_page_slides(page_id: str) -> dict:
    """Return dict of {slide_title: block_id} for all 🗑️ slides in Notion."""
    slides_dict = {}
    has_more = True
    start_cursor = None
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
    """Create a toggle in Notion for a slide, with link + thumbnail."""
    toggle_block = notion.blocks.children.append(
        parent_page_id,
        children=[{
            "object": "block",
            "type": "toggle",
            "toggle": {"rich_text": [{"type": "text", "text": {"content": slide_title}}]}
        }]
    )["results"][0]
    toggle_id = toggle_block["id"]

    # Slide link
    slide_id = slide.get('objectId')
    slide_url = f"https://docs.google.com/presentation/d/{DECK_ID}/edit#slide=id.{slide_id}"
    notion.blocks.children.append(toggle_id, children=[{
        "object": "block",
        "type": "paragraph",
        "paragraph": {
            "rich_text": [{
                "type": "text",
                "text": {"content": "🔗 Open in Google Slides", "link": {"url": slide_url}},
                "annotations": {"bold": True}
            }]
        }
    }])

    # Thumbnail
    try:
        thumb = service.presentations().pages().getThumbnail(
            presentationId=DECK_ID,
            pageObjectId=slide_id,
            thumbnailProperties={'thumbnailSize': 'LARGE'}
        ).execute()
        content_url = thumb.get('contentUrl')
        image_block = {
            "object": "block",
            "type": "image",
            "image": {"type": "external", "external": {"url": content_url}}
        }
        notion.blocks.children.append(toggle_id, children=[image_block])
        print(f"[{slide_title}] Added thumbnail via external URL")
    except Exception as e:
        print(f"[{slide_title}] Error fetching thumbnail: {e}")

    return toggle_id

# --- Verify Notion Page vs Deck ---
notion_slides = notion_page_slides(PAGE_ID)
deck_slides = [f"🗑️ Slide {i+1}" for i in range(len(slides))]

missing_in_notion = [s for s in deck_slides if s not in notion_slides]
extra_in_notion = [s for s in notion_slides if s not in deck_slides]
matched = [s for s in deck_slides if s in notion_slides]

print("📊 Slide Sync Report")
print(f"  ✅ Matched: {len(matched)}")
print(f"  ❌ Missing in Notion: {len(missing_in_notion)}")
print(f"  ❌ Extra in Notion: {len(extra_in_notion)}")

# --- Always sync if out of sync ---
if not FORCE_UPDATE:
    if last_revision == revision_id and not missing_in_notion and not extra_in_notion:
        print("⏸️ Deck unchanged and Notion already in sync — skipping update.")
        exit()

# --- Delete extra slides ---
for slide_title in extra_in_notion:
    block_id = notion_slides[slide_title]
    print(f"🗑️ Removing extra slide in Notion: {slide_title}")
    notion.blocks.delete(block_id)

# --- Add missing slides ---
for i, slide_title in enumerate(deck_slides):
    if slide_title in missing_in_notion:
        slide = slides[i]
        print(f"➕ Adding missing slide: {slide_title}")
        add_slide_to_notion(slide, slide_title, PAGE_ID)

# --- Save revision only if synced ---
if missing_in_notion or extra_in_notion or FORCE_UPDATE:
    with open(REVISION_FILE, "w") as f:
        json.dump({"revisionId": revision_id, "timestamp": now.isoformat()}, f)
    print("✅ Notion updated and revision saved")
else:
    print("⏸️ No changes applied; Notion already matches deck")
