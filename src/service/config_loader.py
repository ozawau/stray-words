import yaml
import logging
from pathlib import Path
from typing import Dict, Any

# 从 constants.py 导入项目根目录
from model.constants import PROJECT_ROOT
from model.config import Config

logger = logging.getLogger(__name__)
# 使用PROJECT_ROOT常量，它会根据是否是打包环境自动调整路径
CONFIG_FILE = PROJECT_ROOT / "config/config.yaml"

class ConfigLoader:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._config = None
            cls._instance.load_config()
        return cls._instance
    
    def load_config(self) -> Config:
        logger.debug(f"Loading config from {CONFIG_FILE}")
        if CONFIG_FILE.exists():
            try:
                self._config = Config.from_yaml(CONFIG_FILE)
                logger.debug(f"Loaded config: {self._config}")
            except yaml.YAMLError as e:
                logger.error(f"Error parsing config file: {e}")
                self._config = Config(wordbook_id=None)
        return self._config
    
    def get(self, key: str, default: Any = None) -> Any:
        return getattr(self._config, key, default)
        
    def __getattr__(self, name: str) -> Any:
        return getattr(self._config, name)
        
    def __setitem__(self, key: str, value: Any):
        setattr(self._config, key, value)

config = ConfigLoader()

def load_config() -> Config:
    """Public interface to load config"""
    return config.load_config()

def save_config():
    """Saves configuration to config.yaml."""
    with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
        yaml.dump(config._config.__dict__, f)
