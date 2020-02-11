import textwrap
from . import parser


def format(text):
    dct = {}
    for typ, key, tags in parser.parse(text):
        k = key, typ
        dct.setdefault(k, set())
        dct[k].update(tags)

    blocks = []
    for (key, typ), tags in sorted(dct.items()):
        body = textwrap.indent(format_tags(tags), ' ' * 2)
        blocks.append(f'@{typ}{{{key},\n{body}\n}}')

    return '\n\n'.join(blocks)


def format_tags(tags):
    lng = max(len(name) for name, _ in tags)
    lines = []
    for name, val in sorted(tags):
        lines.append(f'{name.ljust(lng)} = {val}')
    return ',\n'.join(lines)
