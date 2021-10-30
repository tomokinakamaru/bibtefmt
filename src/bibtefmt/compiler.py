def compile(ast):
    return Compiler().compile(ast)


class Compiler(object):
    def compile(self, node):
        if node:
            name = node.__class__.__name__
            compile = getattr(self, f'compile_{name}')
            return compile(node)
        return node

    def compile_Entries(self, entries):
        head, tail = self._map(entries.head, entries.tail)
        return (head,) + (tail or ())

    def compile_Entry(self, entry):
        type, body = self._map(entry.type, entry.body)
        return type, (body or (None, ()))

    def compile_EntryType(self, entry_type):
        return entry_type.name.lower()

    def compile_EntryBody(self, entry_body):
        key, tags = self._map(entry_body.key, entry_body.tags)
        return key, (tags or ())

    def compile_EntryKey(self, entry_key):
        return entry_key.name

    def compile_Tags(self, tags):
        head, tail = self._map(tags.head, tags.tail)
        return (head,) + (tail or ())

    def compile_Tag(self, tag):
        name, value = self._map(tag.name, tag.value)
        return name, value

    def compile_TagName(self, tag_name):
        return tag_name.value.lower()

    def compile_TagValue(self, tag_value):
        elems, = self._map(tag_value.elems)
        return elems

    def compile_TagValueElements(self, tag_value_elems):
        head, tail = self._map(tag_value_elems.head, tag_value_elems.tail)
        return f'{head} # {tail}' if tail else head

    def compile_NonbracedText(self, nonbraced_text):
        return nonbraced_text.value

    def compile_QuotedText(self, quoted_text):
        return quoted_text.value

    def compile_BracedText(self, braced_text):
        elems, = self._map(braced_text.elems)
        return f'{{{elems}}}'

    def compile_BracedTextElements(self, braced_text_elems):
        head, tail = self._map(braced_text_elems.head, braced_text_elems.tail)
        return f'{head}{tail or ""}'

    def _map(self, *args):
        return tuple(map(self.compile, args))
