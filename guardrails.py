import json, os, sys, time
from typing import Any, Dict

def safe_print(*a, **k):
    try:
        print(*a, **k)
    except Exception:
        sys.stdout.write(( " ".join(map(str,a)) + "\n").encode("utf-8","replace").decode("utf-8","replace"))

def strict_env(name: str, default: str | None = None) -> str:
    v = os.getenv(name, default)
    if v is None or (isinstance(v,str) and v.strip()==""):
        raise RuntimeError(f"Missing required env: {name}")
    return v

def defensive_json(x: Any) -> str:
    return json.dumps(x, ensure_ascii=False, sort_keys=True, default=str)

def retry(fn, *, tries=5, base=0.5, factor=2.0, exceptions=(Exception,)):
    def wrapper(*args, **kwargs):
        delay = base
        for i in range(tries):
            try:
                return fn(*args, **kwargs)
            except exceptions as e:
                if i == tries-1: raise
                time.sleep(delay); delay *= factor
    return wrapper
