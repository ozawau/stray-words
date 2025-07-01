from dataclasses import dataclass
import yaml
from pathlib import Path

@dataclass
class Config:
    wordlist_path: str

    def __setitem__(self, key: str, value):
        setattr(self, key, value)

    def __getitem__(self, key: str):
        return getattr(self, key)

    @classmethod
    def from_yaml(cls, path: str | Path) -> "Config":
        with open(path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
        return cls(**data)