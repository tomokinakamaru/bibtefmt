from argparse import ArgumentParser
from sys import stdin
from . import analyzer
from . import compiler
from . import formatter
from . import parser
from . import version


def bibtefmt(args=None):
    args = parse_args(args)
    bib = read(args.path)
    ast = parser.parse(bib)
    seq = compiler.compile(ast, args)
    analyzer.find_unknown_entry_type(seq)
    analyzer.find_duplicate_entry_key(seq)
    analyzer.find_duplicate_tag(seq)
    analyzer.find_missing_tag(seq)
    analyzer.find_unknown_tag(seq)
    analyzer.find_conflicting_tag(seq)
    analyzer.find_optional_tag(seq)
    out = formatter.format(seq)
    write(out, args.path)


def parse_args(args):
    p = ArgumentParser('bibtefmt')

    p.add_argument('path', help='path to .bib file', nargs='?')

    p.add_argument(
        '-v', '--version',
        action='version',
        help='show version and exit',
        version=f'{version.MAJOR}.{version.MINOR}.{version.PATCH}'
    )

    p.add_argument(
        '-n', '--no-extra-tags',
        action='store_true',
        help='Remove unknown/non-required tags'
    )

    return p.parse_args(args)


def read(path):
    if path is None:
        return stdin.read()
    with open(path) as f:
        return f.read()


def write(out, path):
    if path:
        with open(path, 'w') as f:
            print(out, file=f)
    else:
        print(out)
