#!/usr/bin/env python

"""
Venmo CLI.

This script creates charge requests via the Venmo API.

    venv/bin/python -m venmo.cli user zmo 23.19 "tacos"
    venv/bin/python -m venmo.cli user 15305551050 23.19 "tacos"

    venv/bin/python -m venmo.cli group rent
"""

import argparse
import json
import urllib

import gevent
import gevent.pool
import requests

import venmo
from venmo import settings, oauth


def user(args):
    access_token = oauth.get_access_token()
    rent_charge = {
        'note': args.note,
        'phone': args.phone,
        'amount': args.amount,
    }
    create_rent_charge(rent_charge, access_token, args.run)


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
            _payments_url_with_params(params)
        ).json()
        _log_response(response)
    else:
        print "Would send charge {}".format(json.dumps(params, indent=4))


def _payments_url_with_params(params):
    return "{payments_base_url}?{params}".format(
        payments_base_url=settings.PAYMENTS_BASE_URL,
        params=urllib.urlencode(params),
    )


def _log_response(response):
    if 'error' in response:
        message = response['error']['message']
        code = response['error']['code']
        print 'message="{}" code={}'.format(message, code)
        return

    payment = response['data']['payment']
    target = payment['target']

    payment_action = payment['action']
    amount = payment['amount']
    if target['type'] == 'user':
        user = "{first_name} {last_name}".format(
            first_name=target['user']['first_name'],
            last_name=target['user']['last_name'],
        )
    else:
        user = target[target['type']],
    note = payment['note']

    print "{payment_action} {user} ${amount} for {note}".format(
        payment_action=payment_action,
        user=user,
        amount=amount,
        note=note,
    )


def main():
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    subparsers = parser.add_subparsers()

    parser_user = subparsers.add_parser('user')
    parser_user.add_argument("phone", help="who to send the request to")
    parser_user.add_argument(
        "amount",
        help="how much to pay or charge (negative to charge)",
    )
    parser_user.add_argument("note", help="what the request is for")
    parser_user.add_argument("--run", default=False, action='store_true',
                             help="whether to actually send the charges")
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
