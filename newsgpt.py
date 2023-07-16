import sqlite3
import telebot
from datetime import datetime
from parse import get_html, parse_and_add_news
from chatgptapi import rewrite_text


# Замените на свой токен
channel_id = '@gribamstopniki'

def get_latest_news_from_db():
    conn = sqlite3.connect('news.db')
    c = conn.cursor()
    c.execute("SELECT * FROM news WHERE rewritten = 0 ORDER BY id DESC LIMIT 1;")
    result = c.fetchone()
    conn.close()
    return result

def is_news_new(news_date, link):
    try:
        news_date = datetime.strptime(news_date + ":00", '%d.%m.%Y %H:%M:%S')
        current_time = datetime.now()
        time_difference = current_time - news_date
        return time_difference.total_seconds() < 172800
    except ValueError as e:
        print(f"Error parsing date: {e}")
        return False

def post_news_to_channel(bot, channel_id):
    news = get_latest_news_from_db()
    if news:
        title, date, link, text, full_text, rewritten = news[1], news[2], news[3], news[4], news[5], news[6]
        if is_news_new(date, link):
            # Вызываем функцию rewrite_text для рерайта полного текста новости
            rewritten_full_text = rewrite_text(full_text)

            message = f"*{title}*\n\n{rewritten_full_text}\n\n[Read more]({link})"
            bot.send_message(channel_id, message, parse_mode='Markdown', disable_web_page_preview=False)

            # Обновляем статус rewritten для новости в базе данных
            conn = sqlite3.connect('news.db')
            c = conn.cursor()
            c.execute("UPDATE news SET rewritten = 1 WHERE id = ?", (news[0],))
            conn.commit()
            conn.close()

            print(f"Новая новость опубликована: {title} ({date})")
        else:
            print(f"Новость не опубликована: {title} ({date})")


if __name__ == '__main__':
    parse_and_add_news()
