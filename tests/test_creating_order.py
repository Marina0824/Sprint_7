import pytest
import allure
import requests
from helpers import url


class TestCreatingOrder:
    @allure.title('Создание заказа с различными цветами самоката')
    @pytest.mark.parametrize('color', [["BLACK"], ["GRAY"], ["BLACK", "GRAY"], []])
    def test_creating_order(self, color):
        body = {"firstName": "anna",
                "lastName": "alla",
                "address": "Moscow, Red Square",
                "metroStation": 1,
                "phone": "86586095432",
                "rentTime": 2,
                "deliveryDate": "2025-12-31",
                "comment": "Drive!",
                "color": color}

        response = requests.post(f"{url}/api/v1/orders", json=body)

        assert response.status_code == 201
        assert "track" in response.json()
