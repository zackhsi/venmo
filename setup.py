from setuptools import setup

import venmo

requirements = [
    'requests==2.9.1',
]

setup(
    name='venmo',
    version=venmo.__version__,
    description='Venmo CLI',
    url='http://github.com/zackhsi/venmo',
    author='Zack Hsi',
    author_email='zackhsi@gmail.com',
    license='MIT',
    packages=['venmo'],
    install_requires=requirements,
    entry_points={
        'console_scripts': [
            'venmo = venmo.cli:main',
        ],
    },
)
