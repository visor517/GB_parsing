'''
Необходимо собрать информацию о вакансиях на вводимую должность (используем input или через аргументы
получаем должность) с сайтов HH(обязательно) и/или Superjob(по желанию). Приложение должно анализировать
несколько страниц сайта (также вводим через input или аргументы).
'''

import requests
import re
from bs4 import BeautifulSoup
from pprint import pprint

url = 'https://hh.ru'
params = {'text': 'Python стажер'}
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36'}

response = requests.get(url + '/search/vacancy', params=params, headers=headers)

dom = BeautifulSoup(response.text, 'html.parser')

vacancies_list = dom.find_all('div', {'class': 'vacancy-serp-item__row_header'})

vacancies  = []

for vacancy in vacancies_list:
    vacancy_data = {}

    title = vacancy.find('a', {'data-qa': 'vacancy-serp__vacancy-title'})
    vacancy_data['name'] = title.getText()
    vacancy_data['link'] = title.get('href')
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

    vacancies.append(vacancy_data)
    
pprint(vacancies)
