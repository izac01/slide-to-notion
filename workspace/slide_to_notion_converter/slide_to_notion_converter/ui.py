import tkinter as tk
from tkinter import messagebox

class UI:
    """
    This class is responsible for displaying progress and error messages.
    """
    def __init__(self, root: tk.Tk):
        """
        Initialize the UI with a tkinter root widget.
        """
        self.root = root
        self.progress_bar = tk.Scale(self.root, from_=0, to=1, orient=tk.HORIZONTAL)
        self.progress_bar.pack()

    def display_progress(self, progress: float):
        """
        Display the progress of the conversion.
        """
        self.progress_bar.set(progress)
        self.root.update()

    def display_error(self, message: str):
        """
        Display an error message.
        """
        messagebox.showerror("Error", message)
