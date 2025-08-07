# Importing required packages
from mermaid import mermaid

class Diagram:
    """
    This class is responsible for creating a simple diagram using mermaid syntax.
    """
    def __init__(self):
        """
        Constructor for the Diagram class.
        """
        self.diagram = ''

    def create_diagram(self) -> str:
        """
        This function creates a simple diagram showing A leading to B using mermaid syntax.
        """
        self.diagram = """
        graph LR
        A --> B
        """
        return self.diagram
