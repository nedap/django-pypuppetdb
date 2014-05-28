"""
If you want to use pypuppetdb in Django you will have to tell Django
that the backend uses django_pypuppetdb. See the example below.

AUTHENTICATION_BACKENDS = (
    'django_pypuppetdb.django.DjangoPuppetDBAuthentication',
)
"""
import logging

from django.contrib.auth.models import User
from django_pypuppetdb.user_authentication import UserAuthentication


logger = logging.getLogger(__name__)


class PuppetDBAuthentication(object):
    def authenticate(self, username=None, password=None):
        user = UserAuthentication.check_user(username)

        if user is False:
            logger.error('Connection Failed')
            return None

        if user is None:
            logger.error('Nothing is return from puppetdb')
            return None

        if user and UserAuthentication.verify_password(user, password):
            user, created = User.objects.get_or_create(username=username)
            return user

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
