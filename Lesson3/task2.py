'''
Написать функцию, которая производит поиск и выводит на экран вакансии с заработной платой больше введённой
суммы (необходимо анализировать оба поля зарплаты). То есть цифра вводится одна, а запрос проверяет оба поля
'''

from http import client
from pymongo import MongoClient
from pprint import pprint

client = MongoClient('127.0.0.1', 27017)

db = client['my_db']

db_vacancy = db.vacancy

compensation = int(input('Введите зарплату в рублях: '))

for vacancy in db_vacancy.find({'$or': [{'compensation_max': {'$gte': compensation}},   # если макс больше, то точно годится
                                        {'compensation_min': {'$gte': compensation}}],  # если мин меньше и до небыло, то я считаю, что не годится
                                'compensation_currency': 'руб.'}):

    pprint(vacancy)
