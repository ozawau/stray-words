from datetime import datetime
from model.sqlite.base_model import BaseModel

class Wordbook(BaseModel):
    """词库模型"""
    def __init__(self):
        self.id = None
        self.name = None
        self.language = None
        self.type = 0  # 0=系统词库，1=用户自定义词库
        self.create_time = datetime.now()

    @classmethod
    def create_table_sql(cls):
        return """
        CREATE TABLE IF NOT EXISTS wordbook (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            language TEXT NOT NULL,
            type INTEGER NOT NULL DEFAULT 0,
            create_time DATETIME DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(name, language)
        )
        """