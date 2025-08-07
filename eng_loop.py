import time
import traceback
import sys
import requests
import openai
import random

# --- CONFIG ---
PRIMARY_MODEL = "gpt-4o"        # Strong model
FALLBACK_MODEL = "gpt-4o-mini"  # Cheaper fallback
CADENCE = 300  # seconds (5 minutes)
API_KEY = ""  # <-- put your real key
TARGET_URL = "https://example.com"  # Link to ping

openai.api_key = API_KEY

def ping_site(url):
    """Check if the target URL is reachable."""
    try:
        resp = requests.get(url, timeout=10)
        return resp.status_code == 200
    except Exception as e:
        return False

def request_code_update(changelog, model=PRIMARY_MODEL):
    """Request GPT update with fallback."""
    try:
        resp = openai.ChatCompletion.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are Eng Director helping with code parity and improvements."},
                {"role": "user", "content": changelog}
            ],
            temperature=0.2
        )
        return resp.choices[0].message["content"]
    except Exception as e:
        if model != FALLBACK_MODEL:
            return request_code_update(changelog, model=FALLBACK_MODEL)
        raise

def run_loop():
    attempt = 1
    changelog = "Start monitoring."
    print("🚀 Monitor started.")

    while True:
        print(f"[{time.asctime()}] 🔄 Iteration {attempt} started...")

        if ping_site(TARGET_URL):
            print(f"✅ {TARGET_URL} is UP.")
        else:
            print(f"⚠️ {TARGET_URL} seems DOWN. Calling GPT...")
            try:
                updated_code = request_code_update(
                    f"{TARGET_URL} is down. Please suggest diagnostics."
                )
                with open("eng_log.txt", "a", encoding="utf-8") as log:
                    log.write(f"[{time.asctime()}] Iteration {attempt}: GPT response:\n{updated_code}\n\n")
            except Exception as e:
                err_details = traceback.format_exc()
                with open("eng_log.txt", "a", encoding="utf-8") as log:
                    log.write(f"[{time.asctime()}] ERROR: {err_details}\n")

        wait_time = random.randint(CADENCE, CADENCE + 300)  # Randomize between 5–10 mins
        print(f"⏳ Waiting {wait_time//60} minutes...")
        time.sleep(wait_time)
        attempt += 1

if __name__ == "__main__":
    try:
        run_loop()
    except KeyboardInterrupt:
        print("\n🛑 Monitoring stopped by user.")
        sys.exit(0)
