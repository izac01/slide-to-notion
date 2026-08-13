# Google Slides to Notion Converter

Converts slides into Notion pages: one page per slide, with the slide title as a
heading followed by its text and image blocks.

## Setup

1. Install requirements:
   ```bash
   pip install -r requirements.txt
   ```

2. Place `credentials.json` (Google API OAuth credentials) in the same folder.

3. Configure Notion via environment variables:
   ```bash
   export NOTION_API_KEY=secret_...
   export NOTION_DATABASE_ID=...
   ```

## Run

```bash
python main.py --slides workspace/slides.json --limit 3
```

| Flag | Default | Meaning |
| --- | --- | --- |
| `--slides` | `workspace/slides.json` | path to the slides JSON |
| `--database-id` | `$NOTION_DATABASE_ID` | target Notion database |
| `--limit` | `3` | how many slides to convert |

With no `NOTION_API_KEY` set, the run is offline: it prints the Notion payload it
*would* POST and returns a stub page instead of uploading. This is the default
way to inspect output without touching a real workspace.

## Slides JSON format

`slides/slides_fetcher.py` writes this shape:

```json
{
  "deck_id": "optional-deck-id",
  "slides": [
    {
      "title": "DEMO SLIDE",
      "elements": [
        { "type": "text",  "content": "some text" },
        { "type": "image", "url": "https://example.com/a.png" }
      ]
    }
  ]
}
```

Text elements may use either `content` or `text`. Elements without an explicit
`type` are inferred from their keys. Slides with no title fall back to
`"<deck_id> - Slide <n>"`.

## Tests

```bash
pip install pytest
python -m pytest
```

## Notes

- Element order is preserved when mapping a slide to Notion blocks.
- Images are linked as external URLs; uploading them to Notion is not done yet.
