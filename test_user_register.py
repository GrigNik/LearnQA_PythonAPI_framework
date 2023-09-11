import pytest

from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions


class TestUserRegister(BaseCase):

    def test_create_user_successfully(self):
        data = self.prepare_registration_data()

        response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 200)
        Assertions.assert_json_has_key(response, "id")

    def test_create_user_with_existing_email(self):
        email='vinkotov@example.com'
        data = self.prepare_registration_data(email)
        response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response,400)
        assert response.content.decode("utf-8") == f"Users with email '{email}' already exists", f"Unexpected response content {response.content}"

    def test_create_user_with_incorrect_email(self):
        email = 'vinkotovexample.com'
        data = self.prepare_registration_data(email)
        response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == "Invalid email format", f"Unexpected response content {response.content}"

    exclude_params = [
        'username',
        'firstName',
        'lastName',
        'email',
        'password'
    ]
    @pytest.mark.parametrize("exclude_params", exclude_params)
    def test_create_user_without_parameter(self, exclude_params):
        data = self.prepare_registration_data()
        data.pop(exclude_params, None)
        response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode(
            "utf-8") == f"The following required params are missed: {exclude_params}", f"Unexpected response content {response.content}"

    def test_create_user_with_short_name(self):
        username = 'A'
        data = self.prepare_registration_data()
        data['username'] = username
        response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode(
            "utf-8") == "The value of 'username' field is too short", f"Unexpected response content {response.content}"

    def test_create_user_with_long_name(self):
        username = 'A'*251
        data = self.prepare_registration_data()
        data['username'] = username
        response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode(
            "utf-8") == "The value of 'username' field is too long", f"Unexpected response content {response.content}"
