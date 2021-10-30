# REF: http://www.bibtex.org/Format/
from pyparsing import alphas
from pyparsing import delimited_list
from pyparsing import CharsNotIn
from pyparsing import Forward
from pyparsing import Optional
from pyparsing import QuotedString
from pyparsing import Suppress
from pyparsing import White
from pyparsing import Word
from pyparsing import ZeroOrMore
from .ast import BracedText
from .ast import BracedTextElements
from .ast import Entries
from .ast import Entry
from .ast import EntryBody
from .ast import EntryKey
from .ast import EntryType
from .ast import NonbracedText
from .ast import QuotedText
from .ast import Tag
from .ast import TagName
from .ast import Tags
from .ast import TagValue
from .ast import TagValueElements
from .plug import create_rec
from .plug import create1
from .plug import create2

spaces = Suppress(Optional(White()))

nonbraced_text = CharsNotIn('{}')
nonbraced_text.set_parse_action(create1(NonbracedText))

braced_text = Forward()
braced_text_elems = Forward()

braced_text << Suppress('{') + braced_text_elems + Suppress('}')
braced_text.set_parse_action(create1(BracedText))

braced_text_elems << ZeroOrMore(nonbraced_text | braced_text)
braced_text_elems.set_parse_action(create_rec(BracedTextElements))

quoted_text = QuotedString('"', escChar='\\', unquoteResults=False)
quoted_text.set_parse_action(create1(QuotedText))

entry_key = spaces + CharsNotIn('#\\@,={} \t\n') + spaces
entry_key.set_parse_action(create1(EntryKey))

tag_value_elems = delimited_list(braced_text | quoted_text | entry_key, '#')
tag_value_elems.set_parse_action(create_rec(TagValueElements))

tag_value = tag_value_elems
tag_value.set_parse_action(create1(TagValue))

tag_name = spaces + CharsNotIn('#\\@,={} \t\n') + spaces
tag_name.set_parse_action(create1(TagName))

tag = tag_name + Suppress('=') + tag_value
tag.set_parse_action(create2(Tag))

tags = delimited_list(tag, ',', allow_trailing_delim=True)
tags.set_parse_action(create_rec(Tags))

entry_body = entry_key + Optional(Suppress(',') + Optional(tags))
entry_body.set_parse_action(create2(EntryBody))

entry_type = Suppress('@') + Word(alphas)
entry_type.set_parse_action(create1(EntryType))

entry = entry_type + Suppress('{') + Optional(entry_body) + Suppress('}')
entry.set_parse_action(create2(Entry))

entries = ZeroOrMore(entry)
entries.set_parse_action(create_rec(Entries))
