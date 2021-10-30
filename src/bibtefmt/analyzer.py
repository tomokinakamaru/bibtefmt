from sys import stderr
from .analyzerutil import foreach_entry
from .analyzerutil import require_rule
from .rule import rules


def find_unknown_entry_type(entries):
    for type, _ in entries:
        if type not in rules:
            warn(f'unknown entry type "{type}"')


def find_duplicate_entry_key(entries):
    keys = [key for _, (key, _) in entries]
    for k in set(keys):
        if 1 < keys.count(k):
            warn(f'duplicate entry key "{k}"')


@foreach_entry
def find_duplicate_tag(_, key, tags):
    names = [name for name, _ in tags]
    for n in set(names):
        if 1 < names.count(n):
            warn(f'duplicate tag "{n}" in "{key}"')


@foreach_entry
@require_rule
def find_missing_tag(rule, type, key, tags):
    names = [name for name, _ in tags]
    for n in rule.req:
        if n not in names:
            warn(f'missing tag "{n}" in "{key}" ({type})')
    for n1, n2 in rule.req_or_xor:
        if n1 not in names and n2 not in names:
            warn(f'missing tag "{n1}" or "{n2}" in {key} ({type})')


@foreach_entry
@require_rule
def find_unknown_tag(rule, type, key, tags):
    for name, _ in tags:
        if name not in rule.known:
            warn(f'unknown tag "{name}" in "{key}" ({type})')


@foreach_entry
@require_rule
def find_conflicting_tag(rule, type, key, tags):
    names = [name for name, _ in tags]
    for n1, n2 in rule.req_xor:
        if n1 in names and n2 in names:
            warn(f'conflicting tag "{n1}" and "{n2}" in "{key}" ({type})')


@foreach_entry
@require_rule
def find_optional_tag(rule, type, key, tags):
    for name, _ in tags:
        if name in rule.known_opt:
            warn(f'non-required tag "{name}" in "{key}" ({type})')


def warn(msg):
    print(msg, file=stderr)
