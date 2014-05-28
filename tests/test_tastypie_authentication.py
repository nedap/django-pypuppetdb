from django.conf import settings
from django.contrib.auth.models import User
from django.test import TestCase
from django.test.runner import setup_databases
from mock import patch
from django_pypuppetdb.django_authentication \
    import DjangoPuppetDBAuthentication

try:
    import tastypie

    # Only create a database once
    setup_databases(1, 1)

    class TestTastypieAuthentication(TestCase):
        def setUp(self):
            self.user = User.objects.create(
                username='test', email='test@nedap.com')
            self.auth = DjangoPuppetDBAuthentication()

        def test_authenticate_without_user(self):
            self.assertIsNone(self.auth.authenticate())

        @patch('django_pypuppetdb.user_authentication.UserAuthentication.'
               'check_user')
        @patch('django_pypuppetdb.user_authentication.UserAuthentication.'
               'verify_password')
        def test_authenticate_incorrect_password(
                self, puppetdb_user, verify_password):
            puppetdb_user.return_value = None
            verify_password.return_value = True
            self.assertIsNone(self.auth.authenticate('test'))

        @patch('django_pypuppetdb.user_authentication.UserAuthentication.'
               'check_user')
        @patch('django_pypuppetdb.user_authentication.UserAuthentication.'
               'verify_password')
        def test_authenticate_with_existing_user(
                self, puppetdb_user, verify_password):
            puppetdb_user.return_value = 'test'
            verify_password.return_value = True
            user = self.auth.authenticate('test', 'password')
            self.assertIsInstance(user, User)
            self.assertEqual(user.username, 'test')

        @patch('django_pypuppetdb.user_authentication.UserAuthentication.'
               'check_user')
        @patch('django_pypuppetdb.user_authentication.UserAuthentication.'
               'verify_password')
        def test_authenticate_with_new_user(
                self, puppetdb_user, verify_password):
            puppetdb_user.return_value = 'new user'
            verify_password.return_value = True
            user = self.auth.authenticate('new user', 'password')
            self.assertIsInstance(user, User)
            self.assertEqual(user.username, 'new user')
            self.assertIsNotNone(user.api_key)

        def test_get_user_with_incorrect_id(self):
            self.assertIsNone(self.auth.get_user(2))

        def test_get_user(self):
            user = self.auth.get_user(self.user.id)
            self.assertEqual(user, self.user)

except ImportError:
    # Install tastypie in order to run these tests
    pass
