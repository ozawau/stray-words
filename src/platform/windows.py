from PIL import Image, ImageDraw, ImageFont
import pystray
from model.constants import PROJECT_ROOT, WORDLISTS_DIR
from service.words_loader import load_words, get_random_word
from service.config_loader import save_config

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