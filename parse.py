import requests
from bs4 import BeautifulSoup
import sqlite3
import logging
import re

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

URL = 'https://forklog.com/news'

def get_html(url):
    try:
        r = requests.get(url)
        r.raise_for_status()
        return r.text
    except requests.exceptions.RequestException as err:
        logger.error(f"Error: {err}")
    return None

def get_full_text(link):
    html = get_html(link)
    if html:
        soup = BeautifulSoup(html, 'html.parser')
        full_text_block = soup.find('div', class_='post_content')
        if full_text_block:
            paragraphs = full_text_block.find_all('p')
            full_text = ' '.join([p.get_text(strip=True) for p in paragraphs])
            return full_text.strip()
    return ""

def get_data(html):
    soup = BeautifulSoup(html, 'html.parser')
    news_block = soup.find_all('div', class_='post_item')
    news = []

    for item in news_block:
        title = item.find('div', class_='text_blk').find('p').get_text(strip=True)
        link = item.find('a')['href']
        text = item.find('div', class_='text_blk').find('span', class_='post_excerpt').get_text(strip=True)
        full_text = get_full_text(link)
        post_date = item.get('data-full_datetime')

        news.append({'title': title, 'link': link, 'text': text, 'full_text': full_text, 'date': post_date})

    return news

def preprocess_full_text(text):
    text = re.sub(r'http\S+', '', text)
    text = text.replace("Read more", "")
    text = re.sub(r'src="([^"]+)" data-tweet-id="[^"]+"', '', text)
    text = text[:2000]
    return text.strip()

def add_to_database(news):
    conn = sqlite3.connect('news.db')
    c = conn.cursor()

    try:
        c.execute('''CREATE TABLE IF NOT EXISTS news
                     (id INTEGER PRIMARY KEY AUTOINCREMENT,
                      title TEXT,
                      date TEXT,
                      link TEXT UNIQUE,
                      text TEXT,
                      full_text TEXT,
                      rewritten INTEGER DEFAULT 0);''')

        for item in news:
            truncated_full_text = preprocess_full_text(item['full_text'])
            try:
                c.execute("INSERT INTO news (title, date, link, text, full_text) VALUES (?, ?, ?, ?, ?)",
                          (item['title'], item['date'], item['link'], item['text'], truncated_full_text))
                logger.info(f"Добавлена новость в базу данных: {item['title']}")
                print(f"Добавлена новость в базу данных: {item['title']}")
            except sqlite3.IntegrityError:
                pass
    except sqlite3.Error as e:
        logger.error(f"Error adding news to database: {e}")
    finally:
        conn.commit()
        conn.close()

def parse_and_add_news():
    print("Парсинг новостей запущен...")
    html = get_html(URL)
    if html:
        news = get_data(html)
        add_to_database(news)
    else:
        logger.error("Failed to get HTML content.")

if __name__ == '__main__':
    parse_and_add_news()
