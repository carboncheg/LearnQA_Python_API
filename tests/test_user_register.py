import requests
from lib.base_case import BaseCase
from lib.assertions import Assertions
from datetime import datetime
import pytest


class TestUserRegister(BaseCase):
    excluded_params = [
        ("password"),
        ("username"),
        ("firstName"),
        ("lastName"),
        ("email")
    ]

    def setup(self):
        base_part = 'learnqa'
        domain = 'example.com'
        random_part = datetime.now().strftime('%m%d%Y%H%M%S')
        self.email = f'{base_part}{random_part}@{domain}'

    def test_create_user_successfully(self):
        data = {
            'password': '123',
            'username': 'learnqa',
            'firstName': 'learnqa',
            'lastName': 'learnqa',
            'email': self.email
        }

        response = requests.post('https://playground.learnqa.ru/api/user/', data=data)

        # Проверка на нового юзера
        Assertions.assert_code_status(response, 200)
        Assertions.assert_json_has_key(response, 'id')

    def test_create_user_with_existing_email(self):
        email = 'vinkotov@example.com'
        data = {
            'password': '123',
            'username': 'learnqa',
            'firstName': 'learnqa',
            'lastName': 'learnqa',
            'email': email
        }

        response = requests.post('https://playground.learnqa.ru/api/user/', data=data)

        # Проверка на существующий email
        Assertions.assert_code_status(response, 400)
        assert response.content.decode('utf-8') == f"Users with email '{email}' already exists", \
            f'Unexpected status code {response.content}'

    def test_create_user_with_incorrect_email(self):
        incorrect_email = 'vinkotovexample.com'
        data = {
            'password': '123',
            'username': 'learnqa',
            'firstName': 'learnqa',
            'lastName': 'learnqa',
            'email': incorrect_email
        }

        response = requests.post('https://playground.learnqa.ru/api/user/', data=data)

        # Проверка на некорректный email
        Assertions.assert_code_status(response, 400)
        assert response.content.decode('utf-8') == f'Invalid email format', \
            f"Unexpected response content: '{response.content}'"

    @pytest.mark.parametrize('missed_field', excluded_params)
    def test_create_user_without_one_params(self, missed_field):
        data = {
            'password': '123',
            'username': 'learnqa',
            'firstName': 'learnqa',
            'lastName': 'learnqa',
            'email': self.email
        }
        del data[f"{missed_field}"]

        response = requests.post('https://playground.learnqa.ru/api/user/', data=data)

        # Проверка на отсутствие одного из требуемых полей
        Assertions.assert_code_status(response, 400)
        assert response.content.decode('utf-8') == f"The following required params are missed: {missed_field}", \
            f"The following required params are missed: '{missed_field}'"

    def test_create_user_with_too_short_name(self):
        data = {
            'password': '123',
            'username': 'learnqa',
            'firstName': 'learnqa',
            'lastName': 'learnqa',
            'email': self.email
        }
        data['username'] = 'u'

        response = requests.post('https://playground.learnqa.ru/api/user/', data=data)

        # Проверка на очень короткий username
        Assertions.assert_code_status(response, 400)
        assert response.content.decode('utf-8') == f"The value of 'username' field is too short", \
            f"The value of 'username' field is too short"

