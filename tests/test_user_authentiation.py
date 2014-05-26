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

    def test_check_http_authorization_without_data(self):
        self.assertIsNone(self.ua.check_http_authorization(self.request))

    def test_check_http_authorization_with_invalid_data(self):
        self.request.META['HTTP_AUTHORIZATION'] = 'test'
        self.assertIsNone(self.ua.check_http_authorization(self.request))

    def test_check_http_authorization_with_invalid_basic_type(self):
        self.request.META['HTTP_AUTHORIZATION'] = 'random username:password'
        self.assertEqual(UNAUTHORIZED, self.ua.check_http_authorization(self.request).status_code)

    def test_check_http_authorization_with_valid_data(self):
        self.request.META['HTTP_AUTHORIZATION'] = 'Basic dXNlcm5hbWU6cGFzc3dvcmQ='
        self.assertEqual([u'username', u'password'], self.ua.check_http_authorization(self.request))

    @patch('pypuppetdb.types.Node.resources')
    @patch('pypuppetdb.api.v3.API.node')
    def test_check_puppetdb_user_with_correct_data(self, node, resources):
        node.return_value = Node('v3', 'nl12s0016.healthcare.nedap.local')
        resources.return_value = generator()
        self.assertEqual('User[test.user]', str(self.ua.check_puppetdb_user('test.user')))

    def test_check_puppetdb_user_without_connection(self):
        self.assertFalse(self.ua.check_puppetdb_user('test.user'))

    @patch('pypuppetdb.api.v3.API.node')
    def test_check_puppetdb_user_without_result(self, node):
        node.side_effect = trigger_error
        self.assertIsNone(self.ua.check_puppetdb_user('test.user'))

    def test_check_puppetdb_verify__correct_password(self):
        user = lambda: None
        user.parameters = {'password': u'$6$rounds=100000$oj7kfKZU.VKTRkF2$GYjwfj7b/BfhAyT1BmXitF76uYiZDh9IuvEsZggm/x9HiinIkPihMeoUvOQ.uffUtAS6UxSpdbWkKyJ5/2IUY0'}
        self.assertTrue(self.ua.check_puppetdb_verify_password(user, 'password'))

    def test_check_puppetdb_verify_incorrect_password(self):
        user = lambda: None
        user.parameters = {'password': u'$6$rounds=100000$oj7kfKZU.VKTRkF2$GYjwfj7b/BfhAyT1BmXitF76uYiZDh9IuvEsZggm/x9HiinIkPihMeoUvOQ.uffUtAS6UxSpdbWkKyJ5/2IUY0'}
        self.assertFalse(self.ua.check_puppetdb_verify_password(user, '1234567890'))

    def test_is_authenticated_without_data(self):
        self.assertEqual(UNAUTHORIZED, self.ua.is_authenticated(self.request).status_code)

    def test_is_authenticated_with_correct_user_without_connection(self):
        self.request.META['HTTP_AUTHORIZATION'] = 'Basic dXNlcm5hbWU6cGFzc3dvcmQ='
        self.assertEqual(UNAUTHORIZED, self.ua.is_authenticated(self.request).status_code)

    def test_is_authenticated_with_correct_user_with_connection(self):
        self.request.META['HTTP_AUTHORIZATION'] = 'Basic dXNlcm5hbWU6cGFzc3dvcmQ='
        self.assertEqual(UNAUTHORIZED, self.ua.is_authenticated(self.request).status_code)

    def test_is_authenticated_with_correct_user_and_password(self):
        self.request.META['HTTP_AUTHORIZATION'] = 'Basic dXNlcm5hbWU6cGFzc3dvcmQ='
        self.assertEqual(UNAUTHORIZED, self.ua.is_authenticated(self.request).status_code)
