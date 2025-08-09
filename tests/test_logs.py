import pytest
from logs import log_info, log_error

def test_log_info_no_exception():
    try:
        log_info("msg")
    except Exception as e:
        pytest.fail(f"Unexpected exception: {e}")

def test_log_error_no_exception():
    try:
        log_error("msg")
    except Exception as e:
        pytest.fail(f"Unexpected exception: {e}")
