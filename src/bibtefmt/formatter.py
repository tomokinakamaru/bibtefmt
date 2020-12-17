import textwrap
from . import analyzer
from . import parser


def format(text):
    entries = parser.parse(text)
    warnings = analyzer.analyze(entries)
    blocks = []
    for (key, typ), tags in sorted(entries.items()):
        body = textwrap.indent(format_tags(tags), ' ' * 2)
        blocks.append(f'@{typ}{{{key},\n{body}\n}}')

    return '\n\n'.join(blocks), '\n'.join(warnings)


def format_tags(tags):
    lng = max(len(name) for name, _ in tags)
    lines = []
    for name, val in sorted(tags):
        lines.append(f'{name.ljust(lng)} = {val}')
    return ',\n'.join(lines)
