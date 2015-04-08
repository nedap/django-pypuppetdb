import django
from django.contrib.auth.models import User
from django.test import TestCase
from django.test.runner import setup_databases
from mock import patch, Mock
from django_pypuppetdb.django_authentication import PuppetDBAuthentication

django.setup()
# Only create a database once
setup_databases(1, 1)


class TestDjangoAuthentication(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            username='test', email='test@nedap.com')
        self.auth = PuppetDBAuthentication()

    def test_authenticate_without_connection(self):
        self.assertIsNone(self.auth.authenticate())

    @patch('django_pypuppetdb.user_authentication.UserAuthentication.'
           'check_user', Mock(return_value=None))
    def test_authenticate_incorrect_username(self):
        self.assertIsNone(self.auth.authenticate('test'))

    @patch('django_pypuppetdb.user_authentication.UserAuthentication.'
           'check_user', Mock(return_value=None))
    @patch('django_pypuppetdb.user_authentication.UserAuthentication.'
           'verify_password', Mock(return_value=True))
    def test_authenticate_incorrect_password(self):
        self.assertIsNone(self.auth.authenticate('test'))

    @patch('django_pypuppetdb.user_authentication.UserAuthentication.'
           'check_user', Mock(
               return_value=Mock(parameters={'groups': 'a'})
           ))
    @patch('django_pypuppetdb.user_authentication.UserAuthentication.'
           'verify_password', Mock(return_value=True))
    def test_authenticate_with_existing_user(self):
        user = self.auth.authenticate('test', 'password')
        self.assertIsInstance(user, User)
        self.assertEqual(user.username, 'test')
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    @patch('django_pypuppetdb.user_authentication.UserAuthentication.'
           'check_user', Mock(
               return_value=Mock(parameters={'groups': 'a'})
           ))
    @patch('django_pypuppetdb.user_authentication.UserAuthentication.'
           'verify_password', Mock(return_value=True))
    def test_authenticate_with_new_user(self):
        user = self.auth.authenticate('new user', 'password')
        self.assertIsInstance(user, User)
        self.assertEqual(user.username, 'new user')
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    @patch('django_pypuppetdb.user_authentication.UserAuthentication.'
           'check_user', Mock(
               return_value=Mock(parameters={'groups': 'admins'})
           ))
    @patch('django_pypuppetdb.user_authentication.UserAuthentication.'
           'verify_password', Mock(return_value=True))
    def test_user_has_admin_rights(self):
        user = self.auth.authenticate('new user', 'password')
        self.assertIsInstance(user, User)
        self.assertEqual(user.username, 'new user')
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)

    def test_get_user_with_incorrect_id(self):
        self.assertIsNone(self.auth.get_user(2))

    def test_get_user(self):
        user = self.auth.get_user(self.user.id)
        self.assertEqual(user, self.user)
