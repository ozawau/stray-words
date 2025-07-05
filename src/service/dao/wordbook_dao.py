import sqlite3
from typing import List
from model.sqlite.wordbook import Wordbook
from datetime import datetime

class WordbookDAO:
    """词库数据访问对象"""
    def __init__(self, db_path: str):
        self.db_path = db_path

    def _get_connection(self):
        return sqlite3.connect(self.db_path)

    def create(self, wordbook: Wordbook) -> int:
        """创建词库"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO wordbook (name, language, type, create_time) VALUES (?, ?, ?, ?)",
                (wordbook.name, wordbook.language, wordbook.type, datetime.now())
            )
            conn.commit()
            return cursor.lastrowid

    def get_by_id(self, id: int) -> Wordbook:
        """根据ID获取词库"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM wordbook WHERE id = ?", (id,))
            row = cursor.fetchone()
            if row:
                wordbook = Wordbook()
                wordbook.id = row[0]
                wordbook.name = row[1]
                wordbook.language = row[2]
                wordbook.type = row[3]
                wordbook.create_time = row[4]
                return wordbook
            return None

    def get_all(self) -> List[Wordbook]:
        """获取所有词库"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM wordbook")
            wordbooks = []
            for row in cursor.fetchall():
                wordbook = Wordbook()
                wordbook.id = row[0]
                wordbook.name = row[1]
                wordbook.language = row[2]
                wordbook.type = row[3]
                wordbook.create_time = row[4]
                wordbooks.append(wordbook)
            return wordbooks

    def update(self, wordbook: Wordbook) -> bool:
        """更新词库"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE wordbook SET name=?, language=?, type=? WHERE id=?",
                (wordbook.name, wordbook.language, wordbook.type, wordbook.id)
            )
            conn.commit()
            return cursor.rowcount > 0

    def delete(self, id: int) -> bool:
        """删除词库"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM wordbook WHERE id=?", (id,))
            conn.commit()
            return cursor.rowcount > 0