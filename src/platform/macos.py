import rumps
import logging
from model.constants import PROJECT_ROOT, WORDLISTS_DIR
from service.words_loader import load_words, get_random_word
from service.config_loader import save_config

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename=PROJECT_ROOT / 'logs/stray_words.log',
    filemode='w'
)

def build_menu(path):
    items = []
    for item in sorted(path.iterdir()):
        if item.is_dir():
            submenu = build_menu(item)
            if submenu:
                # 创建一个新的菜单对象
                menu = rumps.MenuItem(item.name)
                # 为这个菜单添加子项
                for sub_item in submenu:
                    menu.add(sub_item)
                items.append(menu)
        elif item.suffix == '.txt':
            def callback(_, p=item):
                config['wordlist_path'] = str(p.relative_to(PROJECT_ROOT))
                save_config()
                load_words()
                app.title = get_random_word()
            items.append(rumps.MenuItem(item.stem, callback=callback))
    return items

class WordApp(rumps.App):
    def __init__(self):
        super(WordApp, self).__init__("Word", quit_button="Quit")
        if not WORDLISTS_DIR.is_dir():
            self.menu = ["'wordlists' dir not found"]
            self.title = "Error"
            return

        self.wordlist_menu = build_menu(WORDLISTS_DIR)
        if self.wordlist_menu:
            # 创建一个选择词表的菜单
            select_wordlist_menu = rumps.MenuItem("Select Wordlist")
            # 添加所有词表子菜单
            for item in self.wordlist_menu:
                select_wordlist_menu.add(item)
            
            self.menu = [
                rumps.MenuItem("Next Word"),
                rumps.separator,
                select_wordlist_menu,
                rumps.separator,
            ]
        else:
            self.menu = [
                rumps.MenuItem("Next Word"),
                rumps.separator,
                rumps.MenuItem("Select Wordlist (No .txt found)"),
                rumps.separator,
            ]
        self.title = get_random_word()

    @rumps.clicked("Next Word")
    def next_word(self, _):
        self.title = get_random_word()

def main():
    global app
    app = WordApp()
    app.run()