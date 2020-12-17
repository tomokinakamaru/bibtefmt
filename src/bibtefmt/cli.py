import sys
from argparse import ArgumentParser
from . import formatter
from . import version


def run(args=None, stdin=sys.stdin, stdout=sys.stdout, stderr=sys.stderr):
    namespace = parse_args(args)
    if namespace.path is None:
        entries, warnings = formatter.format(stdin.read())
        print(entries, file=stdout)
        print(warnings, file=stderr)
    else:
        content = read_file(namespace.path)
        entries, warnings = formatter.format(content)
        with open(namespace.path, 'w') as f:
            print(entries, file=f)
        print(warnings, file=stderr)


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
