import codecs
import os.path
import re

from setuptools import setup


def fpath(name):
    return os.path.join(os.path.dirname(__file__), name)


def read(fname):
    return codecs.open(fpath(fname), encoding='utf-8').read()


def grep(attrname, filename):
    pattern = r"{0}\W*=\W*'([^']+)'".format(attrname)
    file_text = read(fpath(filename))
    strval, = re.findall(pattern, file_text)
    return strval


setup(
    name='venmo',
    version=grep('__version__', 'venmo/__version__.py'),
    description='Venmo CLI',
    long_description=read(fpath('README.rst')),
    url='http://github.com/zackhsi/venmo',
    author='Zack Hsi',
    author_email='zackhsi@gmail.com',
    license='MIT',
    packages=['venmo'],
    install_requires=[
        'requests>=2.9.1',
    ],
    entry_points={
        'console_scripts': [
            'venmo = venmo.cli:main',
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.6',
    ]
)
