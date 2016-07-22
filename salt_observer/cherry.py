from django.conf import settings

import requests
from getpass import getpass


class SaltCherrypyApi(object):

    BASE_URL = '{protocol}://{host}:{port}'.format(**settings.SALT_API)

    def __init__(self, username, password):
        ''' Log in every time an instance is created '''
        self.token = self.obtain_auth_token(username, password)

    @classmethod
    def obtain_auth_token(cls, username, password):
        res = requests.post(cls.BASE_URL+'/login', headers={'Accept': 'application/json'}, data={
            'username': username,
            'password': password,
            'eauth': 'pam'
        })

        if res.status_code != 200:
            raise Exception('{} - {}'.format(res.status_code, res.text))

        return res.json().get('return')[0].get('token')

    def request(self, data, api_point=''):
        data.update({'client': 'local'})
        return requests.post(
            '{}/{}'.format(self.BASE_URL, api_point),
            headers={
                'Accept': 'application/json',
                'X-Auth-Token': self.token
            },
            data=data
        )

    def logout(self):
        return requests.post(
            self.BASE_URL+'/logout',
            headers={
                'Accept': 'application/json',
                'X-Auth-Token': self.token
            }
        )

    def get(self, module, target='*', api_args=[], api_kwargs={}):
        return self.request({
            'fun': module,
            'tgt': target,
            'arg': api_args,
            'kwarg': api_kwargs
        }).json().get('return')[0]


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
