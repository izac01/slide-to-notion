import pytest
from main import main

def test_main_no_exception():
    try:
        main("fake_auth", "fake_db")
    except Exception as e:
        pytest.fail(f"Unexpected exception: {e}")
