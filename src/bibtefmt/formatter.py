from functools import wraps
from re import sub
from string import ascii_lowercase
from unicodedata import normalize

from bibtefmt.bibtex import rules


def _foreach(f):
    @wraps(f)
    def _(entries):
        return [f(*e) for e in entries]

    return _


def _use_rule(f):
    @wraps(f)
    def _(typ, key, tags):
        if r := rules.get(typ.lower()):
            return f(r, typ, key, tags)

    return _


def sort_entries(entries):
    return sorted(entries, key=_sort_entries)


def assign_keys(entries):
    idx = {}
    for entry in entries:
        _, key, _ = entry
        if key.startswith("_"):
            d = idx.setdefault(key, {})
            d.setdefault(None, []).append(entry)
        else:
            auth = _get_author(entry)
            year = _get_year(entry)
            d = idx.setdefault(auth, {})
            d.setdefault(year, []).append(entry)

    out = []
    for auth in idx:
        for year in idx[auth]:
            es = idx[auth][year]
            if year is None:
                typ, _, tags = es[0]
                out.append([typ, auth, tags])
            elif len(es) == 1:
                typ, _, tags = es[0]
                key = f"{auth}{year}"
                out.append([typ, key, tags])
            else:
                for i, e in enumerate(es):
                    suf = ascii_lowercase[i]
                    typ, _, tags = e
                    key = f"{auth}{year}{suf}"
                    out.append([typ, key, tags])
    return out


@_foreach
def sort_tags(typ, key, tags):
    return [typ, key, sorted(tags)]


@_foreach
def lowercase_entry_type(typ, key, tags):
    return [typ.lower(), key, tags]


@_foreach
def lowercase_tag_name(typ, key, tags):
    return [typ, key, [[n.lower(), v] for n, v in tags]]


@_foreach
def remove_duplicate_tags(typ, key, tags):
    tags = {n: v for n, v in tags}
    return [typ, key, [[n, v] for n, v in tags.items()]]


@_foreach
@_use_rule
def remove_unknown_tags(rule, typ, key, tags):
    tags = [[n, v] for n, v in tags if n in rule.known]
    return [typ, key, tags]


@_foreach
@_use_rule
def remove_optional_tags(rule, typ, key, tags):
    if rule.known_req:
        tags = [[n, v] for n, v in tags if n in rule.known_req]
        return [typ, key, tags]
    return [typ, key, tags]


def _sort_entries(entry):
    typ, key, _ = entry
    return (typ, key or "")


def _get_author(entry):
    _, _, tags = entry
    for n, v in tags:
        if n == "author":
            v = _unquote(v)
            v = v.split(" and ")[0].strip()
            if "," in v:
                v = v.split(",")[0].split()[-1]
                return _normalize_name(v)
            else:
                v = v.split()[-1]
                return _normalize_name(v)
    return "no-author"


def _get_year(entry):
    _, _, tags = entry
    for n, v in tags:
        if n == "year":
            return _unquote(v)[-2:]
    return "-no-year"


def _unquote(lst):
    t = lst[0]
    return t[1:-1] if t.startswith(("{", '"')) else t


def _normalize_name(name):
    name = name.lower()
    name = sub(r"\\.+{(.+)}", r"\1", name)
    name = normalize("NFKD", name)
    name = name.encode("ASCII", "ignore").decode()
    name = "".join(c for c in name if c in ascii_lowercase)
    return name
