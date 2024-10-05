import allure
import requests
from helpers import generate_random_string
from urls import url, register_new_courier, login_courier, delete_courier
from data import creating_courier_success, already_in_use, not_enough_data


class TestCreatingCourier:
    @allure.title('Успешное создание курьера')
    def test_creating_courier(self):
        login = generate_random_string(10)
        password = generate_random_string(10)
        first_name = generate_random_string(10)
        payload = {"login": login, "password": password, "firstName": first_name}

        response = requests.post(f"{url}{register_new_courier}", json=payload)

        assert response.status_code == 201
        assert response.text == creating_courier_success

        data = {"login": login, "password": password}
        response_login = requests.post(f"{url}{login_courier}", json=data)
        id_courier = response_login.json()['id']
        requests.delete(f"{url}{delete_courier}/{id_courier}")

    @allure.title('Создание двух одинаковых курьеров невозможно')
    def test_same_couriers_are_impossible(self, register_new_courier_return_login_password_delete_courier):
        login, password, first_name = register_new_courier_return_login_password_delete_courier
        payload = {"login": login, "password": password, "firstName": first_name}

        response = requests.post(f"{url}{register_new_courier}", json=payload)

        assert response.status_code == 409
        assert response.text == already_in_use

    @allure.title('Ошибка при создании курьера без логина')
    def test_creating_courier_without_login(self):
        password = generate_random_string(10)
        first_name = generate_random_string(10)
        payload = {"password": password, "firstName": first_name}

        response = requests.post(f"{url}{register_new_courier}", data=payload)

        assert response.status_code == 400
        assert response.text == not_enough_data

    @allure.title('Ошибка при создании курьера без пароля')
    def test_creating_courier_without_password(self):
        login = generate_random_string(10)
        first_name = generate_random_string(10)
        payload = {"login": login, "first_name": first_name}

        response = requests.post(f"{url}{register_new_courier}", data=payload)

        assert response.status_code == 400
        assert response.text == not_enough_data
