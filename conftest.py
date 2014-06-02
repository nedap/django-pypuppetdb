"""
:copyright: Copyright 2014 by Ronald van Zon
:contact: rvzon84+django-pypuppetdb@gmail.com
"""
from __future__ import unicode_literals

from django.conf import settings


def pytest_configure():
    settings.configure(
        DATABASES={'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory:'
        }},
        CACHES={'default': {
            'BACKEND': 'django.core.cache.backends.dummy.DummyCache'
        }},
        INSTALLED_APPS=(
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'tastypie',
        ),
        ROOT_URLCONF='tests.urls',

        # Puppetdb config settings
        PUPPETDB_HOST = 'localhost',
        PUPPETDB_PORT = 8080,
        PUPPETDB_NODE = 'node',
        PUPPETDB_KEY = None,
        PUPPETDB_CERT = None,
        PUPPETDB_SSL_VERIFY = False
    )
