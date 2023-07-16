import requests

def get_usd_rate():
    response = requests.get("https://www.cbr-xml-daily.ru/daily_json.js")
    data = response.json()
    return round(data["Valute"]["USD"]["Value"], 2)

def get_usdt_rate():
    response = requests.get("https://api.binance.com/api/v3/ticker/price?symbol=USDTRUB")
    data = response.json()
    return float(data["price"])

def send_price(bot, message):
    pairs = [
    ("USDTRUB", "🔹 USD/RUB"),
    ("USDTRUB", "🔹 USDT/RUB "), # изменение названия пары
    ("BTCUSDT", "🔹 BTC/USDT "),
    ("ETHUSDT", "🔹 ETH/USDT "),
    ("LTCUSDT", "🔹 LTC/USDT  "),
    ("XMRUSDT", "🔹 XMR/USDT")
]


    usd_rate = get_usd_rate()
    if usd_rate is None:
        bot.reply_to(message, "Ошибка получения курса USD/RUB")
        return
    else:
        response_text = f"<b>Текущие курсы:</b>\n🔹 USD/RUB ЦБ РФ: {usd_rate}\n"

    for symbol, pair in pairs[1:]:
        url = f"https://api.binance.com/api/v3/ticker/24hr?symbol={symbol}"
        response = requests.get(url)
        json_data = response.json()
        if "lastPrice" in json_data:
            pair_price = float(json_data["lastPrice"])
            open_price = float(json_data["openPrice"])
            change_percentage = round(((pair_price - open_price) / open_price) * 100, 2)
            emoji = "📈" if change_percentage >= 0 else "📉"
            change_percentage_text = f"{'+' if change_percentage > 0 else ''}{change_percentage:.2f}%"
            response_text += f"{pair} {emoji} {pair_price:.2f} ({change_percentage_text})\n"
        else:
            response_text += f"{pair}: Ошибка получения курса\n"

    response_text += '<a href="http://enter-change.com/">Надежный обменный сервис криптовалюты enter-change</a>'
    bot.reply_to(message, response_text, parse_mode="HTML")


def get_usd_rate():
    response = requests.get("https://www.cbr-xml-daily.ru/daily_json.js")
    data = response.json()
    return round(data["Valute"]["USD"]["Value"], 2)

def get_usdt_rate():
    response = requests.get("https://api.binance.com/api/v3/ticker/price?symbol=USDTRUB")
    data = response.json()
    return float(data["price"])

def post_price_to_channel(bot, channel_id):
    print('Posting prices to channel')
    pairs = [
    ("USDTRUB", "🔹 USD/RUB"),
    ("USDTRUB", "🔹 USDT/RUB "), # изменение названия пары
    ("BTCUSDT", "🔹 BTC/USDT "),
    ("ETHUSDT", "🔹 ETH/USDT "),
    ("LTCUSDT", "🔹 LTC/USDT  "),
    ("XMRUSDT", "🔹 XMR/USDT")
]

    response_text = "<b>Текущие курсы:</b>\n"
    usd_rate = get_usd_rate()
    if usd_rate is not None:
        response_text += f"🔹 USD/RUB ЦБ РФ: {usd_rate}\n"
    else:
        response_text += "🔹 USD/RUB: Ошибка получения курса\n"

    for symbol, pair in pairs[1:]:
        if pair == "🔹 USD/RUB":
            continue
        url = f"https://api.binance.com/api/v3/ticker/24hr?symbol={symbol}"
        response = requests.get(url)
        json_data = response.json()
        if "lastPrice" in json_data:
            pair_price = float(json_data["lastPrice"])
            open_price = float(json_data["openPrice"])
            change_percentage = round(((pair_price - open_price) / open_price) * 100, 2)
            emoji = "📈" if change_percentage >= 0 else "📉"
            response_text += f"{pair} {emoji}: {pair_price:.2f} ({'+' if change_percentage > 0 else ''}{change_percentage:.2f}%)\n"
        else:
            response_text += f"{pair}: Ошибка получения курса\n"

    response_text += '<a href="http://enter-change.com/">Надежный обменный сервис криптовалюты enter-change</a>'
    bot.send_message(chat_id=channel_id, text=response_text, parse_mode="HTML")
