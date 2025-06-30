import random
from PIL import Image, ImageDraw, ImageFont
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

def create_icon_image(word, font_size=48):
    """Creates an icon image with the word written on it."""
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

    # Adjust font size to fit
    while font.getbbox(word)[2] > width and font_size > 10:
        font_size -= 2
        try:
            font = ImageFont.truetype(font.path, font_size)
        except (IOError, AttributeError): # Handle default font or other errors
            break

    text_bbox = draw.textbbox((0, 0), word, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    x = (width - text_width) / 2
    y = (height - text_height) / 2
    
    draw.text((x, y-5), word, font=font, fill='black')

    return image

def update_word(icon):
    """Updates the icon's title and image with a new random word."""
    new_word = get_random_word()
    icon.title = new_word
    icon.icon = create_icon_image(new_word)

def on_next_word(icon, item):
    """Callback for the 'Next Word' menu item."""
    update_word(icon)

def on_quit(icon, item):
    """Callback for the 'Quit' menu item."""
    icon.stop()

def main():
    """Main function to set up and run the tray icon."""
    load_words()
    
    initial_word = get_random_word()
    image = create_icon_image(initial_word)
    
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