from functools import wraps
from .rule import rules


def foreach_entry(f):
    @wraps(f)
    def _(entries):
        for type, (key, tags) in entries:
            f(type, key, tags)
    return _


def require_rule(f):
    @wraps(f)
    def _(type, key, tags):
        rule = rules.get(type)
        if rule:
            f(rule, type, key, tags)
    return _
