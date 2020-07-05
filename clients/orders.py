import requests
from orders.settings import Settings


class OrderClient:
    def __init__(self, api_url=None):
        self.api_url = api_url or Settings.FLASK_SERVER_NAME

    def list(self, token):
        headers = dict()
        headers['Authorization'] = token

        url = 'http://{}/api/orders'.format(self.api_url)
        response = requests.get(url, headers=headers)

        if response.status_code == 401:
            raise ValueError('You are not authorized to see orders.')

        if not response.status_code == 200:
            raise ValueError('Received not supported status code.')

        return response.json()

    def current(self, token):
        headers = dict()
        headers['Authorization'] = token

        url = 'http://{}/api/orders/current'.format(self.api_url)
        response = requests.get(url, headers=headers)

        if response.status_code == 401:
            raise ValueError('You are not authorized to see orders.')

        if not response.status_code == 200:
            raise ValueError('Received not supported status code.')

        return response.json()

    def add_beer(self, token, sku, quantity):
        headers = dict()
        headers['Authorization'] = token

        data = dict()
        data['sku'] = sku
        data['quantity'] = quantity

        url = 'http://{}/api/orders/current'.format(self.api_url)
        response = requests.put(url, headers=headers, data=data)

        if response.status_code == 200:
            return True, response.json()

        if response.status_code == 400:
            return False, response.json()

        if response.status_code == 401:
            raise ValueError('You are not authorized to add beers.')

        raise ValueError('Received not supported status code.')

    def remove_beer(self, token, sku):
        headers = dict()
        headers['Authorization'] = token

        data = dict()
        data['sku'] = sku

        url = 'http://{}/api/orders/current'.format(self.api_url)
        response = requests.delete(url, headers=headers, data=data)

        if response.status_code == 200:
            return True, response.json()

        if response.status_code == 400:
            return False, response.json()

        if response.status_code == 401:
            raise ValueError('You are not authorized to remove beers.')

        raise ValueError('Received not supported status code.')

    def checkout(self, token):
        headers = dict()
        headers['Authorization'] = token

        url = 'http://{}/api/orders/checkout'.format(self.api_url)
        response = requests.delete(url, headers=headers)

        if response.status_code == 200:
            return True

        raise ValueError('Received not supported status code.')

    def details(self, token, id):
        headers = dict()
        headers['Authorization'] = token

        url = 'http://{}/api/orders/{}'.format(self.api_url, id)
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            return response.json()

        raise ValueError('Received not supported status code.')
