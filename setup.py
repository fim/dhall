#!/usr/bin/env python

from distutils.core import setup

execfile('modules/dhall/version.py')

setup(name='dhall',
    version=__version__,
    description='Sign/Verify tool',
    author=__maintainer__,
    install_requires=[
        'ed25519==1.3'
    ],
    package_dir = {'': 'modules'},
    packages=['dhall'],
    scripts=['dhall']
)
