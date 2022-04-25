import allure
from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions


@allure.epic("Getting user details cases")
class TestUserGet(BaseCase):

    @allure.description("This test checks unsuccessful user details getting w/o sending auth token and cookies")
    def test_get_user_details_not_auth(self):

        with allure.step("Try to get data of user with id=2"):
            response = MyRequests.get('/user/2')

        Assertions.assert_json_has_key(response, 'username')
        Assertions.assert_json_has_not_key(response, 'email')
        Assertions.assert_json_has_not_key(response, 'firstName')
        Assertions.assert_json_has_not_key(response, 'lastName')

    @allure.description("This test checks getting user details: "
                        "username, email, firstName, lastName being authorized as same user")
    def test_get_user_details_auth_as_same_user(self):
        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }
        with allure.step(f"Authorize as user with id=2 and data={data}"):
            response_1 = MyRequests.post('/user/login', data=data)

            auth_sid = self.get_cookie(response_1, 'auth_sid')
            token = self.get_header(response_1, 'x-csrf-token')
            user_id_from_auth_method = self.get_json_value(response_1, 'user_id')

        with allure.step("Get authorized user's data"):
            response_2 = MyRequests.get(
                f'/user/{user_id_from_auth_method}',
                headers={'x-csrf-token': token},
                cookies={'auth_sid': auth_sid}
            )

        expected_fields = ['username', 'email', 'firstName', 'lastName']
        Assertions.assert_json_has_keys(response_2, expected_fields)

    @allure.description("This test checks unsuccessful getting user details: "
                        "username, email, firstName, lastName, being authorized as another user")
    def test_get_user_details_auth_as_other_user(self):
        data = self.prepare_registration_data()

        with allure.step("Register user 1"):
            MyRequests.post("/user", data=data)
            login_data = {
                'email': data['email'],
                'password': data['password']
            }

        with allure.step("Authorize as user 1"):
            response_1 = MyRequests.post("/user/login", data=login_data)

            auth_sid = self.get_cookie(response_1, "auth_sid")
            token = self.get_header(response_1, "x-csrf-token")

        with allure.step("Try to get data of user with id=2, auth as user 1"):
            response_2 = MyRequests.get(
                "/user/1",
                headers={"x-csrf-token": token},
                cookies={"auth_sid": auth_sid}
            )

        Assertions.assert_json_has_key(response_2, 'username')
        Assertions.assert_json_has_not_key(response_2, 'email')
        Assertions.assert_json_has_not_key(response_2, 'firstName')
        Assertions.assert_json_has_not_key(response_2, 'lastName')
