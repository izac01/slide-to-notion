import json

raw_path = "workspace/slides.json"
fixed_path = "workspace/slides_fixed.json"

with open(raw_path, "r", encoding="utf-8") as f:
    try:
        data = json.load(f)
    except json.JSONDecodeError:
        # Try to decode as stringified JSON
        f.seek(0)
        raw_string = f.read()
        try:
            data = json.loads(json.loads(raw_string))
        except Exception as e:
            print(f"❌ Failed to parse nested JSON: {e}")
            exit()

# Validate structure
if isinstance(data, list) and isinstance(data[0], dict) and "elements" in data[0]:
    with open(fixed_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print("✅ Fixed JSON written to slides_fixed.json")
else:
    print("❌ Unexpected JSON structure.")
