import json
from telebot import types
class MyKeyboard:
    def __init__(self, keys):
        self.keys = keys
    def getKeyboard(self):
        raise NotImplementedError()

class MyInlineKeyboard(MyKeyboard):
    def getKeyboard(self):
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(*[types.InlineKeyboardButton(text=text,
        callback_data = text) for text in self.keys])
        return keyboard   

class MyReplyKeyboard(MyKeyboard):
    def getKeyboard(self):
        keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        for item in self.keys:
            keyboard.add(item)
        return keyboard

class MyLinkKeyboard(MyKeyboard):
    def getKeyboard(self):
        keyboard= types.InlineKeyboardMarkup()
        for i in range(0,len(self.keys),2):
            btn_my= types.InlineKeyboardButton(text=self.keys[i], url=self.keys[i+1])
            keyboard.add(btn_my)
        return keyboard

class GenerateKeyboard():
    def create_keyboard(type_keyboard, keys):
        if type_keyboard == 'inline':
            return MyInlineKeyboard(keys).getKeyboard()
        elif type_keyboard == 'reply':
            return MyReplyKeyboard(keys).getKeyboard()
        elif type_keyboard == 'link':
            return MyLinkKeyboard(keys).getKeyboard()
            