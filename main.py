import telebot
import schedule
import time
import logging
from threading import Thread
import commands
from parse import parse_and_add_news
from newsgpt import post_news_to_channel
from price import post_price_to_channel


channel_id = '@gribamstopniki'

# установка уровня логирования
logging.basicConfig(level=logging.INFO)

# инициализация логгера
logger = logging.getLogger(__name__)

bot = telebot.TeleBot("6287995182:AAFoMaSODWqyFXy4LNL7QU6jZwYYc5f39qM")

print("Бот запущен")

# Регистрация обработчиков команд
commands.register_commands(bot, logger)

# Вынес запуск пулинга сообщений в отдельный поток
botThread = Thread(target=bot.polling, args=())
botThread.start()

# Запускаем задание на выполнение каждые 8 и 17 часов
schedule.every().day.at("08:00").do(post_price_to_channel, bot, '@cryptonews_enterchange')
schedule.every().day.at("17:00").do(post_price_to_channel, bot, '@cryptonews_enterchange')

# Запуск парсера и добавление новостей при запуске бота
parse_and_add_news()
schedule.every(5).minutes.do(parse_and_add_news)

# Регистрируем задачу для проверки новых новостей каждую минуту
schedule.every(1).minutes.do(post_news_to_channel, bot, channel_id)  

while True:
    try:
        schedule.run_pending()
    except Exception as e:
        logger.error(f'Error running bot: {e}')