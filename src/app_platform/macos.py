import rumps
import logging
from model.constants import PROJECT_ROOT
from service.words_loader import get_random_word, get_last_word_obj, format_word_by_view
from service.dao.wordbook_dao import WordbookDAO
import pyperclip
from service.wordbook_service import get_wordbooks_grouped_by_language, select_wordbook
import os
import sys
from service.view_menu_service import get_view_config, update_view_config, get_word_view_display, VIEW_FIELDS

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename=PROJECT_ROOT / 'logs/stray_words.log',
    filemode='w'
)

wordbook_dao = WordbookDAO(str(PROJECT_ROOT / "resource" / "stray-words.db"))

# 在WordApp类前添加全局变量
definition_mode_once = False

def build_menu():
    items = []
    language_groups = get_wordbooks_grouped_by_language()
    # 创建两级菜单
    for lang, wbs in sorted(language_groups.items()):
        lang_menu = rumps.MenuItem(lang)
        for wb in sorted(wbs, key=lambda x: x.name):
            def callback(_, book=wb):
                select_wordbook(book.id)
                app.title = get_random_word()
            lang_menu.add(rumps.MenuItem(wb.name, callback=callback))
        items.append(lang_menu)
    return items

def truncate_for_menu(text, max_length=30):
    return text if len(text) <= max_length else text[:max_length-1] + "…"

class WordApp(rumps.App):
    def __init__(self):
        super(WordApp, self).__init__("Word", quit_button="Quit")
        self.showing_definition = False
        global definition_mode_once
        definition_mode_once = False
        try:
            self.wordlist_menu = build_menu()
        except Exception as e:
            logging.error(f"Failed to load wordbooks: {e}")
            self.menu = ["Failed to load wordbooks"]
            self.title = "Error"
            return
        if self.wordlist_menu:
            self.refresh_config_menu()
        else:
            self.menu = [
                rumps.MenuItem("Definition", callback=self.show_current_definition),
                rumps.MenuItem("Copy Word", callback=self.copy_word),
                rumps.separator,
                rumps.MenuItem("Select Wordlist (No wordbooks found)"),
                rumps.separator,
            ]
        self.title = get_random_word()

    @rumps.clicked("Next Word")
    def next_word(self, _):
        global definition_mode_once
        if definition_mode_once:
            definition_mode_once = False
        self.title = get_random_word()
        self.showing_definition = False

    def show_current_definition(self, _):
        from service.words_loader import get_current_definition, get_random_word, get_last_word_obj
        from service.config_loader import config as config_loader
        if getattr(self, 'showing_definition', False):
            # 恢复为当前last_word_obj对应的word显示
            word_obj = get_last_word_obj()
            if word_obj:
                view = config_loader.get('view', {})
                word_view = view.get('word_view', ['word'])
                self.title = format_word_by_view(word_view, word_obj)
            else:
                self.title = get_random_word()
            self.showing_definition = False
        else:
            # 保证last_word_obj有效
            definition = get_current_definition()
            if not definition or definition == "No words loaded":
                _ = get_random_word()
                definition = get_current_definition()
            self.title = truncate_for_menu(definition)
            self.showing_definition = True

    def copy_word(self, _):
        word_obj = get_last_word_obj()
        try:
            if word_obj and getattr(word_obj, 'word', None):
                pyperclip.copy(word_obj.word)
        except Exception as e:
            rumps.alert("Failed to copy: {}".format(e))

    def mark_status(self, status):
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
        self.title = get_random_word()
        self.showing_definition = False

    def skip_word(self, _):
        self.title = get_random_word()
        self.showing_definition = False

    def build_view_menu(self):
        def make_item(view_key, field):
            item = rumps.MenuItem(field)
            item.state = 1 if field in get_view_config().get(view_key, []) else 0
            def on_click(_):
                update_view_config(view_key, field)
                self.title = get_word_view_display()
                self.refresh_config_menu()
            item.set_callback(on_click)
            return item
        def make_view_submenu(view_key):
            submenu = rumps.MenuItem(view_key)
            for field in VIEW_FIELDS:
                submenu.add(make_item(view_key, field))
            return submenu
        view_menu = rumps.MenuItem('View')
        view_menu.add(make_view_submenu('word_view'))
        view_menu.add(make_view_submenu('definition_view'))
        return view_menu

    def refresh_config_menu(self):
        # 重新生成 Configuration 菜单并刷新 self.menu
        select_wordlist_menu = rumps.MenuItem("Select Wordlist")
        for item in self.wordlist_menu:
            select_wordlist_menu.add(item)
        configuration_menu = rumps.MenuItem("Configuration")
        configuration_menu.add(select_wordlist_menu)
        configuration_menu.add(self.build_view_menu())
        mark_menu = rumps.MenuItem("Mark")
        mark_menu.add(rumps.MenuItem("Yes", callback=lambda _: self.mark_status(2)))
        mark_menu.add(rumps.MenuItem("Blur", callback=lambda _: self.mark_status(1)))
        mark_menu.add(rumps.MenuItem("No", callback=lambda _: self.mark_status(0)))
        mark_menu.add(rumps.MenuItem("Skip", callback=self.skip_word))
        
        # 添加当前 wordlist 信息显示
        from service.config_loader import config as config_loader
        current_wordbook_id = config_loader.get('wordbook_id')
        if current_wordbook_id:
            current_wordbook = wordbook_dao.get_by_id(current_wordbook_id)
            if current_wordbook:
                wordlist_info = f"{current_wordbook.language} {current_wordbook.name}"
            else:
                wordlist_info = "Unknown wordlist"
        else:
            wordlist_info = "No wordlist selected"
        
        self.menu = [
            rumps.MenuItem(wordlist_info, callback=None),
            rumps.separator,
            rumps.MenuItem("Definition", callback=self.show_current_definition),
            rumps.MenuItem("Copy Word", callback=self.copy_word),
            mark_menu,
            rumps.separator,
            configuration_menu,
            rumps.separator,
        ]

def main(daemon_mode=False):
    if daemon_mode:
        pid = os.fork()
        if pid > 0:
            sys.exit(0)
        os.setsid()
        pid2 = os.fork()
        if pid2 > 0:
            sys.exit(0)
        sys.stdin.close()
        sys.stdout.close()
        sys.stderr.close()
    global app
    app = WordApp()
    app.run()
