import allure
import requests
from helpers import url, generate_random_string


class TestCreatingCourier:
    @allure.title('Успешное создание курьера')
    def test_creating_courier(self):
        login = generate_random_string(10)
        password = generate_random_string(10)
        first_name = generate_random_string(10)
        payload = {"login": login, "password": password, "firstName": first_name}

        response = requests.post(f"{url}/api/v1/courier", json=payload)

        assert response.status_code == 201
        assert response.text == '{"ok":true}'

        data = {"login": login, "password": password}
        response_login = requests.post(f"{url}/api/v1/courier/login", json=data)
        id_courier = response_login.json()['id']
        requests.delete(f"{url}/api/v1/courier/{id_courier}")

    @allure.title('Создание двух одинаковых курьеров невозможно')
    def test_same_couriers_are_impossible(self, register_new_courier_return_login_password_delete_courier):
        login, password, first_name = register_new_courier_return_login_password_delete_courier
        payload = {"login": login, "password": password, "firstName": first_name}

        response = requests.post(f"{url}/api/v1/courier", json=payload)

        assert response.status_code == 409
        assert response.text == '{"code":409,"message":"Этот логин уже используется. Попробуйте другой."}'

    @allure.title('Ошибка при создании курьера без логина')
    def test_creating_courier_without_login(self):
        password = generate_random_string(10)
        first_name = generate_random_string(10)
        payload = {"password": password, "firstName": first_name}

        response = requests.post(f"{url}/api/v1/courier", data=payload)

        assert response.status_code == 400
        assert response.text == '{"code":400,"message":"Недостаточно данных для создания учетной записи"}'

    @allure.title('Ошибка при создании курьера без пароля')
    def test_creating_courier_without_password(self):
        login = generate_random_string(10)
        first_name = generate_random_string(10)
        payload = {"login": login, "first_name": first_name}

        response = requests.post(f"{url}/api/v1/courier", data=payload)

        assert response.status_code == 400
        assert response.text == '{"code":400,"message":"Недостаточно данных для создания учетной записи"}'
