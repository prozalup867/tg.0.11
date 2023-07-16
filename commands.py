import help
import price
import chatgptapi
from parce2 import handle_news_command

def register_commands(bot, logger):
    # Обработчик команды /start
    @bot.message_handler(commands=['start'])
    def start_command(message):
        bot.reply_to(message, 'Привет! Я бот, который поможет тебе переформулировать текст командой /k и узнать курсы валют командой /price.')

    # Обработчик команды /help
    @bot.message_handler(commands=['help'])
    def send_help(message):
        bot.send_message(message.chat.id, help.help_message())

    # Обработчик команды /k
    @bot.message_handler(commands=['k'])
    def handle_k_command(message):
        text_to_rewrite = message.text[3:]
        if text_to_rewrite:
            rewritten_text = chatgptapi.rewrite_text(text_to_rewrite)
            bot.reply_to(message, rewritten_text)
        else:
            bot.reply_to(message, "Напишите текст после команды /k, чтобы я мог его переформулировать")

    # Обработчик команды /price
    @bot.message_handler(commands=['price'])
    def send_price_command(message):
        price.send_price(bot, message)

    # Обработчик команды /pprice
    @bot.message_handler(commands=['pprice'])
    def post_price_command(message):
        channel_id = '@cryptonews_enterchange'  # замените на ID вашего канала
        try:
            price.post_price_to_channel(bot, channel_id)
            logger.info('Prices posted to channel')
        except Exception as e:
            logger.error(f'Error posting prices to channel: {e}')

    # Обработчик команды /news
    @bot.message_handler(commands=['news'])
    def handle_news_command_wrapper(message):
        handle_news_command(bot, message)
