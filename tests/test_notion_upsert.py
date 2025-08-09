import pytest
from notion_client import upsert

def test_upsert_no_exception():
    try:
        upsert("fake_db", {"type": "paragraph", "paragraph": {"text": [{"content": "x"}]}})
    except Exception as e:
        pytest.fail(f"Unexpected exception: {e}")
