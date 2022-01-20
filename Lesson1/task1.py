# Посмотреть документацию к API GitHub, разобраться как вывести список репозиториев
# для конкретного пользователя, сохранить JSON-вывод в файле *.json.

import requests
from pprint import pprint

user = input('Введите логин пользователя github: ')

response = requests.get(f'https://api.github.com/users/{user}/repos')

if response.ok:
    repos = response.json()

    with open('result1.json', 'w') as file:
        file.write(response.content.decode())

    result = []
    for repo in repos:
        result.append(repo['full_name'])
    pprint(result)

else:
    print(response.status_code)
