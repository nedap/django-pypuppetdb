"""
If you want to use pypuppetdb in Django you will have to tell Django
that the backend uses django_pypuppetdb. See the example below.

If you have tastypie installed the first time a user logs-in
it will make a unique api key for the user.

AUTHENTICATION_BACKENDS = (
    'django_pypuppetdb.django.PuppetDbAuthentication',
)
"""
import logging

from django.contrib.auth.models import User
from .user_authentication import UserAuthentication


logger = logging.getLogger(__name__)


class PuppetDbAuthentication(object):
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

            try:
                from tastypie.models import create_api_key
                create_api_key(self, instance=user, created=created)
            except ImportError:
                # Install tastypie to auto create a new api key for every new
                # user that connects with his username and password from
                # puppetdb.
                pass

            return user

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None