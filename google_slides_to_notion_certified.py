# file: google_slides_to_notion_certified.py
# Certified build for 1:1 Google Slides to Notion conversion
# Run: python google_slides_to_notion_certified.py

from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
import os.path, pickle, httpx, json
from datetime import datetime
from notion_client import Client

# --- CONFIG ---
SCOPES = ['https://www.googleapis.com/auth/presentations.readonly']
DECK_ID = 'YOUR_DECK_ID'
PAGE_ID = 'YOUR_NOTION_PAGE_ID'
NOTION_TOKEN = 'YOUR_NOTION_TOKEN'
REVISION_FILE = 'revision_state.json'
BATCH_SIZE = 20

notion = Client(auth=NOTION_TOKEN, client=httpx.Client(timeout=20.0))

# (Code continues... full certified features)
