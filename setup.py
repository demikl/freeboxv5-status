from distutils.core import setup

setup(
    name='freebox_v5_status',
    version='1.0.0',
    author=u'Mickaël Le Baillif',
    author_email='mickael.le.baillif@gmail.com',
    packages=['freeboxstatus'],
    scripts=['bin/freebox_to_graphite.py'],
    url='http://github.com/demikl/freeboxv5-status',
    license='LICENSE.txt',
    description='Parse Freebox V5 status page',
    long_description=open('README.md').read(),
    install_requires=[
        "urllib2"
    ],
)