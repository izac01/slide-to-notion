from mappers import google_slides_to_notion

def test_google_slides_to_notion_returns_dict():
    notion_block = google_slides_to_notion({"elements": [{"text": "Hello"}, {"text": "World"}]})
    assert isinstance(notion_block, dict)
    assert "paragraph" in notion_block
