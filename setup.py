from distutils.core import setup

setup(
    name='freebox_v5_status',
    version='1.1.0',
    author='Mickael Le Baillif',
    author_email='mickael.le.baillif@gmail.com',
    packages=['freebox_v5_status'],
    scripts=['bin/freebox_to_graphite.py', 'bin/freebox_show_status.py'],
    url='http://github.com/demikl/freeboxv5-status',
    license='LICENSE.txt',
    description='Parse Freebox V5 status page',
    long_description=open('README.md').read(),
)


#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys

from setuptools import setup
from setuptools.command.install import install

# circleci.py version
VERSION = "1.1.0"

def readme():
    """print long description"""
    with open('README.md') as f:
        return f.read()


class VerifyVersionCommand(install):
    """Custom command to verify that the git tag matches our version"""
    description = 'verify that the git tag matches our version'

    def run(self):
        tag = os.getenv('CIRCLE_TAG')

        if tag != VERSION:
            info = "Git tag: {0} does not match the version of this app: {1}".format(
                tag, VERSION
            )
            sys.exit(info)

setup(
    name='freebox_v5_status',
    version=VERSION,
    url='http://github.com/demikl/freeboxv5-status',
    author='Mickael Le Baillif',
    author_email='mickael.le.baillif@gmail.com',
    license='MIT',
    description='Parse Freebox V5 status page',
    long_description=readme(),
    keywords='freebox adsl',
    packages=['freebox_v5_status'],
    scripts=['bin/freebox_to_graphite.py', 'bin/freebox_show_status.py'],
    cmdclass={
        'verify': VerifyVersionCommand,
    }

)
