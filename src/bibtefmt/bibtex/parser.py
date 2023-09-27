# REF: http://www.bibtex.org/Format/
from pyparsing import (
    CharsNotIn,
    Forward,
    Optional,
    QuotedString,
    Suppress,
    White,
    Word,
    ZeroOrMore,
    alphas,
    delimited_list,
)


def parse(text):
    return _entries.parse_string(text, True)[0]


def _mk_text(toks):
    return ["".join(toks)]


def _mk_list(toks):
    return [list(toks)]


def _mk_entry_body(toks):
    t1 = toks[1] if 1 < len(toks) else []
    return [[toks[0], t1]]


def _mk_entry(toks):
    t1 = toks[1] if 1 < len(toks) else [None, []]
    return [[toks[0], *t1]]


_spaces = Suppress(Optional(White()))

_nonbraced_text = CharsNotIn("{}")
_nonbraced_text.set_parse_action(_mk_text)

_braced_text = Forward()
_braced_text_elems = Forward()

_braced_text << "{" + _braced_text_elems + "}"
_braced_text.set_parse_action(_mk_text)

_braced_text_elems << ZeroOrMore(_nonbraced_text | _braced_text)
_braced_text_elems.set_parse_action(_mk_text)

_quoted_text = QuotedString('"', "\\", unquoteResults=False, multiline=True)
_quoted_text.set_parse_action(_mk_text)

_entry_key = _spaces + CharsNotIn("#\\@,={} \t\n") + _spaces
_entry_key.set_parse_action(_mk_text)

_tag_value = delimited_list(_braced_text | _quoted_text | _entry_key, "#")
_tag_value.set_parse_action(_mk_list)

_tag_name = _spaces + CharsNotIn("#\\@,={} \t\n") + _spaces
_tag_name.set_parse_action(_mk_text)

_tag = _tag_name + Suppress("=") + _tag_value
_tag.set_parse_action(_mk_list)

_tags = delimited_list(_tag, ",", allow_trailing_delim=True)
_tags.set_parse_action(_mk_list)

_entry_body = _entry_key + Optional(Suppress(",") + Optional(_tags))
_entry_body.set_parse_action(_mk_entry_body)

_entry_type = Suppress("@") + Word(alphas)
_entry_type.set_parse_action(_mk_text)

_entry = _entry_type + Suppress("{") + Optional(_entry_body) + Suppress("}")
_entry.set_parse_action(_mk_entry)

_entries = ZeroOrMore(_entry)
_entries.set_parse_action(_mk_list)
