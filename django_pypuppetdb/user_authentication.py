import base64

import pypuppetdb
from passlib.hash import sha512_crypt
from django.conf import settings
from requests import ConnectionError


class UserAuthentication(object):
    def is_authenticated(self, request, **kwargs):
        bits = self.check_authorization(request, **kwargs)
        if bits is not None:
            user = self.check_user(bits)

            if user is not None and user is not False:
                return self.verify_password(user, bits)

    def check_authorization(self, request, **kwargs):
        if not request.META.get('HTTP_AUTHORIZATION'):
            return None

        try:
            (auth_type, data) = request.META['HTTP_AUTHORIZATION'].split()
            if auth_type.lower() != 'basic':
                return None
            user_pass = base64.b64decode(data).decode('utf-8')
        except:
            return None

        bits = user_pass.split(':')

        if len(bits) != 2:
            return None
        return bits

    @staticmethod
    def check_user(username):
        puppet_db = pypuppetdb.connect(host=settings.PUPPETDB_HOST,
                                       port=settings.PUPPETDB_PORT,
                                       ssl_verify=settings.PUPPETDB_SSL_VERIFY,
                                       ssl_key=settings.PUPPETDB_KEY,
                                       ssl_cert=settings.PUPPETDB_CERT)

        try:
            node = puppet_db.node(settings.PUPPETDB_NODE)
            return next(node.resources(type_='User', title=username))
        except ConnectionError:
            return False
        except StopIteration:
            return None

    @staticmethod
    def verify_password(user, password):
        try:
            return sha512_crypt.verify(password, user.parameters['password'])
        except:
            return False
