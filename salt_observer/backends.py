from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User

from salt_observer.saltapis import SaltCherrypy, SaltTornado


class RestBackend(ModelBackend):
    ''' Authenticate against salt-api-permissions '''

    def authenticate(self, username=None, password=None, request=None):

        try:
            cherrypy_token = SaltCherrypy(username, password).token
            tornado_token = SaltTornado(username, password).token
        except Exception as e:
            cherrypy_token = False
            tornado_token = False

        if cherrypy_token and tornado_token:
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                user = User.objects.create_user(username=username, email='', password=password)

            request.session['salt_cherrypy_token'] = cherrypy_token
            request.session['salt_tornado_token'] = tornado_token

            return user
        return None
