from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions

class TestUserEdit(BaseCase):
    def test_edit_just_created_user(self):

        # REGISTER
        register_data = self.prepare_registration_data()
        response_1 = MyRequests.post('/user', data=register_data)

        Assertions.assert_code_status(response_1, 200)
        Assertions.assert_json_has_key(response_1, 'id')

        email = register_data['email']
        first_name = register_data['firstName']
        password = register_data['password']
        user_id = self.get_json_value(response_1, 'id')

        # LOGIN
        login_data = {
            'email': email,
            'password': password
        }
        response_2 = MyRequests.post('/user/login', data=login_data)

        auth_sid = self.get_cookie(response_2, 'auth_sid')
        token = self.get_header(response_2, 'x-csrf-token')

        # EDIT
        new_name = 'Changed Name'

        response_3 = MyRequests.put(
            f'/user/{user_id}',
            cookies={'auth_sid': auth_sid},
            headers={'x-csrf-token': token},
            data={'firstName': new_name}
        )

        Assertions.assert_code_status(response_3, 200)

        # GET
        response_4 = MyRequests.get(
            f'/user/{user_id}',
            cookies={'auth_sid': auth_sid},
            headers={'x-csrf-token': token}
        )

        Assertions.assert_json_value_by_name(
            response_4,
            'firstName',
            new_name,
            'Wrong name of the user after edit'
        )
