#################
django-pypuppetdb
#################

.. image:: https://api.travis-ci.org/nedap/django-pypuppetdb.png
   :target: https://travis-ci.org/nedap/django-pypuppetdb

.. image:: https://coveralls.io/repos/nedap/django-pypuppetdb/badge.png
   :target: https://coveralls.io/r/nedap/django-pypuppetdb

.. image:: https://pypip.in/d/django_pypuppetdb/badge.png
   :target: https://pypi.python.org/pypi/django_pypuppetdb

.. image:: https://pypip.in/v/django_pypuppetdb/badge.png
   :target: https://crate.io/packages/django-pypuppetdb

django-pypuppetdb is a library that handles authentication
by using the PuppetDB's REST API to get Users that are registrated
in PuppetDB. It is implemented using the `requests`_ library.

.. _requests: http://docs.python-requests.org/en/latest/

To use this library you will need:
    * Python 2.7+
    * Python 3.3+
    * Django 1.6+
    * pypuppetdb

Installation
============

You can install this package from source or from PyPi.

.. code-block:: bash

    $ pip install django-pypuppetdb

.. code-block:: bash

    $ git clone https://github.com/nedap/django-pypuppetdb
    $ python setup.py install

Django
------

To let django connect to puppetdb in order to get your user
add the following line to you settings.

    * add "django_pypuppetdb" to INSTALLED_APPS.
    * add "django_pypuppetdb.django_authentication.PuppetDBAuthentication" to AUTHENTICATION_BACKENDS

    * add the followin settings

.. code-block:: python

        PUPPETDB_HOST = 'localhost',
        PUPPETDB_PORT = 8080,
        PUPPETDB_NODE = 'node',
        PUPPETDB_KEY = None,
        PUPPETDB_CERT = None,
        PUPPETDB_SSL_VERIFY = False
        PUPPETDB_ADMIN_GROUP = 'admins'

Tastypie
--------

If you are using tastypie as API framework and want to use pypuppetdb to
validate the user you can add the following line to your resource file

.. code-block:: python

    from django_pypuppetdb.tastypie_authentication import PuppetDBAuthentication

    in your class Meta add:
    authentication = PuppetDBAuthentication()

if you would like to use multiple authentications you can use

.. code-block:: python

    authentication = MultiAuthentication(ApiKeyAuthentication(), PuppetDBAuthentication())

Getting Help
============
This project is still very new so most likely there will be issues
you'll run into.

For bug reports you can file an `issue`_. If you need help with something
feel free to hit up `@eagllus`_ by e-mail.

.. _issue: https://github.com/nedap/pypuppetdb/issues
.. _@eagllus: https://github.com/eagllus