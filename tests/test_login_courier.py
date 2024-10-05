import pytest
import allure
import requests
from urls import url, login_courier
from helpers import generate_random_string


class TestLoginCourier:
    @allure.title('Курьер успешно залогинен')
    def test_login_courier(self, register_new_courier_return_login_password_delete_courier):
        login, password, _ = register_new_courier_return_login_password_delete_courier
        data = {"login": login, "password": password}

        response = requests.post(f"{url}{login_courier}", json=data)
        id_courier = response.json()['id']

        assert response.status_code == 200
        assert response.json() == {"id": id_courier}

    @allure.title('Ошибка при логине курьера без логина')
    def test_login_courier_without_login(self, register_new_courier_return_login_password_delete_courier):
        _, password, _ = register_new_courier_return_login_password_delete_courier
        data = {"password": password}

        response = requests.post(f"{url}{login_courier}", json=data)

        assert response.status_code == 400
        assert response.json() == {'code': 400, 'message': 'Недостаточно данных для входа'}

    @pytest.mark.xfailed
    @allure.title('Ошибка при логине курьера без пароля')
    def test_login_courier_without_password(self, register_new_courier_return_login_password_delete_courier):
        login, _, _ = register_new_courier_return_login_password_delete_courier
        data = {"login": login}

        response = requests.post(f"{url}{login_courier}", json=data)

        assert response.status_code == 400
        assert response.json() == {'code': 400, 'message': 'Недостаточно данных для входа'}

    @allure.title('Ошибка при авторизации несуществующего курьера')
    def test_login_courier_incorrect_login_password(self, register_new_courier_return_login_password_delete_courier):
        log = generate_random_string(10)
        pas = generate_random_string(10)
        data = {"login": log, "password": pas}

        response = requests.post(f"{url}{login_courier}", json=data)

        assert response.status_code == 404
        assert response.json() == {'code': 404, 'message': 'Учетная запись не найдена'}
