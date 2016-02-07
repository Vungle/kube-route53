try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'AWS Route53',
    'author': 'Garland Kan',
    'url': '',
    'download_url': '',
    'author_email': '',
    'version': '0.1',
    'install_requires': ['nose2', 'boto3', 'botocore', 'configparser'],
    'packages': [],
    'scripts': [],
    'name': 'awsRoute53'
}

setup(**config)
