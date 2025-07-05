#!/usr/bin/env python3
"""
将日语 N5 单词表（n5.txt）导入 SQLite 数据库的工具脚本
"""

import sqlite3
from pathlib import Path
from datetime import datetime

# 配置参数
WORDBOOK_NAME = "n5"
WORDBOOK_LANGUAGE = "japanese"
WORDBOOK_TYPE = 0
N5_TXT_PATH = Path(__file__).parent.parent.parent / "wordlists" / "japanese" / "n5.txt"
DB_PATH = Path(__file__).parent.parent.parent / "resource" / "stray-words.db"

def create_connection(db_file):
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except sqlite3.Error as e:
        print(f"数据库连接错误: {e}")
        return None

def get_or_create_wordbook(conn, name, language, type_):
    cursor = conn.cursor()
    # 检查是否已存在
    cursor.execute(
        "SELECT id FROM wordbook WHERE name=? AND language=?",
        (name, language)
    )
    row = cursor.fetchone()
    if row:
        return row[0]
    # 不存在则插入
    cursor.execute(
        "INSERT INTO wordbook (name, language, type) VALUES (?, ?, ?)",
        (name, language, type_)
    )
    conn.commit()
    return cursor.lastrowid

def import_n5_words(conn, wordbook_id, n5_txt_path):
    cursor = conn.cursor()
    sql = """
    INSERT OR IGNORE INTO wordlist (
        wordbook_id, word, pronunciation, part, definition, 
        status, modify_time, mistake_count
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """
    inserted_count = 0
    with open(n5_txt_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            parts = line.split("\t")
            if len(parts) < 4:
                print(f"跳过格式错误行: {line}")
                continue
            word, pronunciation, part, definition = parts[:4]
            data = (
                wordbook_id,
                word,
                pronunciation,
                part,
                definition,
                0,  # 默认状态为未记住
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                0   # 错误计数初始为0
            )
            try:
                cursor.execute(sql, data)
                inserted_count += 1
            except sqlite3.Error as e:
                print(f"插入单词 '{word}' 失败: {e}")
    conn.commit()
    return inserted_count

def main():
    print("开始导入日语 N5 单词表...")
    conn = create_connection(DB_PATH)
    if not conn:
        return
    try:
        wordbook_id = get_or_create_wordbook(conn, WORDBOOK_NAME, WORDBOOK_LANGUAGE, WORDBOOK_TYPE)
        print(f"n5 词库 ID: {wordbook_id}")
        count = import_n5_words(conn, wordbook_id, N5_TXT_PATH)
        print(f"成功导入 {count} 个单词到数据库")
    finally:
        conn.close()

if __name__ == "__main__":
    main() 