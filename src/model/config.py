from dataclasses import dataclass, field
import yaml
from pathlib import Path
from typing import Optional, Dict, List

@dataclass
class Config:
    wordbook_id: Optional[int] = None
    view: Dict[str, List[str]] = field(default_factory=dict)
    click_action: Optional[str] = None

    def __setitem__(self, key: str, value):
        setattr(self, key, value)

    def __getitem__(self, key: str):
        return getattr(self, key)

    @classmethod
    def from_yaml(cls, path: str | Path) -> "Config":
        with open(path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f) or {}
        if 'wordbook_id' not in data:
            data['wordbook_id'] = None
        if 'view' not in data:
            data['view'] = {}
        if 'click_action' not in data:
            data['click_action'] = None
        return cls(wordbook_id=data['wordbook_id'], view=data['view'], click_action=data['click_action'])