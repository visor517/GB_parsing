'''
Развернуть у себя на компьютере/виртуальной машине/хостинге MongoDB и реализовать функцию,
которая будет добавлять только новые вакансии в вашу базу.
'''

import requests
import re
from bs4 import BeautifulSoup
from pprint import pprint
from http import client
from pymongo import MongoClient, errors

search = input('Введите запрос: ')

url = 'https://hh.ru'
params = {'text': search, 'page': 1}
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 \
    (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36'}

client = MongoClient('127.0.0.1', 27017)
db = client['my_db']

db_vacancy = db.vacancy

# счетчик добавленных вакансий
vacancies_added = 0

# основной цикл сбора и переключения страниц
while True:
    response = requests.get(url + '/search/vacancy', params=params, headers=headers)
    dom = BeautifulSoup(response.text, 'html.parser')
    vacancies_list = dom.find_all('div', {'class': 'vacancy-serp-item__row_header'})

    if len(vacancies_list) == 0:
        break

    for vacancy in vacancies_list:
        vacancy_data = {}

        title = vacancy.find('a', {'data-qa': 'vacancy-serp__vacancy-title'})
        vacancy_data['name'] = title.getText()
        vacancy_data['link'] = title.get('href').split('?')[0]

        # разбираем оклад на три части
        vacancy_data['compensation_min'] = None
        vacancy_data['compensation_max'] = None
        vacancy_data['compensation_currency'] = None
        try:
            compensation = str(vacancy.find('span', {'data-qa': 'vacancy-serp__vacancy-compensation'}).getText())
            compensation = compensation.replace('\u202f', '')
            digits = re.findall(r'\d+', compensation, flags=0)

            if compensation.startswith('от'):
                vacancy_data['compensation_min'] = int(digits[0])
            elif compensation.startswith('до'):
                vacancy_data['compensation_max'] = int(digits[0])
            else:
                vacancy_data['compensation_min'] = int(digits[0])
                vacancy_data['compensation_max'] = int(digits[1])

            vacancy_data['compensation_currency'] = compensation.split(' ')[-1]
        except:
            pass

        # добавляем вакансию в базу
        try:
            if not db_vacancy.find_one({'link': vacancy_data['link']}):
                db_vacancy.insert_one(vacancy_data)
                vacancies_added += 1
        except errors.DuplicateKeyError:
            pass

    params['page'] += 1

print(f'Добавлено {vacancies_added} вакансий')
