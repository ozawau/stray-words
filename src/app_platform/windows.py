from PIL import Image, ImageDraw, ImageFont
import pystray
from model.constants import PROJECT_ROOT
from service.words_loader import get_random_word, get_current_definition, get_last_word_obj
from service.dao.wordbook_dao import WordbookDAO
import pyperclip
from service.wordbook_service import get_wordbooks_grouped_by_language, select_wordbook
import sys
import subprocess
from service.view_menu_service import get_view_config, update_view_config, get_word_view_display, VIEW_FIELDS

wordbook_dao = WordbookDAO(str(PROJECT_ROOT / "resource" / "stray-words.db"))

# 在main函数前添加全局变量
show_definition_once = False
show_definition = False

def create_icon_image(font_size=48):
    # 始终使用 'ABC' 作为图标内容
    display_text = 'ABC'
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
    
    while hasattr(font, 'getbbox') and font.getbbox(display_text)[2] > width and font_size > 10:
        font_size -= 2
        try:
            font = ImageFont.truetype(font.path, font_size)
        except (IOError, AttributeError):
            font = ImageFont.load_default()
            break
    
    if hasattr(draw, 'textbbox'):
        text_bbox = draw.textbbox((0, 0), display_text, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]
    else:
        text_width, text_height = draw.textsize(display_text, font=font)

    x = (width - text_width) / 2
    y = (height - text_height) / 2 - 5
    draw.text((x, y), display_text, font=font, fill='black')
    return image

def update_word(icon, force_next=False):
    global show_definition_once, show_definition
    if force_next:
        new_word = get_random_word()
        show_definition = False
        show_definition_once = False
    elif show_definition or show_definition_once:
        new_word = get_current_definition()
        show_definition_once = False
    else:
        new_word = get_random_word()
        show_definition = False
    icon.title = new_word
    icon.icon = create_icon_image()

def on_show_definition(icon, item):
    global show_definition
    from service.words_loader import get_last_word_obj, format_word_by_view
    from service.config_loader import config as config_loader
    if show_definition:
        # 恢复为当前last_word_obj对应的word显示
        word_obj = get_last_word_obj()
        if word_obj:
            view = config_loader.get('view', {})
            word_view = view.get('word_view', ['word'])
            icon.title = format_word_by_view(word_view, word_obj)
        else:
            icon.title = get_random_word()
        show_definition = False
    else:
        show_definition = True
        update_word(icon)

def on_quit(icon, item):
    icon.stop()

def on_copy_word(icon, item):
    word_obj = get_last_word_obj()
    print("CopyWord clicked", word_obj.word if word_obj else None)
    if word_obj and getattr(word_obj, 'word', None):
        pyperclip.copy(word_obj.word)

def on_next_word(icon, item):
    global show_definition
    show_definition = False
    update_word(icon)

def on_mark_status(icon, status):
    from service.words_loader import get_last_word_obj
    from service.dao.wordlist_dao import WordlistDAO
    from model.constants import PROJECT_ROOT
    word_obj = get_last_word_obj()
    if word_obj and hasattr(word_obj, 'status'):
        word_obj.status = status
        if status in (0, 1):  # No 或 Blur
            word_obj.mistake_count = (word_obj.mistake_count or 0) + 1
        wordlist_dao = WordlistDAO(str(PROJECT_ROOT / "resource" / "stray-words.db"))
        wordlist_dao.update(word_obj)
    update_word(icon, force_next=True)

def on_skip(icon, item):
    print("Debug: on_skip function called")  # 调试输出
    update_word(icon, force_next=True)

def get_view_menu(icon):
    def make_item(view_key, field):
        def toggle(icon, item):
            update_view_config(view_key, field)
            icon.title = get_word_view_display()
            icon.update_menu()
        def checked(_):
            view = get_view_config()
            return field in view.get(view_key, [])
        return pystray.MenuItem(field, toggle, checked=checked)
    def make_view_submenu(view_key):
        return pystray.MenuItem(
            view_key,
            pystray.Menu(*(make_item(view_key, field) for field in VIEW_FIELDS))
        )
    return pystray.MenuItem(
        'View',
        pystray.Menu(
            make_view_submenu('word_view'),
            make_view_submenu('definition_view'),
        )
    )

def main(daemon_mode=False):
    if daemon_mode:
        if not hasattr(sys, 'frozen'):
            python = sys.executable
        else:
            python = sys.argv[0]
        args = [python] + [a for a in sys.argv if a not in ("--daemon", "-d")]
        DETACHED_PROCESS = 0x00000008
        subprocess.Popen(args, creationflags=DETACHED_PROCESS, close_fds=True)
        sys.exit(0)
    global show_definition_once, show_definition
    show_definition_once = False
    show_definition = False
    initial_word = get_random_word()
    icon = pystray.Icon("wordlist_app")
    icon.icon = create_icon_image()
    icon.title = initial_word

    # 构建顶层分发器
    def tray_click_dispatcher():
        from service.config_loader import config as config_loader  # 确保每次都重新获取
        action = config_loader.get('click_action', 'definition')
        print(f"Debug: tray_click_dispatcher called, action={action}")
        if action == 'definition':
            on_show_definition(icon, None)
        elif action == 'copy':
            on_copy_word(icon, None)
        elif action == 'yes':
            on_mark_status(icon, 2)
        elif action == 'blur':
            on_mark_status(icon, 1)
        elif action == 'no':
            on_mark_status(icon, 0)
        elif action == 'skip':
            on_skip(icon, None)
        else:
            on_show_definition(icon, None)
    
    def refresh_menu():
        from service.config_loader import config as config_loader
        click_action = config_loader.get('click_action', 'definition')
        menu_items = []
        # 添加当前 wordlist 信息显示
        current_wordbook_id = config_loader.get('wordbook_id')
        if current_wordbook_id:
            current_wordbook = wordbook_dao.get_by_id(current_wordbook_id)
            if current_wordbook:
                wordlist_info = f"{current_wordbook.language} {current_wordbook.name}"
            else:
                wordlist_info = "Unknown wordlist"
        else:
            wordlist_info = "No wordlist selected"
        menu_items.append(pystray.MenuItem(wordlist_info, None, enabled=False))
        menu_items.append(pystray.Menu.SEPARATOR)
        # 动态添加 default 菜单项
        if click_action == 'definition':
            menu_items.append(pystray.MenuItem('Definition', lambda: on_show_definition(icon, None), default=True))
        elif click_action == 'copy':
            menu_items.append(pystray.MenuItem('Copy Word', on_copy_word, default=True))
            menu_items.append(pystray.MenuItem('Definition', lambda: on_show_definition(icon, None)))
        elif click_action == 'yes':
            menu_items.append(pystray.MenuItem('Mark as Yes', lambda: on_mark_status(icon, 2), default=True))
            menu_items.append(pystray.MenuItem('Definition', lambda: on_show_definition(icon, None)))
        elif click_action == 'no':
            menu_items.append(pystray.MenuItem('Mark as No', lambda: on_mark_status(icon, 0), default=True))
            menu_items.append(pystray.MenuItem('Definition', lambda: on_show_definition(icon, None)))
        elif click_action == 'blur':
            menu_items.append(pystray.MenuItem('Mark as Blur', lambda: on_mark_status(icon, 1), default=True))
            menu_items.append(pystray.MenuItem('Definition', lambda: on_show_definition(icon, None)))
        elif click_action == 'skip':
            menu_items.append(pystray.MenuItem('Skip', on_skip, default=True))
            menu_items.append(pystray.MenuItem('Definition', lambda: on_show_definition(icon, None)))
        else:
            menu_items.append(pystray.MenuItem('Definition', lambda: on_show_definition(icon, None), default=True))
        if click_action != 'copy':
            menu_items.append(pystray.MenuItem('Copy Word', on_copy_word))
        mark_menu_items = [
            pystray.MenuItem('Yes', lambda icon, item: on_mark_status(icon, 2)),
            pystray.MenuItem('Blur', lambda icon, item: on_mark_status(icon, 1)),
            pystray.MenuItem('No', lambda icon, item: on_mark_status(icon, 0)),
            pystray.MenuItem('Skip', on_skip),
        ]
        menu_items.append(pystray.MenuItem('Mark', pystray.Menu(*mark_menu_items)))
        menu_items.extend([
            pystray.Menu.SEPARATOR,
            configuration_menu,
            pystray.Menu.SEPARATOR,
            pystray.MenuItem('Quit', on_quit)
        ])
        icon.menu = pystray.Menu(*menu_items)

    def create_wordlist_selection_handler(icon, wordbook_id):
        def handler(item):
            global show_definition, show_definition_once
            select_wordbook(wordbook_id)
            show_definition = False
            show_definition_once = False
            update_word(icon)
            refresh_menu()  # 切换后刷新菜单
        return handler

    def build_menu_items(icon):
        items = []
        language_groups = get_wordbooks_grouped_by_language()
        # 创建两级菜单
        for lang, wbs in sorted(language_groups.items()):
            lang_menu_items = []
            for wb in sorted(wbs, key=lambda x: x.name):
                handler = create_wordlist_selection_handler(icon, wb.id)
                lang_menu_items.append(pystray.MenuItem(wb.name, handler))
            if lang_menu_items:
                items.append(pystray.MenuItem(lang, pystray.Menu(*lang_menu_items)))
        return items

    try:
        wordlist_menu_items = build_menu_items(icon)
    except Exception as e:
        menu = pystray.Menu(
            pystray.MenuItem("Failed to load wordbooks", None),
            pystray.MenuItem('Quit', on_quit)
        )
        icon.menu = menu
        icon.run()
        return

    configuration_menu = pystray.MenuItem(
        'Configuration',
        pystray.Menu(
            pystray.MenuItem('Select Wordlist', pystray.Menu(*wordlist_menu_items)),
            get_view_menu(icon),
        )
    )

    # 首次启动时也用 refresh_menu
    refresh_menu()
    icon.run()