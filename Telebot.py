import telebot
from config import TOKEN, currencies
from extensions import APIException, Converter
from keyboards import create_mrk

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def preview(message: telebot.types.Message):
    text = """Вас приветствует бот конвертор валют

чтобы посмотреть список доступных валют используйте команду /values

чтобы начать конвертацию используйте команду /convert"""

    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['values'])
def val_info(message: telebot.types.Message):
    text = "Доступные валюты:"
    for val in currencies.keys():
        text = '\n'.join((text, val))

    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['convert'])
def insert_values(message: telebot.types.Message):
    text = "Выберите валюту из которой конвертировать"
    bot.send_message(message.chat.id, text, reply_markup=create_mrk())
    bot.register_next_step_handler(message, base_curr)


def base_curr(message: telebot.types.Message):
    base = message.text.strip().lower()
    text = "Выберите валюту в котрую конвертировать"
    bot.send_message(message.chat.id, text, reply_markup=create_mrk())
    bot.register_next_step_handler(message, quote_curr, base)


def quote_curr(message: telebot.types.Message, base):
    quote = message.text.strip().lower()
    text = 'Напишите количество конвертируемой валюты'
    bot.send_message(message.chat.id, text)
    bot.register_next_step_handler(message, start_convert, base, quote)


def start_convert(message: telebot.types.Message, base, quote):
    amount = message.text.strip()
    try:
        result = Converter.get_price(base, quote, amount)
    except APIException as e:
        bot.send_message(message.chat.id, f'Ошибка пользователя:\n{e}')
    except Exception as e:
        bot.send_message(message.chat.id, f'Ошибка системы\n{e}')
    else:
        bot.send_message(message.chat.id, f'Результат конвертации:\n{amount} {base} = {result} {quote}')


bot.polling()
