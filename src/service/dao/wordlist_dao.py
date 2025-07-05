import sqlite3
from typing import List
from model.sqlite.wordlist import Wordlist
from datetime import datetime

class WordlistDAO:
    """单词列表数据访问对象"""
    def __init__(self, db_path: str):
        self.db_path = db_path

    def _get_connection(self):
        return sqlite3.connect(self.db_path)

    def create(self, word: Wordlist) -> int:
        """添加单词"""
        now = datetime.now()
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """INSERT INTO wordlist 
                (wordbook_id, word, pronunciation, part, definition, status, mistake_count, create_time, modify_time)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (word.wordbook_id, word.word, word.pronunciation, 
                 word.part, word.definition, word.status, word.mistake_count, now, now)
            )
            conn.commit()
            return cursor.lastrowid

    def get_by_id(self, id: int) -> Wordlist:
        """根据ID获取单词"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM wordlist WHERE id = ?", (id,))
            row = cursor.fetchone()
            if row:
                word = Wordlist()
                word.id = row[0]
                word.wordbook_id = row[1]
                word.word = row[2]
                word.pronunciation = row[3]
                word.part = row[4]
                word.definition = row[5]
                word.status = row[6]
                word.modify_time = row[7]
                word.create_time = row[9]
                word.mistake_count = row[8]
                return word
            return None

    def get_by_wordbook(self, wordbook_id: int) -> List[Wordlist]:
        """获取词库下的所有单词"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM wordlist WHERE wordbook_id = ?", (wordbook_id,))
            words = []
            for row in cursor.fetchall():
                word = Wordlist()
                word.id = row[0]
                word.wordbook_id = row[1]
                word.word = row[2]
                word.pronunciation = row[3]
                word.part = row[4]
                word.definition = row[5]
                word.status = row[6]
                word.modify_time = row[7]
                word.create_time = row[9]
                word.mistake_count = row[8]
                words.append(word)
            return words

    def update(self, word: Wordlist) -> bool:
        """更新单词"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """UPDATE wordlist SET 
                word=?, pronunciation=?, part=?, definition=?, 
                status=?, mistake_count=?, modify_time=? WHERE id=?""",
                (word.word, word.pronunciation, word.part, 
                 word.definition, word.status, word.mistake_count, datetime.now(), word.id)
            )
            conn.commit()
            return cursor.rowcount > 0

    def delete(self, id: int) -> bool:
        """删除单词"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM wordlist WHERE id=?", (id,))
            conn.commit()
            return cursor.rowcount > 0