from slides_client import fetch_presentations, parse_slide

def test_fetch_presentations_returns_list_of_dicts():
    presentations = fetch_presentations("fake_auth_client")
    assert isinstance(presentations, list)
    assert all(isinstance(p, dict) for p in presentations)

def test_parse_slide_returns_dict():
    parsed = parse_slide({"elements": [{"text": "Hi"}]})
    assert isinstance(parsed, dict)
