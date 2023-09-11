from lib.my_requests import MyRequests
from lib.assertions import Assertions
from lib.base_case import BaseCase

class TestUserEdit(BaseCase):
    def test_edit_just_created_user(self):
        # REGISTER USER1
        register_data = self.prepare_registration_data()
        response1 = MyRequests.post("/user/", data=register_data)

        Assertions.assert_code_status(response1,200)
        Assertions.assert_json_has_key(response1,"id")

        email1 = register_data['email']
        first_name1 = register_data['firstName']
        password1 = register_data['password']
        user_id1 = self.get_json_value(response1,"id")

        # пытаемся изменить данные пользователя, будучи неавторизованными

        new_name = "Changed Name"

        response2 = MyRequests.put(
            f"/user/{user_id1}",
            cookies={"auth_sid": None},
            headers={"x-csrf-token": None},
            data={"firstName": new_name}
        )

        Assertions.assert_code_status(response2, 400)
        assert response2.text == f"Auth token not supplied", f"Unexpected response text! Expected:Auth token not supplied. Actual: {response2.text}"

        # REGISTER USER2
        register_data = self.prepare_registration_data()
        response3 = MyRequests.post("/user/", data=register_data)

        Assertions.assert_code_status(response3, 200)
        Assertions.assert_json_has_key(response3, "id")

        email2 = register_data['email']
        first_name2 = register_data['firstName']
        password2 = register_data['password']
        user_id2 = self.get_json_value(response3, "id")

        # LOGIN USER1
        login_data = {
            'email': email1,
            'password': password1
        }
        response4 = MyRequests.post("/user/login",data = login_data)

        auth_sid1 = self.get_cookie(response4,"auth_sid")
        token1 = self.get_header(response4, "x-csrf-token")

        # пытаемся изменить данные пользователя 2, будучи авторизованными под пользователем 1

        new_name = "Changed Name"

        response5 = MyRequests.put(
            f"/user/{user_id2}",
            cookies={"auth_sid": auth_sid1},
            headers={"x-csrf-token": token1},
            data={"firstName": new_name}
        )

        Assertions.assert_code_status(response5, 200)
        #assert response5.text == f"Auth token not supplied", f"Unexpected response text! Expected:Auth token not supplied. Actual: {response2.text}"

        # LOGIN USER2
        login_data = {
            'email': email2,
            'password': password2
        }
        response6 = MyRequests.post("/user/login",data = login_data)

        auth_sid2 = self.get_cookie(response6,"auth_sid")
        token2 = self.get_header(response6, "x-csrf-token")

        # проверяем что пользователь 1 не смог изменить данные пользователя 2

        response7 = MyRequests.get(
            f"/user/{user_id2}",
            cookies={"auth_sid": auth_sid2},
            headers={"x-csrf-token": token2},
        )

        Assertions.assert_json_value_by_name(response7,"firstName", first_name2, "Пользователь 1 смог изменить имя пользователя 2" )

    def test_edit_email_without_dog(self):
        # REGISTER USER
        register_data = self.prepare_registration_data()
        response1 = MyRequests.post("/user/", data=register_data)

        Assertions.assert_code_status(response1,200)
        Assertions.assert_json_has_key(response1,"id")

        email = register_data['email']
        first_name = register_data['firstName']
        password = register_data['password']
        user_id = self.get_json_value(response1,"id")

        # LOGIN USER
        login_data = {
            'email': email,
            'password': password
        }
        response2 = MyRequests.post("/user/login",data = login_data)

        auth_sid = self.get_cookie(response2,"auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        # пытаемся изменить email пользователя, будучи авторизованными тем же пользователем, на новый email без символа @

        new_email = email.replace('@','')

        response3 = MyRequests.put(
            f"/user/{user_id}",
            cookies={"auth_sid": auth_sid},
            headers={"x-csrf-token": token},
            data={"email": new_email}
        )

        Assertions.assert_code_status(response3, 400)
        assert response3.text == f"Invalid email format", f"Unexpected response text! Expected:Invalid email format. Actual: {response3.text}"

    def test_edit_short_firstName(self):
        # REGISTER USER
        register_data = self.prepare_registration_data()
        response1 = MyRequests.post("/user/", data=register_data)

        Assertions.assert_code_status(response1,200)
        Assertions.assert_json_has_key(response1,"id")

        email = register_data['email']
        first_name = register_data['firstName']
        password = register_data['password']
        user_id = self.get_json_value(response1,"id")

        # LOGIN USER
        login_data = {
            'email': email,
            'password': password
        }
        response2 = MyRequests.post("/user/login",data = login_data)

        auth_sid = self.get_cookie(response2,"auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        # пытаемся изменить firstName пользователя, будучи авторизованными тем же пользователем, на очень короткое значение в один символ
        new_name = "A"

        response3 = MyRequests.put(
            f"/user/{user_id}",
            cookies={"auth_sid": auth_sid},
            headers={"x-csrf-token": token},
            data={"firstName": new_name}
        )

        Assertions.assert_code_status(response3, 400)
        Assertions.assert_json_value_by_name (response3,"error","Too short value for field firstName", f"Unexpected response text! Expected:Too short value for field firstName. Actual: {response3.text}")






