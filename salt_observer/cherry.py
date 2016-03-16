import requests
from getpass import getpass


class SaltCherrypyApi(object):

    BASE_URL = 'http://localhost:8989'

    def __init__(self, username, password):
        ''' Log in every time an instance is created '''
        self.token = self.obtain_auth_token(username, password)

    def obtain_auth_token(self, username, password):
        return requests.post(self.BASE_URL+'/login', headers={'Accept': 'application/json'}, data={
            'username': username,
            'password': password,
            'eauth': 'pam'
        }).json().get('return')[0].get('token')

    def request(self, data, api_point=''):
        data.update({'client': 'local'})
        return requests.post('{}/{}'.format(self.BASE_URL, api_point), headers={'Accept': 'application/json', 'X-Auth-Token': self.token}, data=data)

    def logout(self):
        return requests.post(self.BASE_URL+'/logout', headers={'Accept': 'application/json', 'X-Auth-Token': self.token})

    def get_server_information(self):
        return self.request({'tgt': '*', 'fun': 'grains.items'}).json().get('return')[0]


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
