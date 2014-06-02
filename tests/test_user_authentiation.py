from django.test import TestCase, RequestFactory
from mock import patch
from pypuppetdb.types import Resource, Node

from django_pypuppetdb.user_authentication import UserAuthentication


UNAUTHORIZED = 401


def generator():
    yield Resource('cert', 'test.user', 'User', [], False, '', 0, {})


def trigger_error(node):
    raise StopIteration


class TestUserAuthentication(TestCase):
    def setUp(self):
        self.ua = UserAuthentication()
        self.factory = RequestFactory()
        self.request = self.factory.get('/login')
        self.basic_auth = 'Basic dXNlcm5hbWU6cGFzc3dvcmQ='
        self.password = '$6$rounds=100000$oj7kfKZU.VKTRkF2$GYjwfj7b/BfhAyT1B' \
                        'mXitF76uYiZDh9IuvEsZggm/x9HiinIkPihMeoUvOQ.uffUtAS6' \
                        'UxSpdbWkKyJ5/2IUY0'

    def test_is_authenticated_without_data(self):
        self.assertIsNone(self.ua.is_authenticated(self.request))

    def test_is_authenticated_with_incorrect_authorization(self):
        self.request.META['HTTP_AUTHORIZATION'] = 'something random'
        self.assertIsNone(self.ua.is_authenticated(self.request))

    def test_is_authenticated_with_correct_authorization(self):
        self.request.META['HTTP_AUTHORIZATION'] = self.basic_auth
        self.assertIsNone(self.ua.is_authenticated(self.request))

    @patch(
        'django_pypuppetdb.user_authentication.UserAuthentication.check_user')
    def test_is_authenticated_with_valid_username(self, check_user):
        check_user.return_value = 'test'
        self.request.META['HTTP_AUTHORIZATION'] = self.basic_auth
        self.assertFalse(self.ua.is_authenticated(self.request))

    @patch(
        'django_pypuppetdb.user_authentication.UserAuthentication.check_user')
    @patch('django_pypuppetdb.user_authentication.UserAuthentication.'
           'verify_password')
    def test_is_authenticated_with_valid_password(
            self, check_user, verify_password):
        check_user.return_value = 'test'
        verify_password.return_value = True
        self.request.META['HTTP_AUTHORIZATION'] = self.basic_auth
        self.assertTrue(self.ua.is_authenticated(self.request))

    def test_check_authorization_without_data(self):
        self.assertIsNone(self.ua.check_authorization(self.request))

    def test_check_authorization_with_invalid_data(self):
        self.request.META['HTTP_AUTHORIZATION'] = 'test'
        self.assertIsNone(self.ua.check_authorization(self.request))

    def test_check_authorization_with_invalid_basic_type(self):
        self.request.META['HTTP_AUTHORIZATION'] = 'random username:password'
        self.assertIsNone(self.ua.check_authorization(self.request))

    def test_check_authorization_with_valid_data(self):
        self.request.META['HTTP_AUTHORIZATION'] = self.basic_auth
        expect = ['username', 'password']
        result = self.ua.check_authorization(self.request)
        self.assertEqual(expect, result)

    def test_check_authorization_with_to_much_data(self):
        self.request.META[
            'HTTP_AUTHORIZATION'] = 'Basic dXNlcjpwYXNzOnNvbWV0aGluZw=='
        self.assertIsNone(self.ua.check_authorization(self.request))

    def test_check_user_without_connection(self):
        self.assertFalse(self.ua.check_user('test.user'))

    @patch('pypuppetdb.api.v3.API.node')
    def test_check_user_without_result(self, node):
        node.side_effect = trigger_error
        self.assertIsNone(self.ua.check_user('test.user'))

    @patch('pypuppetdb.types.Node.resources')
    @patch('pypuppetdb.api.v3.API.node')
    def test_check_user_with_correct_data(self, node, resources):
        node.return_value = Node('v3', 'nl12s0016.healthcare.nedap.local')
        resources.return_value = generator()
        expect = 'User[test.user]'
        result = str(self.ua.check_user('test.user'))
        self.assertEqual(expect, result)

    def test_verify_password(self):
        user = lambda: None
        user.parameters = {'password': self.password}
        result = self.ua.verify_password(user, 'password')
        self.assertTrue(result)

    def test_verify_password_with_invalid_password(self):
        user = lambda: None
        user.parameters = {'password': self.password}
        self.assertFalse(self.ua.verify_password(user, '1234567890'))
