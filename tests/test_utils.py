from utils import calculate_hash

def test_calculate_hash_returns_sha256_hex():
    h = calculate_hash({"a": 1})
    assert isinstance(h, str) and len(h) == 64
