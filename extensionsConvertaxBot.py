import requests
import json


# Валютный словарь
currency = {
    'рубль': 'RUB',
    'доллар': 'USD',
    'евро': 'EUR',
    'рупия': 'INR'
}


# Класс исключений
class APIException(Exception):
    pass


# Класс конвертаций
class Converter:
    @staticmethod
    # Метод отправки запросов к API
    def get_price(quote: str, base: str, amount: str):
        if quote == base:
            raise APIException(f'⚠️Невозможно конвертировать одинаковые валюты "{base}".')

        try:
            quote_ticker = currency[quote]
        except KeyError:
            raise APIException(f'⚠️Не удалось обработать валюту "{quote}"')

        try:
            base_ticker = currency[base]
        except KeyError:
            raise APIException(f'⚠️Не удалось обработать валюту "{base}"')

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'⚠️Не удалось обработать количество "{amount}"')

        # Отправляем запрос к API
        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}')
        # Присваиваем ответ (за единицу валюты) от API переменной.
        r_base = json.loads(r.content)[currency[base]]
        # Присваиваем переменной значение, полученное от произведения количества валюты на стоимость.
        total_base = r_base * amount

        # Возвращаем значение результата конвертации
        return total_base
