import sys

import os
import codecs
from setuptools import setup, find_packages


if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

with codecs.open('README.rst', encoding='utf-8') as f:
    README = f.read()

with codecs.open('CHANGELOG.rst', encoding='utf-8') as f:
    CHANGELOG = f.read()

setup(
    name='django_pypuppetdb',
    version='0.1.0',
    url='https://github.com/nedap/django-pypuppetdb',
    license='Apache License 2.0',
    description='Handles authorization for Django by using puppetdb users',
    long_description='\n'.join((README, CHANGELOG)),
    keywords='puppet puppetdb django authorization tastypie',

    author='Ronald van Zon',
    author_email='rvzon84+django-pypuppetdb@gmail.com',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Topic :: Software Development :: Libraries'
    ],
)
