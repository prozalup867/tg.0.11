import sqlite3

# Функция для получения последней новости
def get_latest_news():
    conn = sqlite3.connect('news.db')
    cursor = conn.cursor()
    cursor.execute('SELECT title, full_text FROM news ORDER BY date DESC LIMIT 1')
    news = cursor.fetchone()
    conn.close()
    return news

# Обработчик команды news
def handle_news_command(bot, message):
    latest_news = get_latest_news()
    
    if latest_news:
        title, full_text = latest_news
        bot.send_message(message.chat.id, f"Заголовок: {title}\n\n{full_text}")
    else:
        bot.send_message(message.chat.id, "Новостей в базе данных нет.")
