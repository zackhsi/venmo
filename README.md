[![PyPI version](https://img.shields.io/pypi/v/venmo.svg)](https://pypi.python.org/pypi/venmo)
[![Build status](https://travis-ci.org/zackhsi/venmo.svg?branch=master)](https://travis-ci.org/zackhsi/venmo)

Venmo
=====

Pay or charge people on the command line!

```sh
venmo pay @zackhsi 23.19 "Thanks for the beer <3"
venmo charge 19495551234 23.19 "That beer wasn't free!"
```

Installation
------------
`venmo` can be installed via `pip`.

```sh
pip install venmo
```

Setup
-----
Set up venmo by running:

```sh
venmo configure

> Venmo email [None]: zackhsi@gmail.com
> Venmo password [None]:
> Verification code: 908126  # for 2 factor authentication
```

That's it!

Contributing
------------
Pull requests welcome! To get started, first clone the repository:

```sh
git clone git@github.com:zackhsi/venmo.git
```

Then install the development package:

```sh
python setup.py develop
```
