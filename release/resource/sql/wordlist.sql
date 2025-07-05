-- 单词表
CREATE TABLE IF NOT EXISTS wordlist (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    wordbook_id INTEGER NOT NULL,            -- 所属词库
    word VARCHAR(64) NOT NULL,               -- 单词文本
    pronunciation VARCHAR(64),               -- 音标或假名（不同语言）
    part VARCHAR(16),              -- 词性（n. v. 等）
    definition VARCHAR(256),                 -- 词义
    status INTEGER NOT NULL DEFAULT 0,       -- 0=未记住, 1=模糊, 2=已记住
    modify_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    create_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    mistake_count INTEGER DEFAULT 0,

    UNIQUE(wordbook_id, word)               -- 同一词库中单词唯一
);
