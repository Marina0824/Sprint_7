import allure
import requests
from urls import url, get_list_of_order


class TestListOfOrders:
    @allure.title('Получение списка заказов')
    def test_get_list_of_orders(self):
        response = requests.get(f"{url}{get_list_of_order}")
        orders = response.json()

        assert response.status_code == 200
        assert type(orders) == dict
