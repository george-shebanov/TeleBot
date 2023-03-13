import telebot
from config import TOKEN, keys
from extensions import APIException, Converter


def create_mrk(but=None):
    markup = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True)
    buttons = []
    for val in keys.keys():
        if val != but:
            buttons.append(val)

    markup.add(*buttons)
    return markup


bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def info_bot_message(message):
    text = """Вас приветствует Бот_Конвертер_Валют!!!

Увидеть список валют можно с помощью команды /val

Что бы начать конвертацию введите команду /conv"""
    bot.reply_to(message, text)


@bot.message_handler(commands=['val'])
def info_values(message):
    text = "доступные валюты:\n"
    for key in keys.keys():
        text = '\n'.join((text, key))
    bot.reply_to(message, text)


@bot.message_handler(commands=['conv'])
def base_handler(message: telebot.types.Message):
    text = "Выберите валюту, из которой конвентировать:"
    bot.send_message(message.chat.id, text, reply_markup=create_mrk())
    bot.register_next_step_handler(message, quote_handler)


def quote_handler(message: telebot.types.Message):
    base = message.text.strip().lower()
    text = "Выбеирте валюту, в которую конвертировать:"
    bot.send_message(message.chat.id, text, reply_markup=create_mrk(base))
    bot.register_next_step_handler(message, amount_handler, base)


def amount_handler(message: telebot.types.Message, base):
    quote = message.text.strip().lower()
    text = "Напишите количество конвертируемой валюты:"
    bot.send_message(message.chat.id, text, reply_markup=create_mrk(quote))
    bot.register_next_step_handler(message, main_handler, base, quote)


def main_handler(message: telebot.types.Message, base, quote):
    amount = message.text.strip()
    try:
        total_base = Converter.get_price(base, quote, amount)
    except APIException as a:
        bot.reply_to(message, f"Ошибка пользователя\n{a}")
    except Exception as a:
        bot.reply_to(message, f"Неудалось обработать запрос\n{a}")
    else:

        bot.send_message(message.chat.id, f"{amount} {keys[base]} = {total_base} {keys[quote]}")


bot.polling()
