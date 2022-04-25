import json.decoder
from requests import Response
from lib.my_requests import MyRequests
from datetime import datetime
from typing import Tuple


class BaseCase:
    def get_cookie(self, response: Response, cookie_name):
        assert cookie_name in response.cookies, f'Cannot find cookie with name {cookie_name} in the last response'
        return response.cookies[cookie_name]

    def get_header(self, response: Response, headers_name):
        assert headers_name in response.headers, f'Cannot find headers with name {headers_name} in the last response'
        return response.headers[headers_name]

    def get_json_value(self, response: Response, name):
        try:
            response_as_dict = response.json()
        except json.decoder.JSONDecodeError:
            assert False, f'Response is not in JSON format. Response text is "{response.text}"'

        assert name in response_as_dict, f'Response JSON doesn\'t have key "{name}"'
        return response_as_dict[name]

    def prepare_registration_data(self, email=None):
        if email is None:
            base_part = 'learnqa'
            domain = 'example.com'
            random_part = datetime.now().strftime('%d%m%Y%H%M%S%f')
            email = f'{base_part}{random_part}@{domain}'
        return {
            'password': '123',
            'username': 'learnqa',
            'firstName': 'learnqa',
            'lastName': 'learnqa',
            'email': email
        }

    def generate_new_user(self) -> Tuple[Response, dict]:
        user_data = self.prepare_registration_data()
        return MyRequests.post('/user', data=user_data), user_data
