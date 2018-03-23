import telebot
from telebot import types

#получаем настройки бота из settings.json

import sqlite3

# Создаем соединение с нашей базой данных
# В нашем примере у нас это просто файл базы
conn = sqlite3.connect('db.sqlite3')




TOKEN = '460229690:AAGfrgxIU1Hh6dBAv0LoYsAWd4YUF7cvLHQ'
bot = telebot.TeleBot(TOKEN)
ftypes = []
# работа с inline клавиатурой

@bot.callback_query_handler(func=lambda call: True)
def query_handler(call):
    # Создаем курсор - это специальный объект который делает запросы и получает их результаты
    cursor = conn.cursor()
    if call.data == 'like':
        cursor.execute(" UPDATE facebot_messagereaction SET likecount = 1 WHERE chat_id ="+str(call.message.chat.id)"+";")
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(types.InlineKeyboardButton(text="text",callback_data = "text"))    
        bot.edit_message_reply_markup(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=keyboard
        )  
    # Не забываем закрыть соединение с базой данных
    conn.close()
if __name__ == '__main__':
     bot.polling(none_stop=True)
