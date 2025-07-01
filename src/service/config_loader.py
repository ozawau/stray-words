import json
import logging
from pathlib import Path

# 从 constants.py 导入项目根目录
from model.constants import PROJECT_ROOT

logger = logging.getLogger(__name__)
CONFIG_FILE = PROJECT_ROOT / "config/config.json"

class Config:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.data = {}
            cls._instance.load_config()
        return cls._instance
    
    def load_config(self):
        logger.debug(f"Loading config from {CONFIG_FILE}")
        if CONFIG_FILE.exists():
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                try:
                    self.data = json.load(f)
                    logger.debug(f"Loaded config: {self.data}")
                except json.JSONDecodeError as e:
                    self.data = {}
                    logger.error(f"Error parsing config file: {e}")
        else:
            logger.warning(f"Config file not found, creating new at {CONFIG_FILE}")
            CONFIG_FILE.parent.mkdir(parents=True, exist_ok=True)
            with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
                json.dump({"wordlist_path": "wordlists/english/cet4.txt"}, f)
            self.data = {"wordlist_path": "wordlists/english/cet4.txt"}
            logger.info(f"Created new config with default wordlist_path")
    
    def get(self, key, default=None):
        return self.data.get(key, default)

config = Config()

def load_config():
    """Public interface to load config"""
    config.load_config()

def save_config():
    """Public interface to save config"""
    with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
        json.dump(config.data, f, indent=4)

def save_config():
    """Saves configuration to config.json."""
    with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=4)