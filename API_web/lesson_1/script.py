import requests


url = 'https://wttr.in/'
payload = {'nTqM': '', 'lang': 'ru'}
cities = ['london', 'svo', 'cherepovets']

def main():
    for city in cities:
        try:
            response = requests.get(f'{url}{city}', params=payload)
            response.raise_for_status()
            print(response.text)
        except requests.exceptions.HTTPError as error:
            print(f'Ошибка получения данных с сервера:\n{error}')
        except Exception as error:
            print(f'Неизвестная ошибка:\n{error}')

if __name__ == '__main__':
    main()