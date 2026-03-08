# config.py
BOT_TOKEN = "8762092693:AAH8U53qPo0mmUoa_LMEg8pAcUk-gWZ5cHo"
ADMIN_PASSWORD = "1234"  # Поменяй на свой пароль!

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

# Хранилище авторизованных админов (временно, до перезапуска)
authorized_admins = set()
# Режим ожидания пароля
waiting_password = set()
# Режим редактирования ссылки
editing_link = {}  # user_id: link_key