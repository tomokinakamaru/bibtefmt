import pyparsing as pp


def parse(text):
    dct = {}
    for typ, key, tags in entries.parseString(text, parseAll=True)[0]:
        k = key, typ
        dct.setdefault(k, set())
        dct[k].update(tags)
    return dct


braced = pp.Forward()
braced << '{' + pp.ZeroOrMore(pp.CharsNotIn('{}') | braced) + '}'
braced.setParseAction(lambda pr: ''.join(pr))

quoted = pp.QuotedString('"', escChar='\\', unquoteResults=False)
quoted.setParseAction(lambda pr: pr[0])

optwhite = pp.Suppress(pp.Optional(pp.White()))

key = optwhite + pp.CharsNotIn('#\\@,={} \t\n') + optwhite
key.setParseAction(lambda pr: pr[0].lower())

name = optwhite + pp.CharsNotIn('#\\@,={} \t\n') + optwhite
name.setParseAction(lambda pr: pr[0].lower())

value = pp.delimitedList(braced | quoted | key, '#')
value.setParseAction(lambda pr: ' # '.join(pr))

tag = name + pp.Suppress('=') + value
tag.setParseAction(lambda pr: tuple(pr))

tags = pp.delimitedList(tag, ',') + pp.Suppress(pp.Optional(','))
tags.setParseAction(lambda pr: tuple(pr))

body = key + pp.Optional(pp.Suppress(',') + pp.Optional(tags))
body.setParseAction(lambda pr: (pr[0], ()) if len(pr) == 1 else tuple(pr))

etype = pp.Word('@', pp.alphas)
etype.setParseAction(lambda pr: pr[0][1:].lower())

entry = etype + pp.Suppress('{') + body + pp.Suppress('}')
entry.setParseAction(lambda pr: (pr[0], pr[1][0], pr[1][1]))

entries = pp.ZeroOrMore(entry)
entries.setParseAction(lambda pr: tuple(pr))
