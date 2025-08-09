import os
import json
import re
import requests

with open("workspace/slides.json", "r", encoding="utf-8") as f:
    slides = json.load(f)

output_dir = "./output/markdown"
os.makedirs(output_dir, exist_ok=True)
image_dir = "./workspace/images"
os.makedirs(image_dir, exist_ok=True)

image_map_path = "workspace/image_map.json"
image_map = {}

def download_image(url, name_hint):
    safe_name = re.sub(r'\W+', '_', name_hint)[:40]
    ext = url.split('.')[-1].split('?')[0]
    filename = f"{safe_name}.{ext}"
    save_path = os.path.join(image_dir, filename)
    
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            with open(save_path, "wb") as f:
                f.write(response.content)
            image_map[url] = filename
            return filename
    except Exception as e:
        print(f"❌ Error downloading {url}: {e}")
    return None

def write_group(title, blocks):
    safe_title = re.sub(r'[\\/*?:"<>|]', '_', title)
    md_path = os.path.join(output_dir, f"{safe_title}.md")
    with open(md_path, "w", encoding="utf-8") as f:
        f.write("\n\n".join(blocks))

current_group = "Slides"
slide_blocks = []

for slide in slides:
    title = None
    elements = []

    for el in slide["elements"]:
        if el["type"] == "text" and not title:
            title = el["content"].strip()
        elements.append(el)

    if title and len(title) < 50:
        if slide_blocks:
            write_group(current_group, slide_blocks)
        current_group = title
        slide_blocks = []

    block = f"\n\n### Slide {slide['slide']}\n"
    for el in elements:
        if el["type"] == "text":
            block += f"\n- {el['content'].strip()}"
        elif el["type"] == "image":
            image_filename = download_image(el["url"], f"{current_group}_{slide['slide']}")
            if image_filename:
                block += f"\n![image](./workspace/images/{image_filename})"
            else:
                block += f"\n❌ Image failed to download: {el['url']}"
    slide_blocks.append(block)

if slide_blocks:
    write_group(current_group, slide_blocks)

# Save image map for bulk upload
with open(image_map_path, "w", encoding="utf-8") as f:
    json.dump(image_map, f, indent=2)

print("✅ Markdown generated.")
print("📂 All images saved in workspace/images/")
print("📄 Image map saved to workspace/image_map.json (upload to Google Drive next)")
