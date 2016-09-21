from django.conf import settings

import requests
from getpass import getpass


class AbstractApi(object):
    '''
        Defines an abstract api to inherit from.
        You MUST specify a BASE_URL for your api to build a proper request url.
    '''

    BASE_URL = ''

    def __init__(self, username='', password='', token=''):
        ''' Set a token to work with '''
        if not self.BASE_URL:
            raise NotImplementedError('Please provide an BASE_URL')

        if token:
            self.token = token
        else:
            self.token = self.obtain_auth_token(username, password)

    def request(self, method='get', resource='/', headers={}, data={}, set_token_header=True):
        if set_token_header:
            headers.update({'X-Auth-Token': self.token})

        return getattr(requests, method)(
            self.BASE_URL + resource,
            headers=headers,
            data=data
        )

    def obtain_auth_token(self, username, password):
        res = self.request('post', '/login', headers={'Accept': 'application/json'}, data={
            'username': username,
            'password': password,
            'eauth': 'pam'
        }, set_token_header=False)

        if res.status_code != 200:
            raise Exception('{} - {}'.format(res.status_code, res.text))

        return res.json().get('return')[0].get('token')


class SaltCherrypy(AbstractApi):

    BASE_URL = '{protocol}://{host}:{port}'.format(**settings.SALT['api']['cherrypy'])

    def logout(self):
        return self.request('post', '/logout', headers={'Accept': 'application/json'})

    def get(self, module, target='*', api_args=[], api_kwargs={}):
        return self.request(
            'post',
            data={
                'client': 'local',
                'fun': module,
                'tgt': target,
                'arg': api_args,
                'kwarg': api_kwargs
            },
            headers={
                'Accept': 'application/json',
            }
        ).json().get('return')[0]


class SaltTornado(AbstractApi):

    BASE_URL = '{protocol}://{host}:{port}'.format(**settings.SALT['api']['tornado'])
