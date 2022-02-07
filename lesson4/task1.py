'''
Написать приложение, которое собирает основные новости с сайта news.mail.ru.
Для парсинга использовать XPath. Структура данных должна содержать:
название источника / наименование новости / ссылку на новость / дата публикации.
Сложить собранные новости в БД
'''

import requests
from lxml import html
from pymongo import MongoClient, errors


client = MongoClient('127.0.0.1', 27017)
db = client['my_db']
db_news = db.news

url = 'https://news.mail.ru/'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36'}
response = requests.get(url, headers=headers)
dom = html.fromstring(response.text)
links = dom.xpath("//div[contains(@class, 'daynews__item')]/a/@href | //li[@class='list__item']/a/@href")

# счетчик добавленных вакансий
news_added = 0

for link in links:
    response = requests.get(link, headers=headers)
    dom = html.fromstring(response.text)

    data = {}
    data['name'] = dom.xpath("//h1/text()")[0]
    data['link'] = link
    data['source'] = dom.xpath("//a[contains(@class, 'breadcrumbs__link')]/span/text()")[0]
    data['date'] = dom.xpath("//span[@datetime]/@datetime")[0]

    # добавляем новость в базу
    try:
        if not db_news.find_one({'link': data['link']}):
            db_news.insert_one(data)
            news_added += 1
    except errors.DuplicateKeyError:
        pass

print(f'Добавлено {news_added} новостей')
