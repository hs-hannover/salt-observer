import requests

#from salt_observer.models import Minion

BASE_URL = 'localhost:8888'


def obtain_auth_token(username, password):
    return requests.post(BASE_URL+'/login', headers={'Accept': 'application/json'}, data={
        'username': username,
        'password': password,
        'eauth': 'pam'
    }).json().get('return')[0].get('token')


def request(token, data):
    data.update({'client': 'local'})
    return requests.post(BASE_URL, headers={'Accept': 'application/json', 'X-Auth-Token': token}, data=data)
