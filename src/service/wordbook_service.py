from typing import Dict, List
from service.dao.wordbook_dao import WordbookDAO
from service.config_loader import save_config, config
from service.words_loader import load_words
from model.constants import PROJECT_ROOT
from model.sqlite.wordbook import Wordbook

wordbook_dao = WordbookDAO(str(PROJECT_ROOT / "resource" / "stray-words.db"))

def get_wordbooks_grouped_by_language() -> Dict[str, List[Wordbook]]:
    """
    获取所有词书，并按 language 分组。
    返回: {language: [Wordbook, ...], ...}
    """
    wordbooks = wordbook_dao.get_all()
    language_groups = {}
    for wb in wordbooks:
        language_groups.setdefault(wb.language, []).append(wb)
    return language_groups

def select_wordbook(wordbook_id: int):
    """
    切换词书，保存配置并重新加载单词。
    """
    config['wordbook_id'] = wordbook_id
    save_config()
    load_words() 