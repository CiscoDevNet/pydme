from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the relevant file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='pydme',

    version='0.1.0',

    description='Python Bindings for Cisco DME REST API',
    long_description=long_description,

    url='https://github.com/datacenter/pydme',

    author='Sai Chintalapudi',
    author_email='saichint@cisco.com',

    license='Apache',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 3 - Alpha',

        'Intended Audience :: Developers',
        'Topic :: System :: Networking',

        'License :: OSI Approved :: Apache Software License',

        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
    ],

    keywords='cisco dme apic datacenter nxos',

    packages=find_packages(exclude=['docs', 'examples', 'tests']),

    # Install files from MANIFEST.in.
    include_package_data=True,

    # List run-time dependencies here.  These will be installed by pip when
    # your project is installed. For an analysis of "install_requires" vs pip's
    # requirements files see:
    # https://packaging.python.org/en/latest/requirements.html
    install_requires=[
        'anytree',
        'Flask',
        'lxml',
        'paramiko',
        'parse',
        'pyopenssl',
        'pyyaml',
        'requests',
        'scp',
        'websocket-client',
        'xmltodict',
    ],

    # List additional groups of dependencies here (e.g. development
    # dependencies). You can install these using the following syntax,
    # for example:
    # $ pip install -e .[dev,test]
    extras_require={
        'doc': [
            'sphinx',
        ],

        'test': [
            'coverage',
            'httpretty',
            'nose',
            'sure',
        ],
    }
)
