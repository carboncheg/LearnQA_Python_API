import requests
from lib.base_case import BaseCase
from lib.assertions import Assertions
import pytest
import string
import random


class TestUserRegister(BaseCase):
    excluded_params = [
        ("password"),
        ("username"),
        ("firstName"),
        ("lastName"),
        ("email")
    ]
    url = 'https://playground.learnqa.ru/api/user/'

    def test_create_user_successfully(self):
        data = self.prepare_registration_data()

        response = requests.post(self.url, data=data)

        # Проверка на успешное создание нового юзера
        Assertions.assert_code_status(response, 200)
        Assertions.assert_json_has_key(response, 'id')

    def test_create_user_with_existing_email(self):
        email = 'vinkotov@example.com'
        data = self.prepare_registration_data(email)

        response = requests.post(self.url, data=data)

        # Проверка на существующий email
        Assertions.assert_code_status(response, 400)
        assert response.content.decode('utf-8') == f"Users with email '{email}' already exists", \
            f'Unexpected status code {response.content}'

    def test_create_user_with_incorrect_email(self):
        incorrect_email = 'vinkotovexample.com'
        data = self.prepare_registration_data(incorrect_email)

        response = requests.post(self.url, data=data)

        # Проверка на некорректный email
        Assertions.assert_code_status(response, 400)
        assert response.content.decode('utf-8') == f'Invalid email format', \
            f"Unexpected response content: '{response.content}'"

    @pytest.mark.parametrize('missed_field', excluded_params)
    def test_create_user_without_one_params(self, missed_field):
        data = self.prepare_registration_data()
        del data[f"{missed_field}"]

        response = requests.post(self.url, data=data)

        # Проверка на отсутствие одного из требуемых полей
        Assertions.assert_code_status(response, 400)
        assert response.content.decode('utf-8') == f"The following required params are missed: {missed_field}", \
            f"The following required params are missed: '{missed_field}'"

    def test_create_user_with_too_short_name(self):
        data = self.prepare_registration_data()
        data['username'] = 'u'

        response = requests.post(self.url, data=data)

        # Проверка на очень короткий username
        Assertions.assert_code_status(response, 400)
        assert response.content.decode('utf-8') == f"The value of 'username' field is too short", \
            f"The value of 'username' field is too short"

    def test_create_user_with_too_long_name(self):
        letter = string.ascii_lowercase
        name_length = 251
        random_string = ''.join(random.choice(letter) for _ in range(name_length))
        data = self.prepare_registration_data()
        data["username"] = random_string

        response = requests.post(self.url, data=data)

        # Проверка на очень длинный username
        Assertions.assert_code_status(response, 400)
        assert response.content.decode('utf-8') == f"The value of 'username' field is too long", \
            f"The value of 'username' field is too long"
