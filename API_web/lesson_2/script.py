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
    response_data = response.json()
    if 'error' in response_data:
        raise ValueError(response_data['error']['error_msg'])
    return response_data['response']['short_url']


def count_clicks(token, link):
    shortened_link = urlparse(link).path[1:]
    url_api_method_vk = 'https://api.vk.ru/method/utils.getLinkStats'
    params = {
        'v': '5.199',
    }
    payload = {
        'key': shortened_link,
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
    response_data = response.json()
    if 'error' in response_data :
        raise ValueError(response_data['error']['error_msg'])
    if not response_data['response']['stats']:
        return 0
    return response_data['response']['stats'][0]['views']


def is_shorten_link(token, url):
    try:
        count_clicks(token, url)
    except ValueError:
        return False
    return True
    

def main():
    load_dotenv()
    vk_token = os.environ['VK_TOKEN']
    user_input = input('Введите ссылку:\n> ')

    if is_shorten_link(vk_token, user_input):
        try:
            print(f'Количество переходов: {count_clicks(vk_token, user_input)}')
        except ValueError as error:
            print(f'Ошибка: {error}')
        except requests.exceptions.HTTPError as error:
            print(f'Ошибка: {error}')
    else:    
        try:
            print(f'Сокращенная ссылка: {shorten_link(vk_token, user_input)}')
        except ValueError as error:
            print(f'Ошибка: {error}')
        except requests.exceptions.HTTPError as error:
            print(f'Ошибка: {error}')

if __name__ == '__main__':
    main()