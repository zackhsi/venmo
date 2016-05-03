'''
Argument types
'''

import argparse


def positive_float(s):
    if float(s) <= 0:
        raise argparse.ArgumentTypeError('{} is not positive'.format(s))
    return float(s)
