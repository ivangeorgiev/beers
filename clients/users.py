import requests
from users.settings import Settings


class UserClient:
    def __init__(self, api_url=None):
        self.api_url = api_url or Settings.FLASK_SERVER_NAME

    def login(self, username, password):
        url = 'http://{}/api/users/login'.format(self.api_url)
        response = requests.post(url, data=dict(username=username, password=password))

        if not response.status_code == 200:
            raise ValueError('Received not supported status code.')

        token = response.json()['token']

        if token is None:
            return False

        return token

    def logout(self, token):
        url = 'http://{}/api/users/logout'.format(self.api_url)
        response = requests.post(url, data=dict(token=token))
        if response.status_code == 200:
            return True

        if response.status_code == 404:
            return False

        raise ValueError('Received not supported status code.')

    def check_token(self, token):
        url = 'http://{}/api/users/check_token'.format(self.api_url)
        response = requests.post(url, data=dict(token=token))

        if response.status_code == 200:
            return response.json()

        if response.status_code == 404:
            return False

        raise ValueError('Received not supported status code.')

    def exists(self, username):
        url = 'http://{}/api/users/exists'.format(self.api_url)
        response = requests.get(url, params=dict(username=username))

        if response.status_code == 200:
            return True

        if response.status_code == 404:
            return False

        raise ValueError('Received not supported status code.')

    def register(self, username, mail, first_name, last_name, password):
        url = 'http://{}/api/users/register'.format(self.api_url)

        data = {
            'username':   username,
            'mail':       mail,
            'first_name': first_name,
            'last_name':  last_name,
            'password':   password
        }

        response = requests.post(url, data=data)

        if response.status_code == 400:
            return False, response.json()

        if response.status_code == 200:
            return True, response.json()

        raise ValueError('Received not supported status code.')
