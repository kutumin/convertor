import telebot
import requests
from config import keys, TOKEN
import json

class ConversionException(Exception):
    pass

class Convertor:
    @staticmethod
    def convert(from_currency:str, to_currency:str, amount: str):

        if from_currency == to_currency:

            raise ConversionException(f'Невозможно перевести одинаковые валюты {from_currency}')

        try: 
            from_currency_ticker = keys[from_currency]

        except KeyError:
            raise ConversionException(f'Не удалось обработать валюту {from_currency}')

        try: 
            to_currency_ticker = keys[to_currency]

        except KeyError:
            
            raise ConversionException(f'Не удалось обработать валюту {to_currency}')

        try:
            amount_ticker=float(amount)
        
        except ValueError:

            raise ConversionException(f'Не удалось обработать количество {amount}')

        r = requests.get(f'https://api.frankfurter.app/latest?amount={amount_ticker}=10&from={from_currency_ticker}&to={to_currency_ticker}')
        output_base = json.loads(r.content)['rates'][keys[to_currency]]

        return output_base
