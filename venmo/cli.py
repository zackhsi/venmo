#!/usr/bin/env python

'''
Venmo CLI.

Pay or charge people via the Venmo API:

  venmo pay @zackhsi 23.19 'Thanks for the beer <3'
  venmo charge 19495551234 23.19 'That beer wasn't free!'
'''

import argparse
import os
import sys
from datetime import datetime

import venmo


def status():
    '''Print out system status

    $ venmo status
    Version 0.3.2
    Credentials (updated 2016-01-26 19:48):
        User: youremailaddress
        Token: youraccesstoken
    '''
    print('\n'.join([_version(), _credentials()]))


def _version():
    return 'Version {}'.format(venmo.__version__)


def _credentials():
    try:
        updated_at = os.path.getmtime(venmo.settings.CREDENTIALS_FILE)
        updated_at = datetime.fromtimestamp(updated_at)
        updated_at = updated_at.strftime('%Y-%m-%d %H:%M')
        return '''Credentials (updated {updated_at}):
    User: {user}
    Token: {token}'''.format(updated_at=updated_at,
                             user=venmo.auth.get_username(),
                             token=venmo.auth.get_access_token())
    except OSError:
        return 'No credentials'


def parse_args():
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    subparsers = parser.add_subparsers()

    for action in ['pay', 'charge']:
        subparser = subparsers.add_parser(action,
                                          help='{} someone'.format(action))
        subparser.add_argument(
            'user',
            help='who to {}, either phone or username'.format(action),
        )
        subparser.add_argument('amount', type=venmo.types.positive_float,
                               help='how much to pay or charge')
        subparser.add_argument('note', help='what the request is for')
        subparser.set_defaults(func=getattr(venmo.payment, action))

    parser_configure = subparsers.add_parser('configure',
                                             help='set up credentials')
    parser_configure.set_defaults(func=venmo.auth.configure)

    parser_search = subparsers.add_parser('search', help='search users')
    parser_search.add_argument('query', help='search query')
    parser_search.set_defaults(func=venmo.user.print_search)

    parser_status = subparsers.add_parser('status', help='get status')
    parser_status.set_defaults(func=status)

    parser_reset = subparsers.add_parser('reset', help='reset saved data')
    parser_reset.set_defaults(func=venmo.auth.reset)

    parser.add_argument('-v', '--version', action='version',
                        version='%(prog)s ' + venmo.__version__)

    if len(sys.argv) == 1:
        sys.argv.append('-h')
    args = parser.parse_args()
    func = args.func
    del args.func
    func(**vars(args))


def main():
    try:
        parse_args()
    except KeyboardInterrupt:
        print('')


if __name__ == '__main__':
    main()
