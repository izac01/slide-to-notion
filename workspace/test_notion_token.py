import os
from notion_client import Client

def main():
    token = os.getenv("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")
    if not token:
        print("❌ NOTION_TOKEN environment variable is not set.")
        return

    notion = Client(auth=token)
    try:
        user = notion.users.me()
        print("✅ Token works for:", user.get("name", "Unknown"))
    except Exception as e:
        print("❌ Token invalid:", e)

if __name__ == "__main__":
    main()
