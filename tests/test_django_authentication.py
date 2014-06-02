from django.contrib.auth.models import User
from django.test import TestCase
from django.test.runner import setup_databases
from mock import patch
from django_pypuppetdb.django_authentication import PuppetDBAuthentication


# Only create a database once
setup_databases(1, 1)


class TestDjangoAuthentication(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            username='test', email='test@nedap.com')
        self.auth = PuppetDBAuthentication()

    def test_authenticate_without_connection(self):
        self.assertIsNone(self.auth.authenticate())

    @patch(
        'django_pypuppetdb.user_authentication.UserAuthentication.check_user')
    def test_authenticate_incorrect_username(self, check_user):
        check_user.return_value = None
        self.assertIsNone(self.auth.authenticate('test'))

    @patch(
        'django_pypuppetdb.user_authentication.UserAuthentication.check_user')
    @patch('django_pypuppetdb.user_authentication.UserAuthentication.'
           'verify_password')
    def test_authenticate_with_existing_user(
            self, check_user, verify_password):
        check_user.return_value = 'test'
        verify_password.return_value = True
        user = self.auth.authenticate('test', 'password')
        self.assertIsInstance(user, User)
        self.assertEqual(user.username, 'test')

    @patch(
        'django_pypuppetdb.user_authentication.UserAuthentication.check_user')
    @patch('django_pypuppetdb.user_authentication.UserAuthentication.'
           'verify_password')
    def test_authenticate_with_new_user(self, check_user, verify_password):
        check_user.return_value = 'new user'
        verify_password.return_value = True
        user = self.auth.authenticate('new user', 'password')
        self.assertIsInstance(user, User)
        self.assertEqual(user.username, 'new user')

    def test_get_user_with_incorrect_id(self):
        self.assertIsNone(self.auth.get_user(2))

    def test_get_user(self):
        user = self.auth.get_user(self.user.id)
        self.assertEqual(user, self.user)
