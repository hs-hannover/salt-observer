from salt_observer.saltapis import SaltCherrypy

from getpass import getpass


class ApiCommand(object):

    def add_arguments(self, parser):
        parser.add_argument('username', nargs='?', type=str)
        parser.add_argument('password', nargs='?', type=str)

    def handle(self, *args, **kwargs):
        if not kwargs.get('username'):
            username = input('Username: ')
        else:
            username = kwargs.get('username')

        if not kwargs.get('password'):
            password = getpass()
        else:
            password = kwargs.get('password')

        return SaltCherrypy(username, password)
