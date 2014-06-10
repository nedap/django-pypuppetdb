"""
If you want to use pypuppetdb in Django you will have to tell Django
that the backend uses django_pypuppetdb. See the example below.

The first time a user logs-in it will create a tastypie api key for the user.

AUTHENTICATION_BACKENDS = (
    'django_pypuppetdb.tastypie_authentication.PuppetDBAuthentication',
)
"""
import logging

from django.conf import settings
from django.contrib.auth.models import User
from django_pypuppetdb.user_authentication import UserAuthentication
from tastypie.models import create_api_key


logger = logging.getLogger(__name__)


class PuppetDBAuthentication(object):
    def authenticate(self, username=None, password=None):
        puppet_user = UserAuthentication.check_user(username)

        if puppet_user is False:
            logger.error('Connection Failed')
            return None

        if puppet_user is None:
            logger.error('Nothing is return from puppetdb')
            return None

        if puppet_user and \
                UserAuthentication.verify_password(puppet_user, password):
            new_user, created = User.objects.get_or_create(username=username)
            user_groups = puppet_user.parameters['groups']
            create_api_key(self, instance=new_user, created=created)

            if settings.PUPPETDB_ADMIN_GROUP in user_groups:
                new_user.is_staff = 1
                new_user.is_superuser = 1
                new_user.save()

            return new_user

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
