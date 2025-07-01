import json
from pathlib import Path

# 从 constants.py 导入项目根目录
from model.constants import PROJECT_ROOT

CONFIG_FILE = PROJECT_ROOT / "config/config.json"
config = {}

def load_config():
    """Loads configuration from config.json."""
    global config
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            try:
                config = json.load(f)
            except json.JSONDecodeError:
                config = {}
    else:
        # If config doesn't exist, create it.
        CONFIG_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump({}, f)
        config = {}

def save_config():
    """Saves configuration to config.json."""
    with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=4)