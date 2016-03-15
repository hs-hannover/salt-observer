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


# experimental:
# ---
#
# get output of 'w' command of all 'tgt' minions
# request('token', {'tgt': '*', 'fun': 'cmd.run', 'arg': 'w'})
#
# get all grains of 'tgt' minions
# request('token', {'tgt': '*', 'fun': 'grains.items'})
#
# execute some state and apply custom pillars to it
# request('token', {'tgt': '*', 'fun': 'state.sls', 'kwarg': {
#     'mods': 'name_of_state', 'pillar': {'some': 'pillar_data'}
# }})
