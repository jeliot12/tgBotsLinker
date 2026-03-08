# -*- coding: utf-8 -*-

BOT_TOKEN = "5694724281:AAFB5wLVK-k0pegwCxIJlQexqi0KHuQabGY"
ADMIN_PASSWORD = "1234"


# Ссылки на площадки
LINKS = {
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

LINKS_FOOTER = "В случае отключения slon3, slon4, и так далее"

# Хранилище
authorized_admins = set()
waiting_password = set()
editing_link = {}
editing_footer = set()  # Новое: кто редактирует футер