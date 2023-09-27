from functools import wraps
from sys import stderr

from bibtefmt.bibtex import rules


def _foreach(f):
    @wraps(f)
    def _(entries):
        for e in entries:
            f(*e)

    return _


def _use_rule(f):
    @wraps(f)
    def _(typ, key, tags):
        if r := rules.get(typ.lower()):
            f(r, typ, key, tags)

    return _


def check_unknown_entry_type(entries):
    for t, _, _ in entries:
        if t not in rules:
            _warn(f'unknown entry type "{t}"')


def check_duplicate_entry_key(entries):
    for t in _find_dup(k for _, k, _ in entries):
        _warn(f'duplicate entry "{t}"')


@_foreach
def check_duplicate_tag(typ, key, tags):
    for n in _find_dup(n for n, _ in tags):
        _warn(f'duplicate tag "{n}" in "{key}"')


@_foreach
@_use_rule
def check_missing_tag(rule, typ, key, tags):
    ns = [n for n, _ in tags]
    for n in rule.req:
        if n not in ns:
            _warn(f'missing tag "{n}" in "{key}" ({typ})')
    for n1, n2 in rule.req_or_xor:
        if n1 not in ns and n2 not in ns:
            _warn(f'missing tag "{n1}" or "{n2}" in {key} ({typ})')


@_foreach
@_use_rule
def check_unknown_tag(rule, typ, key, tags):
    for n, _ in tags:
        if n not in rule.known:
            _warn(f'unknown tag "{n}" in "{key}" ({typ})')


@_foreach
@_use_rule
def check_tag_conflict(rule, typ, key, tags):
    ns = [n for n, _ in tags]
    for n1, n2 in rule.req_xor:
        if n1 in ns and n2 in ns:
            _warn(f'tag conflict "{n1}" and "{n2}" in "{key}" ({typ})')


@_foreach
@_use_rule
def check_optional_tag(rule, typ, key, tags):
    if rule.known_req:
        for n, _ in tags:
            if n in rule.known_opt:
                _warn(f'non-required tag "{n}" in "{key}" ({typ})')


def _find_dup(seq):
    lst = list(seq)
    for e in set(lst):
        if 1 < lst.count(e):
            yield e


def _warn(msg):
    print(msg, file=stderr)
