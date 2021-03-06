import allure
from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions


@allure.epic("User edition cases")
class TestUserEdit(BaseCase):
    new_name = 'Changed Name'

    @allure.description("This test checks authorized user can edit his registration data")
    def test_edit_just_created_user(self):

        # REGISTER USER 1
        with allure.step("Register user 1"):
            response_register_1, registration_data_1 = self.generate_new_user()

        Assertions.assert_code_status(response_register_1, 200)
        Assertions.assert_json_has_key(response_register_1, 'id')

        email_1 = registration_data_1['email']
        password_1 = registration_data_1['password']
        user_id_1 = self.get_json_value(response_register_1, 'id')

        # LOGIN AS USER 1
        login_data = {
            'email': email_1,
            'password': password_1
        }
        with allure.step("Authorize as user 1"):
            response_login_1 = MyRequests.post('/user/login', data=login_data)

            token_1 = self.get_header(response_login_1, 'x-csrf-token')
            auth_sid_1 = self.get_cookie(response_login_1, 'auth_sid')

        # EDIT USER 1
        with allure.step(f"Try to change user's first name to '{self.new_name}'"):
            response_edit_1 = MyRequests.put(
                f'/user/{user_id_1}',
                headers={'x-csrf-token': token_1},
                cookies={'auth_sid': auth_sid_1},
                data={'firstName': self.new_name}
            )

        Assertions.assert_code_status(response_edit_1, 200)

        # GET USER 1
        with allure.step("Get authorized user's new data"):
            response_get_1 = MyRequests.get(
                f'/user/{user_id_1}',
                cookies={'auth_sid': auth_sid_1},
                headers={'x-csrf-token': token_1}
            )

        Assertions.assert_json_value_by_name(
            response_get_1,
            'firstName',
            self.new_name,
            'Wrong name of the user after edit'
        )

    @allure.description("This test checks unsuccessful user edition w/o sending auth cookies and token")
    def test_edit_not_auth_user(self):

        # EDIT USER 1
        with allure.step(f"Try to edit first name of user with id=2 to '{self.new_name}'"):
            response_edit_1 = MyRequests.put(
                "/user/2",
                data={"firstName": self.new_name}
            )

        Assertions.assert_code_status(response_edit_1, 400)
        Assertions.assert_expected_response_content(response_edit_1, "Auth token not supplied")

    @allure.description("This test checks unsuccessful user edition using another user auth data")
    def test_edit_user_auth_as_another_user(self):

        # REGISTER USER 2
        with allure.step("Register user 2"):
            response_register_2, registration_data_2 = self.generate_new_user()

        Assertions.assert_code_status(response_register_2, 200)
        Assertions.assert_json_has_key(response_register_2, "id")

        email_2 = registration_data_2['email']
        password_2 = registration_data_2['password']

        # REGISTER USER 3
        with allure.step("Register user 3"):
            response_register_3, registration_data_3 = self.generate_new_user()

        Assertions.assert_code_status(response_register_3, 200)
        Assertions.assert_json_has_key(response_register_3, "id")

        email_3 = registration_data_3['email']
        password_3 = registration_data_3['password']
        first_name_3 = registration_data_3['firstName']
        user_id_3 = self.get_json_value(response_register_3, "id")

        # LOGIN AS USER 2
        login_data_2 = {
            'email': email_2,
            'password': password_2
        }
        with allure.step("Authorize as user 2"):
            response_8 = MyRequests.post("/user/login", data=login_data_2)

            token_2 = self.get_header(response_8, "x-csrf-token")
            auth_sid_2 = self.get_cookie(response_8, "auth_sid")

        # EDIT USER 3 DATA
        with allure.step(f"Try to edit first name of user 3 to '{self.new_name}' being auth as user 2"):
            response_edit_3 = MyRequests.put(
                f"/user/{user_id_3}",
                headers={"x-csrf-token": token_2},
                cookies={"auth_sid": auth_sid_2},
                data={"firstName": self.new_name}
            )

        Assertions.assert_code_status(response_edit_3, 200)

        # LOGIN AS USER 3
        login_data_3 = {
            'email': email_3,
            'password': password_3
        }
        with allure.step("Authorize as user 3"):
            response_login_3 = MyRequests.post("/user/login", data=login_data_3)

            token_3 = self.get_header(response_login_3, "x-csrf-token")
            auth_sid_3 = self.get_cookie(response_login_3, "auth_sid")

        # GET USER 3 DATA
        with allure.step("Get user 3 data"):
            response_get_3 = MyRequests.get(
                f"/user/{user_id_3}",
                headers={"x-csrf-token": token_3},
                cookies={"auth_sid": auth_sid_3}
            )

        Assertions.assert_json_value_by_name(
            response_get_3,
            "firstName",
            first_name_3,
            f"Name of the user was edited by another user!"
        )

    @allure.description("This test checks unsuccessful user edition using email with incorrect format")
    def test_edit_user_email_with_incorrect_address(self):

        # REGISTER USER 4
        with allure.step("Register user 4"):
            response_register_4, registration_data_4 = self.generate_new_user()

        Assertions.assert_code_status(response_register_4, 200)
        Assertions.assert_json_has_key(response_register_4, "id")

        email_4 = registration_data_4['email']
        password_4 = registration_data_4['password']
        user_id_4 = self.get_json_value(response_register_4, "id")

        # LOGIN AS USER 4
        login_data = {
            'email': email_4,
            'password': password_4
        }
        with allure.step("Authorize as user 4"):
            response_login_4 = MyRequests.post("/user/login", data=login_data)

            token_4 = self.get_header(response_login_4, "x-csrf-token")
            auth_sid_4 = self.get_cookie(response_login_4, "auth_sid")

        # EDIT USER 4
        new_email = "incorrect_email.com"

        with allure.step("Try to edit user's email using incorrect email"):
            response_edit_4 = MyRequests.put(
                f"/user/{user_id_4}",
                headers={"x-csrf-token": token_4},
                cookies={"auth_sid": auth_sid_4},
                data={"email": new_email}
            )

        Assertions.assert_code_status(response_edit_4, 400)
        Assertions.assert_expected_response_content(response_edit_4, "Invalid email format")

    @allure.description("This test checks unsuccessful user edition using too short name")
    def test_edit_user_first_name_with_too_short_example(self):

        # REGISTER USER 5
        with allure.step("Register user 5"):
            response_register_5, registration_data_5 = self.generate_new_user()

        Assertions.assert_code_status(response_register_5, 200)
        Assertions.assert_json_has_key(response_register_5, "id")

        email_5 = registration_data_5['email']
        password_6 = registration_data_5['password']
        user_id_6 = self.get_json_value(response_register_5, "id")

        # LOGIN AS USER 5
        login_data = {
            'email': email_5,
            'password': password_6
        }
        with allure.step("Authorize as user 5"):
            response_login_5 = MyRequests.post("/user/login", data=login_data)

            auth_sid = self.get_cookie(response_login_5, "auth_sid")
            token = self.get_header(response_login_5, "x-csrf-token")

        # EDIT USER 5
        new_name = "a"

        with allure.step("Try to edit user using too short name"):
            response_edit_5 = MyRequests.put(
                f"/user/{user_id_6}",
                headers={"x-csrf-token": token},
                cookies={"auth_sid": auth_sid},
                data={"firstName": new_name}
            )

        Assertions.assert_code_status(response_edit_5, 400)
        Assertions.assert_json_has_key(response_edit_5, "error")
        Assertions.assert_json_value_by_name(
            response_edit_5,
            "error",
            "Too short value for field firstName",
            "Unexpected error message!"
        )
