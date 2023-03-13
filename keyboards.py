from telebot import types
from config import keys


def create_mrk(but=None):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    buttons = []
    for val in keys.keys():
        if val != but:
            buttons.append(val)

    markup.add(*buttons)
    return markup
