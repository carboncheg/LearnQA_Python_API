from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions


class TestUserGet(BaseCase):
    # Неавторизованный запрос на данные. Получает только username
    def test_get_user_details_not_auth(self):
        response = MyRequests.get('/user/2')

        Assertions.assert_json_has_key(response, 'username')
        Assertions.assert_json_has_not_key(response, 'email')
        Assertions.assert_json_has_not_key(response, 'firstName')
        Assertions.assert_json_has_not_key(response, 'lastName')

    # Авторизованный запрос. Авторизует под пользователем с ID 2 и
    # делает запрос для получения данных того же пользователя и получает все поля
    def test_get_user_details_auth_as_same_user(self):
        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }

        response_1 = MyRequests.post('/user/login', data=data)

        auth_sid = self.get_cookie(response_1, 'auth_sid')
        token = self.get_header(response_1, 'x-csrf-token')
        user_id_from_auth_method = self.get_json_value(response_1, 'user_id')

        response_2 = MyRequests.get(
            f'/user/{user_id_from_auth_method}',
            headers={'x-csrf-token': token},
            cookies={'auth_sid': auth_sid}
        )

        expected_fields = ['username', 'email', 'firstName', 'lastName']
        Assertions.assert_json_has_keys(response_2, expected_fields)

    # Авторизованный запрос. Создаёт нового пользователя, авторизует под новым пользователем и
    # делает запрос для получения данных другого пользователя и получает лишь username
    def test_get_user_details_auth_as_other_user(self):
        data = self.prepare_registration_data()
        MyRequests.post("/user", data=data)
        login_data = {
            'email': data['email'],
            'password': data['password']
        }
        response_1 = MyRequests.post("/user/login", data=login_data)
        auth_sid = self.get_cookie(response_1, "auth_sid")
        token = self.get_header(response_1, "x-csrf-token")

        response_2 = MyRequests.get(
            "/user/1",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )

        Assertions.assert_json_has_key(response_2, 'username')
        Assertions.assert_json_has_not_key(response_2, 'email')
        Assertions.assert_json_has_not_key(response_2, 'firstName')
        Assertions.assert_json_has_not_key(response_2, 'lastName')
