import os
import json
import requests
import mimetypes
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2 import service_account

SCOPES = ["https://www.googleapis.com/auth/drive"]
SERVICE_ACCOUNT_FILE = "credentials.json"

def read_config():
    with open("workspace/config.json", "r", encoding="utf-8") as f:
        return json.load(f)

def get_drive_service():
    creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES
    )
    return build("drive", "v3", credentials=creds)

def upload_to_drive(image_path, folder_id, service):
    file_metadata = {
        "name": os.path.basename(image_path),
        "parents": [folder_id]
    }
    mime_type, _ = mimetypes.guess_type(image_path)
    media = MediaFileUpload(image_path, mimetype=mime_type)
    file = service.files().create(body=file_metadata, media_body=media, fields="id").execute()
    
    # Make the file public
    service.permissions().create(
        fileId=file["id"],
        body={"role": "reader", "type": "anyone"},
    ).execute()

    # Return sharable link
    return f"https://drive.google.com/uc?id={file['id']}"

def md_to_blocks(content, config, drive_service):
    lines = content.strip().split("\n")
    blocks = []
    for line in lines:
        line = line.strip()
        if line.startswith("###"):
            blocks.append({
                "object": "block",
                "type": "heading_3",
                "heading_3": {
                    "rich_text": [{"type": "text", "text": {"content": line.replace("###", "").strip()}}]
                }
            })
        elif line.startswith("- "):
            blocks.append({
                "object": "block",
                "type": "bulleted_list_item",
                "bulleted_list_item": {
                    "rich_text": [{"type": "text", "text": {"content": line[2:].strip()}}]
                }
            })
        elif line.startswith("!"):
            start = line.find("(") + 1
            end = line.find(")")
            image_path = line[start:end].strip()
            if os.path.exists(image_path):
                public_url = upload_to_drive(image_path, config["google_drive_folder_id"], drive_service)
            else:
                public_url = "https://via.placeholder.com/512x256?text=Missing+Image"
            blocks.append({
                "object": "block",
                "type": "image",
                "image": {
                    "type": "external",
                    "external": {
                        "url": public_url
                    }
                }
            })
    return blocks

def create_notion_page(title, blocks, config):
    url = "https://api.notion.com/v1/pages"
    headers = {
        "Authorization": f"Bearer {config['notion_token']}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28"
    }

    data = {
        "parent": {"page_id": config["notion_page_id"]},
        "properties": {
            "title": [
                {"type": "text", "text": {"content": title}}
            ]
        },
        "children": blocks
    }

    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        print(f"✅ Created page: {title}")
    else:
        print(f"❌ Failed to create {title} → {response.status_code}: {response.text}")

def main():
    config = read_config()
    drive_service = get_drive_service()
    md_folder = "./output/markdown"
    for file in os.listdir(md_folder):
        if file.endswith(".md"):
            with open(os.path.join(md_folder, file), "r", encoding="utf-8") as f:
                content = f.read()
            title = file.replace(".md", "").replace("_", " ")
            blocks = md_to_blocks(content, config, drive_service)
            create_notion_page(title, blocks, config)

if __name__ == "__main__":
    main()
