class UI:
    def prompt_presentation_ids(self): 
        return [x.strip() for x in input("Enter Google Slides IDs: ").split(",") if x.strip()]
    def prompt_notion_page_id(self): 
        return input("Enter target Notion page ID: ").strip()
    def show_progress(self, i, total): 
        print(f"Processing {i}/{total} presentations...")
    def show_done(self): 
        print("✅ Conversion complete! Your slides are now in Notion.")
