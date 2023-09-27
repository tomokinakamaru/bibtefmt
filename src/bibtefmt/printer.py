def print(entries):
    return "\n\n".join(_print(entries))


def _print(entries):
    for typ, key, tags in entries:
        k = f"{key}" if key else ""
        t = _print_tags(tags)
        s = "," if t else ""
        yield f"@{typ}{{{k}{s}{t}}}"


def _print_tags(tags):
    w = max((len(n) for n, _ in tags), default=0)
    s = ",\n".join(_print_tag(n, v, w) for n, v in tags)
    return f"\n{s}\n" if s else ""


def _print_tag(name, val, width):
    val = " # ".join(val)
    return f"  {name.ljust(width)} = {val}"
