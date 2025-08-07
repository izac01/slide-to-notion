# Google Slides to Notion Converter

## Setup
1. Install requirements:
   ```bash
   pip install -r requirements.txt
   ```

2. Place `credentials.json` (Google API OAuth credentials) in the same folder.

3. Run the script:
   ```bash
   python google_slides_to_notion.py
   ```

4. On first run, a browser will open to authorize Google Slides access.

5. Ensure your Notion API token is set in the script.

## Notes
- Updates only when deck changes.
- Syncs slides with thumbnails, text, and formatting to Notion.
- Optimized for visual 1:1 parity.

