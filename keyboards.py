from telebot import types
from config import currencies


def create_mrk(but=None):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    buttons = []
    for val in currencies.keys():
        if val != but:
            buttons.append(val.capitalize())

    markup.add(*buttons)
    return markup
