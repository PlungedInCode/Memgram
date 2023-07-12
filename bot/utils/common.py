import gettext
import os
import shutil
import sys
from pathlib import Path

from appdirs import user_config_dir

APP_NAME = 'memgram'
BOT_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BOT_PATH, 'data')

CONFIG_DIR = user_config_dir(APP_NAME)
DB_DIR = os.path.join(os.path.dirname(BOT_PATH), 'config/database')

DB_PATH = os.path.join(DB_DIR, 'memgram.db')
ADMINS_PATH = os.path.join(os.path.dirname(BOT_PATH), 'config/admins.json')


INVALID_MIME_TYPES = [
    'video/quicktime'
]
