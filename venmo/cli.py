#!/usr/bin/env python

"""
Venmo CLI.

This script creates charge requests via the Venmo API.

    ./venmo user zmo 23.19 "tacos"
    ./venmo user 15305551050 23.19 "tacos"

    ./venmo group rent
"""

import argparse
import json
import urllib

import gevent
import gevent.pool
import requests

import venmo
from venmo import settings, oauth
from helpers import log_response


def user(args):
    raise NotImplementedError()


def group(args):
    access_token = oauth.get_access_token()
    pool = gevent.pool.Pool(20)
    for rent_charge in venmo.rent.all():
        pool.spawn(
            create_rent_charge,
            rent_charge,
            access_token,
            args.run,
        )
    pool.join()


def create_rent_charge(rent_charge, access_token, run):
    params = {
        'access_token': access_token,
        'audience': 'private',
    }
    params.update(rent_charge)
    if run:
        response = requests.post(
            payments_url_with_params(params)
        ).json()
        log_response(response)
    else:
        print "Would send charge {}".format(json.dumps(params, indent=4))


def payments_url_with_params(params):
    return "{payments_base_url}?{params}".format(
        payments_base_url=settings.PAYMENTS_BASE_URL,
        params=urllib.urlencode(params),
    )


def main():
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    subparsers = parser.add_subparsers()

    parser_user = subparsers.add_parser('user')
    parser_user.set_defaults(func=user)

    parser_group = subparsers.add_parser('group')
    parser_group.add_argument("group", choices=['rent'])
    parser_group.add_argument("--run", default=False, action='store_true',
                              help="whether to actually send the charges")
    parser_group.set_defaults(func=group)

    parser_refresh_token = subparsers.add_parser('refresh-token')
    parser_refresh_token.set_defaults(func=oauth.refresh_token)

    args = parser.parse_args()
    args.func(args)


if __name__ == '__main__':
    main()
