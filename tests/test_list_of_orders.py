import allure
import requests
from helpers import url


class TestListOfOrders:
    @allure.title('Получение списка заказов')
    def test_get_list_of_orders(self):
        response = requests.get(f"{url}/api/v1/orders")
        orders = response.json()

        assert response.status_code == 200
        assert type(orders) == dict
