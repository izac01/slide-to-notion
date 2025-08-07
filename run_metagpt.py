import os
import shutil
import subprocess
import sys
import yaml

CONFIG_DIR = os.path.expanduser("~/.metagpt")
CONFIG_PATH = os.path.join(CONFIG_DIR, "config2.yaml")
BACKUP_PATH = os.path.join(CONFIG_DIR, "config2.bak")

DEFAULT_CONFIG = {
    "llm": {
        "api_type": "openai",
        "api_key": None,  # Will be set dynamically
        "model": "gpt-4",
        "base_url": "https://api.openai.com/v1"
    },
    "investment": 1,
    "n_round": 1
}

def safe_backup_config():
    if os.path.exists(CONFIG_PATH):
        try:
            if os.path.exists(BACKUP_PATH):
                os.remove(BACKUP_PATH)
            shutil.copy(CONFIG_PATH, BACKUP_PATH)
            print(f"📦 Existing configuration file backed up at {BACKUP_PATH}")
        except Exception as e:
            print(f"⚠️ Warning: Could not backup config ({e}). Continuing anyway.")

def ensure_config():
    os.makedirs(CONFIG_DIR, exist_ok=True)
    config = DEFAULT_CONFIG.copy()

    if os.path.exists(CONFIG_PATH):
        try:
            with open(CONFIG_PATH, "r") as f:
                user_config = yaml.safe_load(f) or {}
            config.update(user_config)
        except Exception as e:
            print(f"⚠️ Warning: Could not read config file ({e}). Using defaults.")

    api_key = os.environ.get("OPENAI_API_KEY") or config["llm"].get("api_key")
    if not api_key or api_key == "YOUR_API_KEY_HERE":
        api_key = input("🔑 Please enter your OpenAI API key: ").strip()
        os.environ["OPENAI_API_KEY"] = api_key

    config["llm"]["api_key"] = api_key

    with open(CONFIG_PATH, "w") as f:
        yaml.dump(config, f)
    print(f"✅ Config saved to {CONFIG_PATH}")

def ensure_dependencies():
    requirements = {
        "typing-extensions==4.9.0": "typing_extensions",
        "httpx==0.26.0": "httpx",
        "pydantic==2.6.4": "pydantic",
        "tqdm==4.66.2": "tqdm",
        "semantic-kernel==0.4.3.dev0": "semantic_kernel",
        "openai==1.6.1": "openai",
        "agentops": "agentops"
    }

    print("🛠 Running MetaGPT hardened launcher...")
    for req, module in requirements.items():
        try:
            __import__(module)
            print(f"✅ {req} is already installed.")
        except ImportError:
            print(f"🔧 Installing missing dependency: {req}")
            subprocess.check_call([sys.executable, "-m", "pip", "install", req])

def main():
    ensure_dependencies()
    safe_backup_config()
    ensure_config()

    idea = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else None
    if idea:
        print(f"🚀 Launching MetaGPT with idea: {idea}")
        try:
            subprocess.call(["metagpt", idea])
        except Exception as e:
            print(f"❌ MetaGPT crashed: {e}")
    else:
        print("🚀 Launching MetaGPT interactive mode...")
        subprocess.call(["metagpt"])

if __name__ == "__main__":
    main()
