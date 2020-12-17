import sys
from argparse import ArgumentParser
from . import formatter
from . import version


def run(args=None, stdin=sys.stdin, stdout=sys.stdout):
    namespace = parse_args(args)
    if namespace.path is None:
        print(formatter.format(stdin.read()), file=stdout)
    else:
        content = read_file(namespace.path)
        formatted = formatter.format(content)
        with open(namespace.path, 'w') as f:
            print(formatted, file=f)


def read_file(path):
    with open(path) as f:
        return f.read()


def parse_args(args):
    p = ArgumentParser('bibtefmt')

    p.add_argument(
        '-v', '--version',
        action='version',
        help='show version and exit',
        version=f'{version.MAJOR}.{version.MINOR}.{version.PATCH}'
    )

    p.add_argument(
        'path',
        help='path to .bib file',
        nargs='?'
    )

    return p.parse_args(args)
