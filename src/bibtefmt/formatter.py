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
    val = format_val(val)
    return f'{name.ljust(width)} = {val}'


def format_val(val):
    val = val.replace('\n', ' ')
    val = ' '.join(val.split())
    if val.startswith(('{ ', '" ')):
        val = val[0] + val[2:]
    if val.endswith((' }', ' "')):
        val = val[:-2] + val[-1]
    return val
