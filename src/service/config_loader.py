import yaml
import logging

# 从 constants.py 导入项目根目录
from model.constants import PROJECT_ROOT

logger = logging.getLogger(__name__)
CONFIG_FILE = PROJECT_ROOT / "config/config.yaml"

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
                    self.data = yaml.safe_load(f)
                    logger.debug(f"Loaded config: {self.data}")
                except yaml.YAMLError as e:
                    self.data = {}
                    logger.error(f"Error parsing config file: {e}")
    
    def get(self, key, default=None):
        return self.data.get(key, default)
        
    def __setitem__(self, key, value):
        self.data[key] = value
        
    def __getitem__(self, key):
        return self.data[key]

config = Config()

def load_config():
    """Public interface to load config"""
    config.load_config()

def save_config():
    """Saves configuration to config.yaml."""
    with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
        yaml.dump(config.data, f)
