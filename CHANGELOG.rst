#########
Changelog
#########

0.0.1
=====
Initial release. Implements most of authorization for django.

0.0.2
=====
Separating Django and Tastypie dependency.

0.0.3
=====
Renaming Django authenticaton and updated all tests
Renaming Tastyie authentication and updated all tests

0.1.0
=====
Django and Tastypie fully tested

0.1.1
=====
Adding check for puppet group that will check if the user
is in the group defined in PUPPETDB_ADMIN_GROUP. This will give the
user admin rights allowing the user to login django-admin.