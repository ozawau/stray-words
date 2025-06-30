import random
from PIL import Image
import pystray

words = []

def load_words():
    """Loads words from wordlist.txt"""
    global words
    try:
        with open('wordlist.txt', 'r', encoding='utf-8') as f:
            words = [line.strip() for line in f if line.strip()]
        if not words:
            words = ['单词列表为空']
    except FileNotFoundError:
        words = ['未找到 wordlist.txt']

def get_random_word():
    """Returns a random word from the list."""
    return random.choice(words)

def create_icon_image():
    """Creates a simple 64x64 black image for the icon."""
    width = 64
    height = 64
    color = (0, 0, 0)  # Black
    image = Image.new('RGB', (width, height), color)
    return image

def update_word(icon):
    """Updates the icon's title with a new random word."""
    new_word = get_random_word()
    icon.title = new_word

def on_next_word(icon, item):
    """Callback for the 'Next Word' menu item."""
    update_word(icon)

def on_quit(icon, item):
    """Callback for the 'Quit' menu item."""
    icon.stop()

def main():
    """Main function to set up and run the tray icon."""
    load_words()
    
    image = create_icon_image()
    initial_word = get_random_word()
    
    menu = pystray.Menu(
        pystray.MenuItem('Next Word', on_next_word),
        pystray.Menu.SEPARATOR,
        pystray.MenuItem('Quit', on_quit)
    )

    icon = pystray.Icon("wordlist_app", image, initial_word, menu)
    
    # The update_word function needs to be called to set the initial title
    # on some platforms after the icon is created.
    # The title is set in the constructor, so this is just for initial setup.
    
    icon.run()

if __name__ == "__main__":
    main() 