from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User

from salt_observer.cherry import SaltCherrypyApi


class RestBackend(ModelBackend):
    ''' Authenticate against salt-api-permissions '''

    def authenticate(self, username=None, password=None):

        try:
            valid = SaltCherrypyApi.obtain_auth_token(username, password)
        except:
            valid = False

        if valid:
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                user = User.objects.create_user(username=username, email='', password=password)

            return user
        return None
