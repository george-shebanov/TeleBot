import requests
import json

from config import currencies,key


class APIException(Exception):
    pass


class Converter:
    @staticmethod
    def get_price(base, quote, amount):
        if base == quote:
            raise APIException("Невозможно конвертировать одинаковые валюты")
        try:
            base_tiker = currencies[base]
        except KeyError:
            raise APIException(f"Невозможно обработать валюту: {base}")
        try:
            quote_tiker = currencies[quote]
        except KeyError:
            raise APIException(f"Невозможно обработать валюту: {quote}")
        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f"Неверное количаство валют: {amount}")

        url = f"https://api.apilayer.com/currency_data/convert?to={quote_tiker}&from={base_tiker}&amount={amount}"

        payload = {}
        headers = {
            "apikey": key
        }

        response = requests.request("GET", url, headers=headers, data=payload)

        res = round(json.loads(response.content)['result'], 2)

        return res
