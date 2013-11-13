from distutils.core import setup

setup(
    name='freebox_v5_status',
    version='1.0.0',
    author='Mickael Le Baillif',
    author_email='mickael.le.baillif@gmail.com',
    packages=['freebox_v5_status'],
    scripts=['bin/freebox_to_graphite.py'],
    url='http://github.com/demikl/freeboxv5-status',
    license='LICENSE.txt',
    description='Parse Freebox V5 status page',
    long_description=open('README.md').read(),
)