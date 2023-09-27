from argparse import ArgumentParser
from sys import stderr, stdin

from bibtefmt import bibtex, checker, formatter, printer


def format(args=None):
    args = _parse_args(args)
    text = _read(args.path)
    data = bibtex.parse(text)

    data = formatter.lowercase_entry_type(data)
    data = formatter.lowercase_tag_name(data)
    data = formatter.assign_keys(data)
    data = formatter.sort_entries(data)
    data = formatter.sort_tags(data)
    data = formatter.remove_duplicate_tags(data)
    data = formatter.remove_unknown_tags(data)
    data = formatter.remove_optional_tags(data)

    checker.check_unknown_entry_type(data)
    checker.check_duplicate_entry_key(data)
    checker.check_duplicate_tag(data)
    checker.check_missing_tag(data)
    checker.check_unknown_tag(data)
    checker.check_optional_tag(data)

    out = printer.print(data)
    _write(out, args.path)


def _parse_args(args):
    p = ArgumentParser()

    p.add_argument(
        "path",
        help="path to .bib file",
        nargs="?",
    )

    return p.parse_args(args)


def _check(func, data):
    for msg in func(data):
        print(msg, file=stderr)


def _read(path):
    if path is None:
        return stdin.read()
    with open(path) as f:
        return f.read()


def _write(out, path):
    if path:
        with open(path, "w") as f:
            print(out, file=f)
    else:
        print(out)
