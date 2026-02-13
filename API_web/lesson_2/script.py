import os
import requests

from urllib.parse import urlparse

from dotenv import load_dotenv


def shorten_link(token, url):
    url_api_method_vk = 'https://api.vk.ru/method/utils.getShortLink'
    params = {
        'v': '5.199',
    }
    payload = {
        'url': url,
    }
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    response = requests.post(url_api_method_vk,
                             params=params,
                             data=payload,
                             headers=headers)
    response.raise_for_status()
    if 'error' in response.json():
        raise ValueError(response.json()['error']['error_msg'])
    return response.json()['response']['short_url']


def count_clicks(token, link):
    shortened_link = urlparse(link).path[1:]
    url_api_method_vk = 'https://api.vk.ru/method/utils.getLinkStats'
    params = {
        'v': '5.199',
    }
    payload = {
        'key': shorten_link,
    }
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    response = requests.post(url_api_method_vk,
                             params=params,
                             data=payload,
                             headers=headers)
    response.raise_for_status()
    if 'error' in response.json() :
        raise ValueError(response.json()['error']['error_msg'])
    if not response.json()['response']['stats']:
        raise ValueError('Ссылка не найдена')
    return response.json()['response']['stats'][0]['views']


def is_shorten_link(url):
    url_parse = urlparse(url)
    if (url_parse.netloc == 'vk.cc') and (len(url_parse.path) > 1):
        return True
    return False
    


def main():
    load_dotenv()
    VK_TOKEN = os.environ['VK_TOKEN']
    
    user_input_url = input('Введите ссылку для скоращения или короткую ссылку для получения статистики по ней:\n> ')

    if is_shorten_link(user_input_url):
        try:
            print(f'Количество переходов: {count_clicks(VK_TOKEN, user_input_url)}')
        except ValueError as error:
            print(f'Ошибка: {error}')
        except requests.exceptions.HTTPError as error:
            print(f'Ошибка: {error}')
    else:    
        try:
            print(f'Сокращенная ссылка: {shorten_link(VK_TOKEN, user_input_url)}')
        except ValueError as error:
            print(f'Ошибка: {error}')
        except requests.exceptions.HTTPError as error:
            print(f'Ошибка: {error}')

if __name__ == '__main__':
    main()