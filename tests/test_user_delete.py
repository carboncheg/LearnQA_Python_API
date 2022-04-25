import allure
from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions


@allure.epic("User deleting cases")
class TestUserDelete(BaseCase):

    @allure.description("This test checks authorized protected user cannot delete himself")
    def test_delete_protected_user(self):
        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }
        with allure.step(f"Authorize as user with id=2 and data={data}"):
            response_1 = MyRequests.post("/user/login", data=data)
            auth_sid = self.get_cookie(response_1, "auth_sid")
            token = self.get_header(response_1, "x-csrf-token")

        with allure.step("Try to delete user with id=2"):
            response_2 = MyRequests.delete(
                f"/user/2",
                headers={"x-csrf-token": token},
                cookies={"auth_sid": auth_sid},
            )

        Assertions.assert_code_status(response_2, 400)
        Assertions.assert_expected_response_content(
            response_2, "Please, do not delete test users with ID 1, 2, 3, 4 or 5.")

    @allure.description("This test checks successful deleting authorized user")
    def test_delete_user_successfully(self):

        # REGISTER
        with allure.step("Register new user"):
            response_1, registration_data = self.generate_new_user()

        Assertions.assert_code_status(response_1, 200)
        Assertions.assert_json_has_key(response_1, "id")

        email = registration_data['email']
        password = registration_data['password']
        user_id = self.get_json_value(response_1, "id")

        # LOGIN
        login_data = {
            'email': email,
            'password': password
        }
        with allure.step(f"Authorize as registered user with data={login_data}"):
            response_2 = MyRequests.post("/user/login", data=login_data)
            auth_sid = self.get_cookie(response_2, "auth_sid")
            token = self.get_header(response_2, "x-csrf-token")

        # DELETE
        with allure.step("Try to delete authorized user"):
            response_3 = MyRequests.delete(
                f"/user/{user_id}",
                headers={"x-csrf-token": token},
                cookies={"auth_sid": auth_sid},
            )

        Assertions.assert_code_status(response_3, 200)

        # GET
        with allure.step("Check user is deleted"):
            response_4 = MyRequests.get(
                f"/user/{user_id}",
                headers={"x-csrf-token": token},
                cookies={"auth_sid": auth_sid}
            )

        Assertions.assert_code_status(response_4, 404)
        Assertions.assert_expected_response_content(response_4, "User not found")

    @allure.description("This test checks authorized user can not delete another user")
    def test_delete_user_auth_as_another_user(self):

        # REGISTER USER 1
        with allure.step("Register user 1"):
            response_1, registration_data_1 = self.generate_new_user()

        Assertions.assert_code_status(response_1, 200)
        Assertions.assert_json_has_key(response_1, "id")

        email_1 = registration_data_1['email']
        password_1 = registration_data_1['password']

        # REGISTER USER 2
        with allure.step("Register user 2"):
            response_2, registration_data_2 = self.generate_new_user()

        Assertions.assert_code_status(response_2, 200)
        Assertions.assert_json_has_key(response_2, "id")

        email_2 = registration_data_2['email']
        password_2 = registration_data_2['password']
        user_id_2 = self.get_json_value(response_2, "id")

        # LOGIN AS USER 1
        login_data_1 = {
            'email': email_1,
            'password': password_1
        }
        with allure.step("Authorize as user 1"):
            response_3 = MyRequests.post("/user/login", data=login_data_1)
            auth_sid_1 = self.get_cookie(response_3, "auth_sid")
            token_1 = self.get_header(response_3, "x-csrf-token")

        # DELETE USER 2 BY USER 1
        with allure.step("Try to delete user 2"):
            MyRequests.delete(
                f"/user/{user_id_2}",
                headers={"x-csrf-token": token_1},
                cookies={"auth_sid": auth_sid_1}
            )

        # LOGIN AS USER 2
        login_data_2 = {
            'email': email_2,
            'password': password_2
        }
        with allure.step("Authorize as user 2"):
            response_5 = MyRequests.post("/user/login", data=login_data_2)
            auth_sid_2 = self.get_cookie(response_5, "auth_sid")
            token_2 = self.get_header(response_5, "x-csrf-token")

        # GET USER 2 DATA
        with allure.step("Check user 2 still exists"):
            response_6 = MyRequests.get(
                f"/user/{user_id_2}",
                headers={"x-csrf-token": token_2},
                cookies={"auth_sid": auth_sid_2}
            )

        Assertions.assert_json_has_key(response_6, "id")
