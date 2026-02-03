import requests


URL = 'https://wttr.in/'
payload = 'nTqM&lang=ru'
cities = ['london', 'svo', 'cherepovets']

if __name__ == '__main__':
    try:
        for city in cities:
            response = requests.get(f'{URL}{city}', params=payload)
            response.raise_for_status()
            print(response.text)
    except requests.exceptions.HTTPError as error:
        exit(f'Ошибка получения данных с сервера:\n{error}')