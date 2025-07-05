#!/usr/bin/env python3
"""
将单词表JSON数据导入SQLite数据库的工具脚本
"""

import sqlite3
import json
from pathlib import Path
from datetime import datetime

# 配置参数
WORDBOOK_ID = 1  # 词库ID
JSON_PATH = Path(__file__).parent.parent.parent / "wordlists" / "english" / "cet4.json"
DB_PATH = Path(__file__).parent.parent.parent / "resource" / "stray-words.db"

def create_connection(db_file):
    """创建数据库连接"""
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except sqlite3.Error as e:
        print(f"数据库连接错误: {e}")
        return None

def import_words(conn, wordbook_id, words_data):
    """导入单词数据到数据库"""
    cursor = conn.cursor()
    
    # 准备插入SQL
    sql = """
    INSERT OR IGNORE INTO wordlist (
        wordbook_id, word, pronunciation, part, definition, 
        status, modify_time, mistake_count
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """
    
    inserted_count = 0
    for word, details in words_data.items():
        try:
            # 准备数据
            data = (
                wordbook_id,
                word,
                details.get("phonetic"),
                details.get("part"),
                details.get("desc"),
                0,  # 默认状态为未记住
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                0   # 错误计数初始为0
            )
            
            cursor.execute(sql, data)
            inserted_count += 1
        except sqlite3.Error as e:
            print(f"插入单词 '{word}' 失败: {e}")
    
    conn.commit()
    return inserted_count

def main():
    print("开始导入单词数据...")
    
    # 读取JSON文件
    try:
        with open(JSON_PATH, "r", encoding="utf-8") as f:
            words_data = json.load(f)
        print(f"成功读取 {len(words_data)} 个单词数据")
    except Exception as e:
        print(f"读取JSON文件失败: {e}")
        return
    
    # 连接数据库
    conn = create_connection(DB_PATH)
    if not conn:
        return
    
    # 导入数据
    try:
        count = import_words(conn, WORDBOOK_ID, words_data)
        print(f"成功导入 {count} 个单词到数据库")
    finally:
        conn.close()

if __name__ == "__main__":
    main()