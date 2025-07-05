import random
import logging
from pathlib import Path
from service.config_loader import config as config_loader
from model.constants import PROJECT_ROOT
from service.dao.wordlist_dao import WordlistDAO

logger = logging.getLogger(__name__)
words = []
wordlist_dao = WordlistDAO(str(PROJECT_ROOT / "resource" / "stray-words.db"))
last_word_obj = None

def load_words():
    """从数据库加载单词"""
    global words
    wordbook_id = config_loader.get('wordbook_id')
    logger.debug(f"Config wordbook_id: {wordbook_id}")
    
    if wordbook_id:
        try:
            word_objects = wordlist_dao.get_by_wordbook(wordbook_id)
            def format_word(w):
                p = f" [{w.pronunciation}]" if w.pronunciation else ""
                part = f" {w.part}" if w.part else ""
                return f"{w.word}{p}{part}".strip()
            words = [format_word(word) for word in word_objects if word.word]
            logger.debug(f"Loaded {len(words)} words from wordbook {wordbook_id}")
            if not words:
                words = ["Wordbook is empty"]
                logger.warning("Wordbook is empty")
        except Exception as e:
            words = [f"Error loading words: {e}"]
            logger.error(f"Error loading words: {e}")
    else:
        words = ["Please select a wordbook"]
        logger.warning("No wordbook_id in config")

def format_word_by_view(view, word_obj):
    """根据view列表格式化单词对象"""
    parts = []
    for field in view:
        value = getattr(word_obj, field, None)
        if value:
            # 特殊处理pronunciation加[]
            if field == 'pronunciation':
                value = f"[{value}]"
            parts.append(str(value))
    return ' '.join(parts).strip()

def get_random_word():
    """返回随机单词"""
    global last_word_obj
    if not words:
        last_word_obj = None
        return "No words loaded"
    # 重新获取wordbook_id下的所有单词对象
    wordbook_id = config_loader.get('wordbook_id')
    if not wordbook_id:
        last_word_obj = None
        return "Please select a wordbook"
    word_objects = wordlist_dao.get_by_wordbook(wordbook_id)
    if not word_objects:
        last_word_obj = None
        return "Wordbook is empty"
    word = random.choice(word_objects)
    last_word_obj = word
    # 动态获取word_view
    view = config_loader.get('view', {})
    word_view = view.get('word_view', ['word'])
    return format_word_by_view(word_view, word)

def get_current_definition():
    """返回当前单词的 definition_view 格式"""
    if not last_word_obj:
        return "No words loaded"
    view = config_loader.get('view', {})
    definition_view = view.get('definition_view', ['definition'])
    return format_word_by_view(definition_view, last_word_obj)

def get_random_definition():
    """返回随机单词的part+definition格式"""
    if not words or isinstance(words[0], str):
        return "No words loaded"
    # 重新获取wordbook_id下的所有单词对象
    wordbook_id = config_loader.get('wordbook_id')
    if not wordbook_id:
        return "Please select a wordbook"
    word_objects = wordlist_dao.get_by_wordbook(wordbook_id)
    if not word_objects:
        return "Wordbook is empty"
    word = random.choice(word_objects)
    part = word.part or ""
    definition = word.definition or ""
    return f"{part} {definition}".strip()

def get_last_word_obj():
    global last_word_obj
    return last_word_obj