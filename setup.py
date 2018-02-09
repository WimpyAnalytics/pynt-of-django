#!/usr/bin/env python
# -*- coding: utf-8 -*-


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


readme = open('README.rst').read()
history = open('HISTORY.rst').read().replace('.. :changelog:', '')

requirements = [
    'six',
    'Django',
    'pynt',
    'pynt-contrib',
]

test_requirements = [
    # None, these go into the test_requirements file
]

setup(
    name='pynt-of-django',
    version='0.3.1',
    description='A companion library for using pynt, a build tool, with Django projects.',
    long_description=readme + '\n\n' + history,
    author='Ivan Ven Osdel',
    author_email='ivan@wimpyanalytics.com',
    url='https://github.com/WimpyAnalytics/pynt-of-django',
    download_url='https://github.com/wimpyanalytics/pynt-of-django/tarball/0.3.1',
    packages=[
        'pyntofdjango',
    ],
    package_dir={'pyntofdjango':
                 'pyntofdjango'},
    include_package_data=True,
    install_requires=requirements,
    license="BSD",
    zip_safe=False,
    keywords=['pynt', 'django', 'build', 'make'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
)
