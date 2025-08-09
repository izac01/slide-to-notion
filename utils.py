# --- MVP helpers ---
from pathlib import Path
import hashlib

def sha256_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()

def ensure_dir(path: str) -> None:
    Path(path).mkdir(parents=True, exist_ok=True)
