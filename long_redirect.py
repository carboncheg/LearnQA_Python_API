import requests

response = requests.request('get', 'https://playground.learnqa.ru/api/long_redirect')
print(f'Количество редиректов: {len(response.history)}')
print(f'Конечный URL: {response.url}')
