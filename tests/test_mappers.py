from mappers import element_text, google_slide_to_blocks


def _texts(blocks, kind):
    return [
        rt["text"]["content"]
        for b in blocks
        if b["type"] == kind
        for rt in b[kind]["rich_text"]
    ]


def test_title_becomes_heading():
    blocks = google_slide_to_blocks({"title": "DEMO SLIDE", "elements": []})
    assert _texts(blocks, "heading_2") == ["DEMO SLIDE"]


def test_content_key_is_mapped_to_paragraph():
    """slides_fetcher writes text under "content" — it must not be dropped."""
    slide = {"elements": [{"type": "text", "content": "hello"}]}
    assert _texts(google_slide_to_blocks(slide), "paragraph") == ["hello"]


def test_legacy_text_key_still_works():
    slide = {"elements": [{"type": "text", "text": "hello"}]}
    assert _texts(google_slide_to_blocks(slide), "paragraph") == ["hello"]


def test_image_element_becomes_external_image_block():
    url = "https://example.com/a.png"
    blocks = google_slide_to_blocks({"elements": [{"type": "image", "url": url}]})
    assert blocks[0]["image"]["external"]["url"] == url


def test_element_order_is_preserved():
    slide = {
        "title": "T",
        "elements": [
            {"type": "text", "content": "first"},
            {"type": "image", "url": "https://example.com/a.png"},
            {"type": "text", "content": "second"},
        ],
    }
    assert [b["type"] for b in google_slide_to_blocks(slide)] == [
        "heading_2",
        "paragraph",
        "image",
        "paragraph",
    ]


def test_untyped_elements_are_inferred():
    slide = {"elements": [{"content": "bare"}, {"url": "https://example.com/a.png"}]}
    assert [b["type"] for b in google_slide_to_blocks(slide)] == ["paragraph", "image"]


def test_blank_text_is_skipped():
    slide = {"title": "T", "elements": [{"type": "text", "content": "   "}]}
    assert [b["type"] for b in google_slide_to_blocks(slide)] == ["heading_2"]


def test_empty_slide_gets_placeholder():
    blocks = google_slide_to_blocks({"elements": []})
    assert _texts(blocks, "paragraph") == ["(empty slide)"]


def test_element_text_prefers_content_and_strips():
    assert element_text({"content": "  x  "}) == "x"
    assert element_text({"text": "y"}) == "y"
    assert element_text({"url": "https://example.com/a.png"}) == ""
