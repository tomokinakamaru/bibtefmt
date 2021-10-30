from textwrap import indent


def format(entries):
    blocks = []
    for type, (key, tags) in sorted(entries):
        body = indent(format_tags(tags), '  ')
        blocks.append(f'@{type}{{{key},\n{body}\n}}')
    return '\n\n'.join(blocks)


def format_tags(tags):
    width = max(len(name) for name, _ in tags)
    return ',\n'.join(format_tag(name, val, width) for name, val in tags)


def format_tag(name, val, width):
    return f'{name.ljust(width)} = {val}'
