from datetime import datetime
from model.sqlite.base_model import BaseModel

class Wordlist(BaseModel):
    """单词列表模型"""
    def __init__(self):
        self.id = None
        self.wordbook_id = None
        self.word = None
        self.pronunciation = None
        self.part = None
        self.definition = None
        self.status = 0  # 0=未记住, 1=模糊, 2=已记住
        self.modify_time = datetime.now()
        self.create_time = datetime.now()
        self.mistake_count = 0

    @classmethod
    def create_table_sql(cls):
        return """
        CREATE TABLE IF NOT EXISTS wordlist (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            wordbook_id INTEGER NOT NULL,
            word VARCHAR(64) NOT NULL,
            pronunciation VARCHAR(64),
            part VARCHAR(16),
            definition VARCHAR(256),
            status INTEGER NOT NULL DEFAULT 0,
            modify_time DATETIME DEFAULT CURRENT_TIMESTAMP,
            create_time DATETIME DEFAULT CURRENT_TIMESTAMP,
            mistake_count INTEGER DEFAULT 0,
            UNIQUE(wordbook_id, word)
        )
        """