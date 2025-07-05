CREATE TABLE IF NOT EXISTS wordbook (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,               -- 词库名称（唯一）
    language TEXT NOT NULL,                  -- 语言（如 en, ja, zh 等）
    type INTEGER NOT NULL DEFAULT 0,          -- 词库类型：0=系统词库，1=用户自定义词库
    `create_time` DATETIME DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(name, language)
);
