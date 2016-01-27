#!/usr/bin/env python

"""
Venmo CLI.

Pay or charge people via the Venmo API:

    venmo pay @zackhsi 23.19 "Thanks for the beer <3"
    venmo charge 19495551234 23.19 "That beer wasn't free!"

Configure with:

    venmo configure
"""

import argparse
import os
from datetime import datetime

from venmo import __version__, auth, payment, settings, user


def status(args):
    """Print out system status

    $ venmo status
    Version 0.3.2
    Credentials (updated 2016-01-26 19:48):
        User: youremailaddress
        Token: youraccesstoken
    """
    print "\n".join([_version(), _credentials()])


def _version():
    return "Version {}".format(__version__)


def _credentials():
    try:
        updated_at = os.path.getmtime(settings.CREDENTIALS_FILE)
        updated_at = datetime.fromtimestamp(updated_at)
        updated_at = updated_at.strftime("%Y-%m-%d %H:%M")
        return """Credentials (updated {updated_at}):
    User: {user}
    Token: {token}""".format(updated_at=updated_at,
                             user=auth.get_username(),
                             token=auth.get_access_token())
    except OSError:
        return "No credentials"


def main():
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    subparsers = parser.add_subparsers()

    for action in ["pay", "charge"]:
        subparser = subparsers.add_parser(action)
        subparser.add_argument(
            "user",
            help="who to {}, either phone or username".format(action),
        )
        subparser.add_argument("amount", help="how much to pay or charge")
        subparser.add_argument("note", help="what the request is for")
        subparser.set_defaults(func=getattr(payment, action))

    parser_configure = subparsers.add_parser('configure')
    parser_configure.set_defaults(func=auth.configure)

    parser_search = subparsers.add_parser('search')
    parser_search.add_argument("query", help="search query")
    parser_search.set_defaults(func=user.print_search)

    parser_status = subparsers.add_parser('status')
    parser_status.set_defaults(func=status)

    parser_reset = subparsers.add_parser('reset')
    parser_reset.set_defaults(func=auth.reset)

    parser.add_argument('-v', '--version', action='version',
                        version='%(prog)s ' + __version__)

    args = parser.parse_args()
    args.func(args)


if __name__ == '__main__':
    main()
