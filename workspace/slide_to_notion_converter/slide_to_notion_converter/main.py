from tkinter import Tk
from converter import Converter
from ui import UI
from file_manager import FileManager
from environment_manager import EnvironmentManager

class Main:
    """
    This class is the entry point of the application and interacts with Converter and UI classes.
    """
    def __init__(self, root: Tk, slide_path: str, notion_path: str, token: str, page_url: str):
        """
        Initialize the Main with a tkinter root widget, slide path, notion path, token and page url.
        """
        self.root = root
        self.slide_path = slide_path
        self.notion_path = notion_path
        self.token = token
        self.page_url = page_url
        self.file_manager = FileManager()
        self.environment_manager = EnvironmentManager()
        self.converter = Converter(self.file_manager, self.environment_manager)
        self.ui = UI(self.root)

    def main(self) -> str:
        """
        Start the conversion process and display the progress.
        """
        try:
            # Start the conversion
            message = self.converter.convert(self.slide_path, self.notion_path, self.token, self.page_url)

            # Display the progress
            self.ui.display_progress(1.0)

            return message
        except Exception as e:
            # Display the error message
            self.ui.display_error(str(e))

if __name__ == "__main__":
    root = Tk()
    slide_path = "path_to_your_pptx_file"
    notion_path = "path_to_your_notion_file"
    token = "your_notion_token"
    page_url = "your_notion_page_url"
    main = Main(root, slide_path, notion_path, token, page_url)
    print(main.main())
    root.mainloop()
