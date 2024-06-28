import json
import os
import sys

def get_base_path():
    """Determine and return the base path for application data."""
    if getattr(sys, 'frozen', False):
        # If running in a PyInstaller bundle
        return os.path.dirname(sys.executable)
    else:
        # If running in a normal Python environment, navigate up from tools directory
        return os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

def get_base_path_audio():
    """Determine and return the base path for application data."""
    if getattr(sys, 'frozen', False):
        # If running in a PyInstaller bundle
        return sys._MEIPASS
    else:
        # If running in a normal Python environment, navigate up from tools directory
        return os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

def load_json_data(filename, default=None):
    """Load JSON data from a file or return the default if file is not found."""
    base_path = get_base_path()
    file_path = os.path.join(base_path, 'storage', filename)
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"File not found: {file_path}, returning default {default}.")
        return default if default is not None else {}
    except json.JSONDecodeError:
        print(f"Error decoding JSON from the file: {file_path}, returning default {default}.")
        return default if default is not None else {}

def save_json_data(filename, data):
    """Save JSON data to a file, ensuring compatibility with both Python and .exe environments."""
    base_path = get_base_path()
    file_path = os.path.join(base_path, 'storage', filename)
    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)  # Ensure the directory exists
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4)
