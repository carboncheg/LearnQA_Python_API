import requests


class TestGetCookie:
    def test_get_cookie(self):
        response = requests.get('https://playground.learnqa.ru/api/homework_cookie')
        cookie_value = response.cookies.get('HomeWork')
        print(f'\nCookie: {cookie_value}')
        assert cookie_value == 'hw_value', f'Expected cookie with value "hw_value"'
