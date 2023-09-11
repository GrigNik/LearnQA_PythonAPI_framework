from lib.my_requests import MyRequests
from lib.assertions import Assertions
from lib.base_case import BaseCase


class TestUserDelete(BaseCase):

    def test_delete_user_id_2(self):
        # LOGIN USER
        login_data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }
        response1 = MyRequests.post("/user/login", data=login_data)

        auth_sid = self.get_cookie(response1, "auth_sid")
        token = self.get_header(response1, "x-csrf-token")

        # Первый - на попытку удалить пользователя по ID 2

        response2 = MyRequests.delete(
            f"/user/2",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
        )

        Assertions.assert_code_status(response2, 400)
        assert response2.text == f"Please, do not delete test users with ID 1, 2, 3, 4 or 5.",\
        f"Unexpected response text! Expected:Auth token not supplied. Actual: {response2.text}"

        response3 = MyRequests.get(
            f"/user/2",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )

        Assertions.assert_code_status(response3, 200)


    def test_delete_user(self):
        # REGISTER USER
        register_data = self.prepare_registration_data()
        response = MyRequests.post("/user/", data=register_data)

        Assertions.assert_code_status(response, 200)
        Assertions.assert_json_has_key(response, "id")

        email = register_data['email']
        first_name = register_data['firstName']
        password = register_data['password']
        user_id = self.get_json_value(response, "id")

        # LOGIN USER
        login_data = {
            'email': email,
            'password': password
        }
        response1 = MyRequests.post("/user/login", data=login_data)

        auth_sid = self.get_cookie(response1, "auth_sid")
        token = self.get_header(response1, "x-csrf-token")

        # удаление пользователя

        response2 = MyRequests.delete(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
        )

        Assertions.assert_code_status(response2, 200)

        # проверка, что пользователя не существует

        response3 = MyRequests.get(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )

        Assertions.assert_code_status(response3, 404)

    def test_delete_user_by_another_user(self):
        # REGISTER FOR USER1
        register_data1 = self.prepare_registration_data()
        response1 = MyRequests.post(
            "/user/",
            data=register_data1
        )

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        email1 = register_data1["email"]
        first_name1 = register_data1["firstName"]
        password1 = register_data1["password"]
        user_id1 = self.get_json_value(response1, "id")

        # REGISTER FOR USER2
        register_data2 = self.prepare_registration_data()
        response2 = MyRequests.post(
            "/user/",
            data=register_data2
        )

        Assertions.assert_code_status(response2, 200)
        Assertions.assert_json_has_key(response2, "id")

        email2 = register_data2["email"]
        first_name2 = register_data2["firstName"]
        password2 = register_data2["password"]
        user_id2 = self.get_json_value(response2, "id")

        # LOGIN BY USER2
        login_data = {
            "email": email2,
            "password": password2
        }

        response3 = MyRequests.post(
            "/user/login",
            data=login_data
        )

        auth_sid2 = self.get_cookie(response3, "auth_sid")
        token2 = self.get_header(response3, "x-csrf-token")

        # проверка удаления пользователя 1 другим пользователем

        response4 = MyRequests.delete(
            f"/user/{user_id1}",
            headers={"x-csrf-token": auth_sid2},
            cookies={"auth_sid": token2}
        )
        Assertions.assert_code_status(response4, 400)
        assert response4.text == f"Auth token not supplied", \
            f"Unexpected response text! Expected:Auth token not supplied. Actual: {response4.text}"

        # вход пользователя 1, проверка, что не удален
        login_data = {
            "email": email1,
            "password": password1
        }

        response5 = MyRequests.post(
            "/user/login",
            data=login_data
        )
        Assertions.assert_code_status(response5, 200)
        Assertions.assert_json_has_key(response5, "user_id")

