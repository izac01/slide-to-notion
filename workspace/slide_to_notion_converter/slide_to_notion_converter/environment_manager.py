import os
import venv
import shutil

class EnvironmentManager:
    """
    This class is responsible for setting up and cleaning up the environment.
    """
    def __init__(self, env_path: str = './env'):
        """
        Initialize the EnvironmentManager with the path to the virtual environment.
        """
        self.env_path = env_path

    def setup_environment(self):
        """
        Set up the virtual environment.
        """
        if not os.path.exists(self.env_path):
            venv.create(self.env_path, with_pip=True)

        # Activate the virtual environment
        activate_file = os.path.join(self.env_path, 'bin', 'activate_this.py')
        with open(activate_file) as f:
            exec(f.read(), {'__file__': activate_file})

    def cleanup_environment(self):
        """
        Clean up the virtual environment.
        """
        # Remove the virtual environment directory
        shutil.rmtree(self.env_path)
