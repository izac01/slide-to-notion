import json
import os

JSON_PATH = './workspace/slides.json'

# Replace with your actual image filename → Drive ID mapping
drive_image_map = {
    "anima.jpg": "1UOeSkCrT9jZzQz0rWyDl9ubJUsaEzmg9",
    "augmentcards.jpg": "1x9CTTbfH29LKuZ9-L0bgLyKr5nNPTWUw",
    "boss.jpg": "1hzVxFX2D3RgT43EZNSIrzUE2cyYjiyFr",
    # Add all image mappings here...
}

def get_drive_url(file_id):
    return f"https://drive.google.com/uc?export=view&id={file_id}"

with open(JSON_PATH, "r", encoding="utf-8") as f:
    try:
        slides = json.load(f)
    except json.JSONDecodeError as e:
        print(f"❌ Failed to parse JSON: {e}")
        exit()

modified = False

for slide in slides:
    if isinstance(slide, dict) and "elements" in slide:
        for el in slide["elements"]:
            if isinstance(el, dict) and "path" in el:
                filename = os.path.basename(el["path"])
                if filename in drive_image_map:
                    el["path"] = get_drive_url(drive_image_map[filename])
                    modified = True
                else:
                    print(f"⚠️ Missing mapping for: {filename}")

if modified:
    with open(JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(slides, f, indent=2, ensure_ascii=False)
    print("✅ Image links updated successfully.")
else:
    print("ℹ️ No matching images found to update.")
