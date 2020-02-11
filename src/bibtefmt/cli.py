import sys
from argparse import ArgumentParser
from . import formatter
from . import version


def run(args=None, stdin=sys.stdin, stdout=sys.stdout):
    parse_args(args)
    print(formatter.format(stdin.read()), file=stdout)


def parse_args(args):
    p = ArgumentParser('bibtefmt')

    p.add_argument(
        '-v', '--version',
        action='version',
        help='show version and exit',
        version=f'{version.MAJOR}.{version.MINOR}.{version.PATCH}'
    )

    return p.parse_args(args)
