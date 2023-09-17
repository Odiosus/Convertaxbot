import telebot
from сonfigConvertaxBot import TOKEN
from extensionsConvertaxBot import APIException, Converter, currency


# Указываем Токен для доступа к боту
bot = telebot.TeleBot(TOKEN)


# Приветственный текст. Переход в раздел Список валют и Помощь по активным ссылкам-командам.
start_txt = "Привет! Я конвертирую валюты. Введи команду в формате: \
\n_<исходная валюта> <валюта назначения> <количество исходной валюты>_. \n\n*Пример:* рубль доллар 99 \
\n\nСписок валют 👉 /values \nПомощь 👉 /help"

# Текст раздела Помощи с инструкцией. Возможность копипаста валюты в один тык.
help_txt = ("Что-то пошло не так? Тогда давай по пунктам: \n1. Соблюдай порядок: \
\n_<исходная валюта>_ — та, что в кармане;\n_<валюта назначения>_ — та, которую хочется;\
\n_<количество исходной валюты>_ — сколько есть в кармане.\n2. Не забывай пробелы. \
\n3. Количество исходной валюты указывай целым числом — копейки для неудачников.\n\n*Пример: рубль доллар 99* \
\n\nСовсем для ленивых. Тут 👇 можно тыкнуть на валюту, чтобы её скопировать (даже пробелы ставить не нужно! Сказка!): \
\n|  `рубль `|  `доллар `|  `евро `|  `рупия `|")


# Старт бота
@bot.message_handler(commands=['start'])
def start(message):
    # Приветственное сообщение
    bot.send_message(message.from_user.id, start_txt, parse_mode='Markdown')


# Раздел помощи с инструкциями
@bot.message_handler(commands=['help'])
def help(message: telebot.types.Message):
    # Текст помощи с инструкциями
    bot.reply_to(message, help_txt, parse_mode='Markdown')


# Раздел Списка валют
@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    # Текст раздела Список валют. Список забираем из Валютного словаря.
    values_txt = '*Доступные валюты:*'
    for key in currency.keys():
        values_txt = '\n'.join((values_txt, key,))
    bot.reply_to(message, values_txt, parse_mode='Markdown')


# Раздел конвертера
@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        # Склеиваем пробелом значения переменной
        options = message.text.split(' ')

        if len(options) != 3:
            raise APIException('Слишком много параметров 🔙')

        # Устанавливаем значение переменной из аргументов
        quote, base, amount = options
        # Вытаскиваем значения из класса Конвертаций
        total_base = Converter.get_price(quote, base, amount)
    # Сообщаем об ошибках
    except APIException as e:
        bot.reply_to(message, f'⛔️Пользовательская ошибка\n{e}')
    except Exception as e:
        bot.reply_to(message, f'⚠️Не удалось обработать команду\n{e}')
    else:
        # Финальный текст с результатом
        text = f'Цена {amount} {quote} — {total_base} {base}'
        bot.send_message(message.chat.id, text)


bot.polling()
