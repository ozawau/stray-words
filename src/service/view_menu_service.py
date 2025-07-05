from service.config_loader import config as config_loader, save_config
from service.words_loader import get_last_word_obj, format_word_by_view

VIEW_FIELDS = ['word', 'pronunciation', 'part', 'definition']

# 通用配置操作

def get_view_config():
    return config_loader.get('view', {})

def update_view_config(view_key, field):
    view = config_loader.get('view', {})
    fields = set(view.get(view_key, []))
    if field in fields:
        fields.remove(field)
    else:
        fields.add(field)
    # 保证顺序
    order = VIEW_FIELDS
    view[view_key] = [f for f in order if f in fields]
    config_loader._config.view = view
    save_config()
    config_loader.load_config()
    return view

def get_word_view_display():
    word_obj = get_last_word_obj()
    view = config_loader.get('view', {})
    word_view = view.get('word_view', ['word'])
    if word_obj:
        return format_word_by_view(word_view, word_obj)
    else:
        from service.words_loader import get_random_word
        return get_random_word() 