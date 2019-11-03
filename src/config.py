import os
import sys
from pathlib import Path

LOCAL_STORAGE_PATH = os.path.expanduser(f"~/.gcal-toggl")
CREDENTIALS_PATH = "data/credentials.json"
GOOGLE_SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

if not os.path.exists(LOCAL_STORAGE_PATH):
    os.makedirs(LOCAL_STORAGE_PATH, exist_ok=True)


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)