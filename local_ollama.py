import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "deepseek-coder:6.7b"

def llm(prompt: str, max_tokens: int = 800, temperature: float = 0.2) -> str:
    r = requests.post(OLLAMA_URL, json={
        "model": MODEL,
        "prompt": prompt,
        "stream": False,
        "options": {"temperature": temperature, "num_predict": max_tokens}
    }, timeout=600)
    r.raise_for_status()
    return r.json().get("response", "").strip()
