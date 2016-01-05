#!/usr/bin/env python

"""
Python module to drop a TinyDB table.

    python -m venmo.drop_table rent
    python -m venmo.drop_table users
"""

import argparse
import venmo


def main():
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("table")
    args = parser.parse_args()
    print "Dropping table {} ...".format(args.table)
    venmo.db.table(args.table).purge()


if __name__ == '__main__':
    main()
