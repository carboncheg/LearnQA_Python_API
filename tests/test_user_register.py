import pytest
import string
import random
import allure
from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions


@allure.epic("User registration cases")
class TestUserRegister(BaseCase):
    excluded_params = [
        ("password"),
        ("username"),
        ("firstName"),
        ("lastName"),
        ("email")
    ]
    url = '/user'

    @allure.description("This test checks successful user registration using email, password"
                        "and filling in 'firstName', 'lastName' and 'username' fields")
    def test_create_user_successfully(self):
        data = self.prepare_registration_data()

        with allure.step("Register new user"):
            response = MyRequests.post(self.url, data=data)

        Assertions.assert_code_status(response, 200)
        Assertions.assert_json_has_key(response, 'id')

    @allure.description("This test checks unsuccessful user registration using existing email")
    def test_create_user_with_existing_email(self):
        email = 'vinkotov@example.com'
        data = self.prepare_registration_data(email)

        with allure.step(f"Try to register existing user with email='{email}'"):
            response = MyRequests.post(self.url, data=data)

        Assertions.assert_code_status(response, 400)
        Assertions.assert_expected_response_content(response, f"Users with email '{email}' already exists")

    @allure.description("This test checks unsuccessful user registration using email with incorrect format")
    def test_create_user_with_incorrect_email(self):
        incorrect_email = 'vinkotovexample.com'
        data = self.prepare_registration_data(incorrect_email)

        with allure.step(f"Try to register new user with incorrect email='{incorrect_email}'"):
            response = MyRequests.post(self.url, data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode('utf-8') == f'Invalid email format', \
            f"Unexpected response content: '{response.content}'"

    @allure.description("This test checks unsuccessful user registration "
                        "with any of required user data fields missed")
    @pytest.mark.parametrize('missed_field', excluded_params)
    def test_create_user_without_one_params(self, missed_field):
        data = self.prepare_registration_data()
        del data[f"{missed_field}"]

        with allure.step(f"Try to register new user with data field '{missed_field}' missing"):
            response = MyRequests.post(self.url, data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode('utf-8') == f"The following required params are missed: {missed_field}", \
            f"The following required params are missed: '{missed_field}'"

    @allure.description("This test checks unsuccessful user registration using too short name")
    def test_create_user_with_too_short_name(self):
        data = self.prepare_registration_data()
        short_name = data['username'] = 'u'

        with allure.step(f"Try to register new user with too short name='{short_name}'"):
            response = MyRequests.post(self.url, data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode('utf-8') == f"The value of 'username' field is too short", \
            f"The value of 'username' field is too short"

    @allure.description("This test checks unsuccessful user registration using too long name")
    def test_create_user_with_too_long_name(self):
        letter = string.ascii_lowercase
        name_length = 251
        random_string = ''.join(random.choice(letter) for _ in range(name_length))
        data = self.prepare_registration_data()
        long_name = data["username"] = random_string

        with allure.step(f"Try to register new user with too long name='{long_name}'"):
            response = MyRequests.post(self.url, data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode('utf-8') == f"The value of 'username' field is too long", \
            f"The value of 'username' field is too long"
