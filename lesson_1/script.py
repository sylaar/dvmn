import requests


URL = 'https://wttr.in/'
PAYLOAD = {'nTqM': '', 'lang': 'ru'}
CITIES = ['london', 'svo', 'cherepovets']

def main():
    for city in CITIES:
        try:
            response = requests.get(f'{URL}{city}', params=PAYLOAD)
            response.raise_for_status()
            print(response.text)
        except requests.exceptions.HTTPError as error:
            print(f'Ошибка получения данных с сервера:\n{error}')
        except Exception as error:
            print(f'Неизвестная ошибка:\n{error}')

if __name__ == '__main__':
    main()