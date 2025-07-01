import json
import os
import random
import sys
from pathlib import Path

# Determine project root based on the script's location
try:
    # This works when running as a script
    SCRIPT_DIR = Path(__file__).resolve().parent
except NameError:
    # Fallback for interactive environments or when __file__ is not defined
    SCRIPT_DIR = Path.cwd()

PROJECT_ROOT = SCRIPT_DIR.parent
CONFIG_FILE = PROJECT_ROOT / "config/config.json"
WORDLISTS_DIR = PROJECT_ROOT / "wordlists"

config = {}
words = []

def load_config():
    """Loads configuration from config.json."""
    global config
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            try:
                config = json.load(f)
            except json.JSONDecodeError:
                config = {}
    else:
        # If config doesn't exist, create it.
        CONFIG_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump({}, f)
        config = {}

def save_config():
    """Saves configuration to config.json."""
    with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=4)

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

if sys.platform == 'darwin':
    import rumps

    def build_menu(path):
        """Builds a recursive menu for rumps."""
        items = []
        for item in sorted(path.iterdir()):
            if item.is_dir():
                submenu_items = build_menu(item)
                if submenu_items:
                    items.append(rumps.MenuItem(item.name, *submenu_items))
            elif item.suffix == '.txt':
                def create_callback(p):
                    def callback(_):
                        config['wordlist_path'] = str(p.relative_to(PROJECT_ROOT))
                        save_config()
                        load_words()
                        app.title = get_random_word()
                    return callback
                items.append(rumps.MenuItem(item.stem, callback=create_callback(item)))
        return items

    class WordApp(rumps.App):
        def __init__(self):
            super(WordApp, self).__init__("Word", quit_button="Quit")
            if not WORDLISTS_DIR.is_dir():
                self.menu = ["'wordlists' dir not found"]
                self.title = "Error"
                return

            self.wordlist_menu = build_menu(WORDLISTS_DIR)
            self.menu = [
                rumps.MenuItem("Next Word"),
                None,
                rumps.MenuItem("Select Wordlist", *self.wordlist_menu),
                None,
            ]
            self.title = get_random_word()

        @rumps.clicked("Next Word")
        def next_word(self, _):
            self.title = get_random_word()

    def main():
        global app
        load_config()
        load_words()
        app = WordApp()
        app.run()

else:  # For other platforms
    from PIL import Image, ImageDraw, ImageFont
    import pystray

    def create_icon_image(word, font_size=48):
        width, height = 64, 64
        image = Image.new('RGB', (width, height), 'white')
        draw = ImageDraw.Draw(image)
        try:
            font = ImageFont.truetype("msyh.ttc", font_size)
        except IOError:
            try:
                font = ImageFont.truetype("arial.ttf", font_size)
            except IOError:
                font = ImageFont.load_default()
        
        while hasattr(font, 'getbbox') and font.getbbox(word)[2] > width and font_size > 10:
            font_size -= 2
            try:
                font = ImageFont.truetype(font.path, font_size)
            except (IOError, AttributeError):
                font = ImageFont.load_default()
                break
        
        if hasattr(draw, 'textbbox'):
            text_bbox = draw.textbbox((0, 0), word, font=font)
            text_width = text_bbox[2] - text_bbox[0]
            text_height = text_bbox[3] - text_bbox[1]
        else:
            text_width, text_height = draw.textsize(word, font=font)

        x = (width - text_width) / 2
        y = (height - text_height) / 2 - 5
        draw.text((x, y), word, font=font, fill='black')
        return image

    def update_word(icon):
        new_word = get_random_word()
        icon.title = new_word
        icon.icon = create_icon_image(new_word)

    def on_quit(icon, item):
        icon.stop()
        
    def create_wordlist_selection_handler(icon, path):
        def handler(item):
            config['wordlist_path'] = str(path.relative_to(PROJECT_ROOT))
            save_config()
            load_words()
            update_word(icon)
        return handler

    def build_menu_items(path, icon):
        items = []
        for item in sorted(path.iterdir()):
            if item.is_dir():
                sub_menu = pystray.Menu(*build_menu_items(item, icon))
                if sub_menu.items:
                    items.append(pystray.MenuItem(item.name, sub_menu))
            elif item.suffix == '.txt':
                handler = create_wordlist_selection_handler(icon, item)
                menu_item = pystray.MenuItem(item.stem, handler)
                items.append(menu_item)
        return items

    def main():
        load_config()
        load_words()
        
        initial_word = get_random_word()
        
        icon = pystray.Icon("wordlist_app")
        icon.icon = create_icon_image(initial_word)
        icon.title = initial_word

        if not WORDLISTS_DIR.is_dir():
             menu = pystray.Menu(pystray.MenuItem("'wordlists' dir not found", None), pystray.MenuItem('Quit', on_quit))
        else:
            wordlist_menu_items = build_menu_items(WORDLISTS_DIR, icon)
            menu = pystray.Menu(
                pystray.MenuItem('Next Word', lambda: update_word(icon)),
                pystray.Menu.SEPARATOR,
                pystray.MenuItem('Select Wordlist', pystray.Menu(*wordlist_menu_items)),
                pystray.Menu.SEPARATOR,
                pystray.MenuItem('Quit', on_quit)
            )
        
        icon.menu = menu
        icon.run()

if __name__ == "__main__":
    main() 