import random
from pathlib import Path
from service.config_loader import config
from model.constants import PROJECT_ROOT, WORDLISTS_DIR

words = []

def load_words():
    """Loads words from the selected wordlist."""
    global words
    wordlist_path_str = config.get('wordlist_path')
    if wordlist_path_str:
        wordlist_path = PROJECT_ROOT / wordlist_path_str
        if wordlist_path.exists():
            try:
                with open(wordlist_path, 'r', encoding='utf-8') as f:
                    words = [line.strip() for line in f if line.strip()]
                if not words:
                    words = ["Wordlist is empty"]
            except Exception as e:
                words = [f"Error loading file: {e}"]
        else:
             words = ["List not found. Select one."]
    else:
        words = ["Please select a wordlist"]

def get_random_word():
    """Returns a random word."""
    return random.choice(words) if words else "No words loaded"