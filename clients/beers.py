from datetime import datetime
from flask import current_app as app
import requests
from beers.settings import Settings


class BeerClient:
    def __init__(self, api_url=None):
        self.api_url = api_url or Settings.FLASK_SERVER_NAME

    def list(self):
        url = 'http://{}/api/beers'.format(self.api_url)
        response = requests.get(url)

        if not response.status_code == 200:
            raise ValueError('Received not supported status code.')

        return response.json()

    def get(self, sku):
        if app.config['TESTING']:
            if sku == 'TESTING_SKU':
                beer = dict()
                beer['id'] = 1
                beer['name'] = 'Test beer'
                beer['sku'] = 'TESTING_SKU'
                beer['price'] = 2.5
                beer['image'] = None
                beer['time_created'] = datetime.utcnow()
                beer['time_modified'] = None
                return beer

            if sku == 'ANOTHER_TESTING_SKU':
                beer = dict()
                beer['id'] = 1
                beer['name'] = 'Another test beer'
                beer['sku'] = 'ANOTHER_TESTING_SKU'
                beer['price'] = 1.25
                beer['image'] = None
                beer['time_created'] = datetime.utcnow()
                beer['time_modified'] = None
                return beer

            return None

        url = 'http://{}/api/beers/{}'.format(self.api_url, sku)
        response = requests.get(url)

        if response.status_code == 404:
            return None

        if not response.status_code == 200:
            raise ValueError('Received not supported status code.')

        return response.json()

    def create(self, token, sku, name, price, image):
        headers = dict()
        headers['Authorization'] = token

        data = dict()
        data['name'] = name
        data['sku'] = sku
        data['price'] = price
        data['image'] = image

        url = 'http://{}/api/beers'.format(self.api_url)
        response = requests.post(url, data=data, headers=headers)

        if response.status_code == 400:
            return False, response.json()

        if response.status_code == 401:
            raise ValueError('You are not authorized to create beers.')

        if response.status_code == 201:
            return True, response.json()

        raise ValueError('Received not supported status code.')

    def modify(self, token, sku, name, price, image):
        url = 'http://{}/api/beers/{}'.format(self.api_url, sku)

        headers = dict()
        headers['Authorization'] = token

        data = dict()
        data['name'] = name
        data['price'] = price
        data['image'] = image

        response = requests.put(url, data=data, headers=headers)

        if response.status_code == 204:
            return response.json()

        if response.status_code == 401:
            raise ValueError('You are not authorized to update beers.')

        if response.status_code == 404:
            raise ValueError('Beer does not exists.')

        raise ValueError('Received not supported status code.')

    def delete(self, token, sku):
        url = 'http://{}/api/beers/{}'.format(self.api_url, sku)

        headers = dict()
        headers['Authorization'] = token

        response = requests.delete(url, headers=headers)

        if response.status_code == 204:
            return True

        if response.status_code == 401:
            raise ValueError('You are not authorized to delete beers.')

        if response.status_code == 404:
            raise ValueError('Beer does not exists.')

        raise ValueError('Received not supported status code.')
