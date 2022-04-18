from requests import Response
import json


class Assertions:
    @staticmethod
    def assert_json_value_by_name(response: Response, name, expected_value, error_message):
        # Проверка формата
        try:
            response_as_dict = response.json()
        except json.JSONDecodeError:
            assert False, f'Response is not in JSON format. Response text is "{response.text}"'

        # Проверка ключа
        assert name in response_as_dict, f'Response JSON doesn\'t have key "{name}"'
        # Проверка значения
        assert response_as_dict[name] == expected_value, error_message
