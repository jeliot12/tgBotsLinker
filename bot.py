# -*- coding: utf-8 -*-

import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import *

bot = telebot.TeleBot(BOT_TOKEN)

def main_menu():
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("Авторизация", callback_data="auth"))
    markup.add(InlineKeyboardButton("Регистрация", callback_data="register"))
    markup.add(InlineKeyboardButton("Ссылки на площадку", callback_data="links"))
    return markup

def back_button():
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("Закрыть", callback_data="back"))
    return markup

def admin_menu():
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("Изменить ссылки", callback_data="admin_edit_links"))
    markup.add(InlineKeyboardButton("Изменить подпись (footer)", callback_data="admin_edit_footer"))
    markup.add(InlineKeyboardButton("Показать текущие ссылки", callback_data="admin_show_links"))
    markup.add(InlineKeyboardButton("Выйти из админки", callback_data="admin_logout"))
    return markup

def links_edit_menu():
    markup = InlineKeyboardMarkup()
    for key, data in LINKS.items():
        markup.add(InlineKeyboardButton("Edit: " + data['url'], callback_data="edit_" + key))
    markup.add(InlineKeyboardButton("Добавить новую ссылку", callback_data="add_new_link"))
    markup.add(InlineKeyboardButton("Назад в админку", callback_data="admin_back"))
    return markup

def get_links_text():
    text = "Ссылки на площадку\n\nClear:\n"
    for key, data in LINKS.items():
        text += data['url'] + " (" + data['note'] + ")\n"
    text += "\n" + LINKS_FOOTER
    return text

def get_admin_links_text():
    text = "Текущие ссылки:\n\n"
    for key, data in LINKS.items():
        text += key + "\n"
        text += "   URL: " + data['url'] + "\n"
        text += "   Примечание: " + data['note'] + "\n\n"
    text += "Подпись (footer):\n" + LINKS_FOOTER
    return text

@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.from_user.id
    
    if user_id in authorized_admins:
        bot.send_message(
            message.chat.id,
            "Снова здравствуй, админ!",
            reply_markup=admin_menu()
        )
        return
    
    bot.send_message(
        message.chat.id,
        "Войдите, или зарегистрируйтесь",
        reply_markup=main_menu()
    )

@bot.message_handler(commands=['admin'])
def admin_command(message):
    user_id = message.from_user.id
    
    if user_id in authorized_admins:
        bot.send_message(
            message.chat.id,
            "Админ-панель",
            reply_markup=admin_menu()
        )
        return
    
    waiting_password.add(user_id)
    bot.send_message(
        message.chat.id,
        "Введите пароль администратора:"
    )

@bot.message_handler(func=lambda message: message.from_user.id in waiting_password or 
                                          message.from_user.id in editing_link or
                                          message.from_user.id in editing_footer)
def handle_admin_input(message):
    user_id = message.from_user.id
    text = message.text
    global LINKS_FOOTER
    
    # Проверка пароля
    if user_id in waiting_password:
        waiting_password.discard(user_id)
        
        if text == ADMIN_PASSWORD:
            authorized_admins.add(user_id)
            bot.send_message(
                message.chat.id,
                "Пароль верный!\n\nАдмин-панель",
                reply_markup=admin_menu()
            )
        else:
            bot.send_message(
                message.chat.id,
                "Неверный пароль!",
                reply_markup=main_menu()
            )
        return
    
    # Редактирование футера
    if user_id in editing_footer:
        editing_footer.discard(user_id)
        LINKS_FOOTER = text
        
        bot.send_message(
            message.chat.id,
            "Подпись обновлена!\n\nНовая подпись:\n" + LINKS_FOOTER,
            reply_markup=admin_menu()
        )
        return
    
    # Редактирование ссылки
    if user_id in editing_link:
        link_key = editing_link[user_id]
        del editing_link[user_id]
        
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
                "Ссылка " + link_key + " обновлена!\n\nURL: " + url + "\nПримечание: " + note,
                reply_markup=links_edit_menu()
            )
        else:
            bot.send_message(
                message.chat.id,
                "Неверный формат!\nИспользуйте: url|примечание\nПример: slon5.new|новое зеркало",
                reply_markup=links_edit_menu()
            )
        return

@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    user_id = call.from_user.id
    
    # Пользовательские кнопки
    if call.data == "auth":
        bot.edit_message_text(
            get_links_text(),
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=back_button()
        )
    
    elif call.data == "register":
        bot.edit_message_text(
            get_links_text(),
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=back_button()
        )
    
    elif call.data == "links":
        bot.edit_message_text(
            get_links_text(),
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=back_button()
        )
    
    elif call.data == "back":
        bot.edit_message_text(
            "Войдите, или зарегистрируйтесь",
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=main_menu()
        )
    
    # Админ кнопки
    elif call.data == "admin_edit_links":
        bot.edit_message_text(
            "Выберите ссылку для редактирования:",
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=links_edit_menu()
        )
    
    elif call.data == "admin_edit_footer":
        editing_footer.add(user_id)
        bot.edit_message_text(
            "Редактирование подписи (footer)\n\n"
            "Текущая подпись:\n" + LINKS_FOOTER + "\n\n"
            "Введите новую подпись:",
            chat_id=call.message.chat.id,
            message_id=call.message.message_id
        )
    
    elif call.data == "admin_show_links":
        bot.edit_message_text(
            get_admin_links_text(),
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=admin_menu()
        )
    
    elif call.data == "admin_logout":
        authorized_admins.discard(user_id)
        bot.edit_message_text(
            "Вы вышли из админ-панели",
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=main_menu()
        )
    
    elif call.data == "admin_back":
        bot.edit_message_text(
            "Админ-панель",
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=admin_menu()
        )
    
    elif call.data.startswith("edit_"):
        link_key = call.data.replace("edit_", "")
        
        if link_key in LINKS:
            current = LINKS[link_key]
            editing_link[user_id] = link_key
            
            bot.edit_message_text(
                "Редактирование: " + link_key + "\n\n"
                "Текущий URL: " + current['url'] + "\n"
                "Текущее примечание: " + current['note'] + "\n\n"
                "Введите новые данные в формате:\n"
                "url|примечание\n\n"
                "Пример: slon5.new|новое зеркало, используйте VPN",
                chat_id=call.message.chat.id,
                message_id=call.message.message_id
            )
    
    elif call.data == "add_new_link":
        new_key = "link" + str(len(LINKS) + 1)
        editing_link[user_id] = new_key
        
        bot.edit_message_text(
            "Добавление новой ссылки\n\n"
            "Введите данные в формате:\n"
            "url|примечание\n\n"
            "Пример: slon5.new|новое зеркало",
            chat_id=call.message.chat.id,
            message_id=call.message.message_id
        )

print("Бот запущен!")
print("Админ-панель: /admin")
print("Пароль: " + ADMIN_PASSWORD)
bot.polling(none_stop=True)