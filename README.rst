.. image:: https://img.shields.io/pypi/v/venmo.svg
    :target: https://pypi.python.org/pypi/venmo

.. image:: https://travis-ci.org/zackhsi/venmo.svg?branch=master
    :target: https://travis-ci.org/zackhsi/venmo

Venmo
=====

Pay or charge people on the command line!

::

    $ venmo pay @zackhsi 23.19 "Thanks for the beer <3"
    $ venmo charge 19495551234 23.19 "That beer wasn't free!"

Installation
------------

``venmo`` can be installed via ``pip``.

::

    $ pip install venmo

Setup
-----
Set up venmo by running:

::

    $ venmo configure

    > Venmo email [None]: zackhsi@gmail.com
    > Venmo password [None]:
    > Verification code: 908126  # for 2 factor authentication

That's it!

Contributing
------------
Pull requests welcome! To get started, first clone the repository:

::

    $ git clone git@github.com:zackhsi/venmo.git

Create a virtualenv containing an editable installation of venmo, plus
development dependencies:

::

    $ make init

Activate the virtualenv:

::

    $ pipenv shell

Run tests:

::

    $ make test
