# bot.py
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from config import *

bot = telebot.TeleBot(BOT_TOKEN)

# ============ КЛАВИАТУРЫ ============

def main_menu():
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("🔐 Авторизация", callback_data="auth"))
    markup.add(InlineKeyboardButton("📝 Регистрация", callback_data="register"))
    markup.add(InlineKeyboardButton("🔗 Ссылки на площадку", callback_data="links"))
    return markup

def back_button():
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("❌ Закрыть", callback_data="back"))
    return markup

def admin_menu():
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("✏️ Изменить ссылки", callback_data="admin_edit_links"))
    markup.add(InlineKeyboardButton("📋 Показать текущие ссылки", callback_data="admin_show_links"))
    markup.add(InlineKeyboardButton("🚪 Выйти из админки", callback_data="admin_logout"))
    return markup

def links_edit_menu():
    markup = InlineKeyboardMarkup()
    for key, data in LINKS.items():
        markup.add(InlineKeyboardButton(f"✏️ {data['url']}", callback_data=f"edit_{key}"))
    markup.add(InlineKeyboardButton("➕ Добавить новую ссылку", callback_data="add_new_link"))
    markup.add(InlineKeyboardButton("🔙 Назад в админку", callback_data="admin_back"))
    return markup

# ============ ФУНКЦИИ ============

def get_links_text():
    text = "🔗 Ссылки на площадку\n\n<b>Clear:</b>\n"
    for key, data in LINKS.items():
        text += f"{data['url']} ({data['note']})\n"
    text += f"\n{LINKS_FOOTER}"
    return text

def get_admin_links_text():
    text = "<b>Текущие ссылки:</b>\n\n"
    for key, data in LINKS.items():
        text += f"🔹 <b>{key}</b>\n"
        text += f"   URL: {data['url']}\n"
        text += f"   Примечание: {data['note']}\n\n"
    return text

# ============ ОБРАБОТЧИКИ ============

# /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.from_user.id
    
    # Если в режиме админки
    if user_id in authorized_admins:
        bot.send_message(
            message.chat.id,
            "👋 Снова здравствуй, админ!",
            reply_markup=admin_menu(),
            parse_mode="HTML"
        )
        return
    
    bot.send_message(
        message.chat.id,
        "Войдите, или зарегистрируйтесь",
        reply_markup=main_menu(),
        parse_mode="HTML"
    )

# /admin
@bot.message_handler(commands=['admin'])
def admin_command(message):
    user_id = message.from_user.id
    
    # Уже авторизован
    if user_id in authorized_admins:
        bot.send_message(
            message.chat.id,
            "👑 <b>Админ-панель</b>",
            reply_markup=admin_menu(),
            parse_mode="HTML"
        )
        return
    
    # Запрашиваем пароль
    waiting_password.add(user_id)
    bot.send_message(
        message.chat.id,
        "🔒 Введите пароль администратора:",
        parse_mode="HTML"
    )

# Проверка пароля и редактирование ссылок
@bot.message_handler(func=lambda message: message.from_user.id in waiting_password or 
                                          message.from_user.id in editing_link)
def handle_admin_input(message):
    user_id = message.from_user.id
    text = message.text
    
    # Проверка пароля
    if user_id in waiting_password:
        waiting_password.discard(user_id)
        
        if text == ADMIN_PASSWORD:
            authorized_admins.add(user_id)
            bot.send_message(
                message.chat.id,
                "✅ Пароль верный!\n\n👑 <b>Админ-панель</b>",
                reply_markup=admin_menu(),
                parse_mode="HTML"
            )
        else:
            bot.send_message(
                message.chat.id,
                "❌ Неверный пароль!",
                reply_markup=main_menu(),
                parse_mode="HTML"
            )
        return
    
    # Редактирование ссылки
    if user_id in editing_link:
        link_key = editing_link[user_id]
        del editing_link[user_id]
        
        # Формат: url|примечание
        if "|" in text:
            parts = text.split("|", 1)
            url = parts[0].strip()
            note = parts[1].strip()
            
            LINKS[link_key] = {
                "url": url,
                "note": note
            }
            
            bot.send_message(
                message.chat.id,
                f"✅ Ссылка <b>{link_key}</b> обновлена!\n\n"
                f"URL: {url}\n"
                f"Примечание: {note}",
                reply_markup=links_edit_menu(),
                parse_mode="HTML"
            )
        else:
            bot.send_message(
                message.chat.id,
                "❌ Неверный формат!\n"
                "Используйте: <code>url|примечание</code>\n"
                "Пример: <code>slon5.new|новое зеркало</code>",
                reply_markup=links_edit_menu(),
                parse_mode="HTML"
            )
        return

# Callback обработчики
@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    user_id = call.from_user.id
    
    # Пользовательские кнопки
    if call.data == "auth":
        bot.edit_message_text(
            get_links_text(),
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=back_button(),
            parse_mode="HTML"
        )
    
    elif call.data == "register":
        bot.edit_message_text(
            get_links_text(),
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=back_button(),
            parse_mode="HTML"
        )
    
    elif call.data == "links":
        bot.edit_message_text(
            get_links_text(),
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=back_button(),
            parse_mode="HTML"
        )
    
    elif call.data == "back":
        bot.edit_message_text(
            "Войдите, или зарегистрируйтесь",
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=main_menu(),
            parse_mode="HTML"
        )
    
    # Админ кнопки
    elif call.data == "admin_edit_links":
        bot.edit_message_text(
            "✏️ Выберите ссылку для редактирования:\n\n"
            "Или нажмите 'Добавить новую'",
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=links_edit_menu(),
            parse_mode="HTML"
        )
    
    elif call.data == "admin_show_links":
        bot.edit_message_text(
            get_admin_links_text(),
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=admin_menu(),
            parse_mode="HTML"
        )
    
    elif call.data == "admin_logout":
        authorized_admins.discard(user_id)
        bot.edit_message_text(
            "👋 Вы вышли из админ-панели",
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=main_menu(),
            parse_mode="HTML"
        )
    
    elif call.data == "admin_back":
        bot.edit_message_text(
            "👑 <b>Админ-панель</b>",
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=admin_menu(),
            parse_mode="HTML"
        )
    
    elif call.data.startswith("edit_"):
        link_key = call.data.replace("edit_", "")
        
        if link_key in LINKS:
            current = LINKS[link_key]
            editing_link[user_id] = link_key
            
            bot.edit_message_text(
                f"✏️ Редактирование: <b>{link_key}</b>\n\n"
                f"Текущий URL: <code>{current['url']}</code>\n"
                f"Текущее примечание: <code>{current['note']}</code>\n\n"
                f"Введите новые данные в формате:\n"
                f"<code>url|примечание</code>\n\n"
                f"Пример: <code>slon5.new|новое зеркало, используйте VPN</code>",
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                parse_mode="HTML"
            )
    
    elif call.data == "add_new_link":
        # Генерируем ключ для новой ссылки
        new_key = f"link{len(LINKS) + 1}"
        editing_link[user_id] = new_key
        
        bot.edit_message_text(
            "➕ Добавление новой ссылки\n\n"
            "Введите данные в формате:\n"
            "<code>url|примечание</code>\n\n"
            "Пример: <code>slon5.new|новое зеркало</code>",
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            parse_mode="HTML"
        )

# Запуск
print("Бот запущен!")
print(f"Админ-панель: /admin")
print(f"Пароль: {ADMIN_PASSWORD}")
bot.polling(none_stop=True)