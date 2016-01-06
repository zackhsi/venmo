from setuptools import setup

requirements = [
    'gevent==1.1b5',  # https://github.com/NixOS/nixpkgs/issues/7275
    'greenlet==0.4.9',
    'requests==2.9.1',
]

setup(
    name='venmo',
    version='0.2.0',
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
