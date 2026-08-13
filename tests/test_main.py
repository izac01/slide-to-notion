import json

import pytest

from main import main
from pipeline import load_slides, run_mvp

DECK = {
    "deck_id": "deck-7",
    "slides": [
        {"title": "One", "elements": [{"type": "text", "content": "alpha"}]},
        {"title": "Two", "elements": [{"type": "text", "content": "beta"}]},
    ],
}


@pytest.fixture
def deck_path(tmp_path, monkeypatch):
    monkeypatch.delenv("NOTION_API_KEY", raising=False)
    monkeypatch.delenv("NOTION_DATABASE_ID", raising=False)
    p = tmp_path / "slides.json"
    p.write_text(json.dumps(DECK), encoding="utf-8")
    return str(p)


def test_load_slides_reads_json(deck_path):
    assert load_slides(deck_path) == DECK


def test_run_mvp_converts_selected_slides(deck_path):
    results = run_mvp(slides_path=deck_path, pick=(0, 1))
    assert [r["title"] for r in results] == ["One", "Two"]
    assert all(r["result"]["url"] == "https://notion.so/stub" for r in results)


def test_run_mvp_ignores_out_of_range_indexes(deck_path):
    results = run_mvp(slides_path=deck_path, pick=(0, 5, 99))
    assert [r["slide_index"] for r in results] == [0]


def test_run_mvp_falls_back_to_deck_id_for_untitled_slides(tmp_path, monkeypatch):
    monkeypatch.delenv("NOTION_API_KEY", raising=False)
    p = tmp_path / "slides.json"
    p.write_text(json.dumps({"deck_id": "deck-7", "slides": [{"elements": []}]}), encoding="utf-8")
    results = run_mvp(slides_path=str(p), pick=(0,))
    assert results[0]["title"] == "deck-7 - Slide 1"


def test_main_runs_end_to_end(deck_path):
    results = main(["--slides", deck_path, "--limit", "2"])
    assert [r["title"] for r in results] == ["One", "Two"]


def test_main_limit_is_respected(deck_path):
    assert len(main(["--slides", deck_path, "--limit", "1"])) == 1
