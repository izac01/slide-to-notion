import hashlib

from utils import ensure_dir, sha256_bytes


def test_sha256_bytes_returns_sha256_hex():
    h = sha256_bytes(b"abc")
    assert isinstance(h, str) and len(h) == 64
    assert h == hashlib.sha256(b"abc").hexdigest()


def test_sha256_bytes_is_stable():
    assert sha256_bytes(b"abc") == sha256_bytes(b"abc")
    assert sha256_bytes(b"abc") != sha256_bytes(b"abd")


def test_ensure_dir_creates_nested_path(tmp_path):
    target = tmp_path / "a" / "b"
    ensure_dir(str(target))
    assert target.is_dir()


def test_ensure_dir_is_idempotent(tmp_path):
    target = tmp_path / "a"
    ensure_dir(str(target))
    ensure_dir(str(target))
    assert target.is_dir()
