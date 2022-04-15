import requests


class TestGetHeaders:
    def test_get_headers(self):
        response = requests.get('https://playground.learnqa.ru/api/homework_cookie')
        header_value = response.headers.get('Set-Cookie')
        print(f'\n{header_value}')
        header_part = 'HomeWork=hw_value'
        assert header_part in header_value, f'Expected "HomeWork=hw_value" in "{header_value}"'
