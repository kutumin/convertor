import telebot
import json
import requests

from extensions import ConversionException,Convertor
from config import keys, TOKEN


bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['info'])
def handle_start_help(message):
        username = message.from_user.first_name
        bot.reply_to(message, "Welcome, "+ username)

@bot.message_handler(commands=['start','help'])
def start_help_123(message):
    text = "Чтобы сконвертировать валюту введите команду в следующем формате \n <имя валюты> \
<в какую валюту перевести> \
<сколько нужно перевести из одной валюты в другую> \n Чтобы увидеть список всех доступных валют введите команду /values"
    bot.reply_to(message, text)

@bot.message_handler(commands=['values'])
def values(message):
    text = "Доступные валюты:"
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')
        
        if len(values) > 3:
            raise ConversionException('Вы ввели слишком много параметров./')

        from_currency, to_currency, amount = values
        output_amount = Convertor.convert(from_currency, to_currency, amount)

    except ConversionException as e:

        bot.reply_to(message, f'Ошибка пользователя {e}')

    except Exception as e:

        bot.reply_to(message, f'Не удалось обработать команду {e}')

    else: 
        output = f'Стоимость {amount} {keys[from_currency]} в {keys[to_currency]} = {output_amount}'
        bot.reply_to(message, output)


@bot.message_handler()
def echo_test(message):
    bot.reply_to(message, "Привет!!!!это простой бот")

 
# Обрабатывается все документы и аудиозаписи
@bot.message_handler(content_types=['document', 'audio', 'photo'])
def function_name(message):
    bot.reply_to(message, "Nice meme XDD")

bot.polling(none_stop=True)