# -*- coding: utf-8 -*-

import json
import os

BOT_TOKEN = "5694724281:AAFB5wLVK-k0pegwCxIJlQexqi0KHuQabGY"
ADMIN_PASSWORD = "fakosfklpwlf"

DATA_FILE = "bot_data.json"

# Загрузка данных из файла
def load_data():
    global LINKS, LINKS_FOOTER
    
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            LINKS = data.get('links', DEFAULT_LINKS)
            LINKS_FOOTER = data.get('footer', DEFAULT_FOOTER)
    else:
        LINKS = DEFAULT_LINKS
        LINKS_FOOTER = DEFAULT_FOOTER

# Сохранение данных в файл
def save_data():
    data = {
        'links': LINKS,
        'footer': LINKS_FOOTER
    }
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# Дефолтные значения
DEFAULT_LINKS = {
    "slon2": {
        "url": "slon2.to",
        "note": "используйте VPN, новая линейка"
    },
    "slon3": {
        "url": "slon3.at", 
        "note": "используйте VPN"
    },
    "slon3cc": {
        "url": "slon3.cc",
        "note": "используйте VPN"
    }
}

DEFAULT_FOOTER = "В случае отключения slon3, slon4, и так далее"

# Загружаем при старте
LINKS = {}
LINKS_FOOTER = ""
load_data()

# Хранилище сессий
authorized_admins = set()
waiting_password = set()
editing_link = {}
editing_footer = set()