import random
import logging
from pathlib import Path
from service.config_loader import config as config_loader
from model.constants import PROJECT_ROOT, WORDLISTS_DIR

logger = logging.getLogger(__name__)
words = []

def load_words():
    """Loads words from the selected wordlist."""
    global words
    wordlist_path_str = config_loader.get('wordlist_path')
    logger.debug(f"Config wordlist_path: {wordlist_path_str}")
    if wordlist_path_str:
        wordlist_path = PROJECT_ROOT / wordlist_path_str
        logger.debug(f"Resolved wordlist path: {wordlist_path}")
        if wordlist_path.exists():
            try:
                with open(wordlist_path, 'r', encoding='utf-8') as f:
                    words = [line.strip() for line in f if line.strip()]
                logger.debug(f"Loaded {len(words)} words from {wordlist_path}")
                if not words:
                    words = ["Wordlist is empty"]
                    logger.warning("Wordlist file is empty")
            except Exception as e:
                words = [f"Error loading file: {e}"]
                logger.error(f"Error loading wordlist: {e}")
        else:
             words = ["List not found. Select one."]
             logger.error(f"Wordlist not found at {wordlist_path}")
    else:
        words = ["Please select a wordlist"]
        logger.warning("No wordlist_path in config")

def get_random_word():
    """Returns a random word."""
    return random.choice(words) if words else "No words loaded"