"""
Argument types
"""

import argparse


def positive_string(s):
    if float(s) <= 0:
        raise argparse.ArgumentTypeError("{} is not positive".format(s))
    return s
