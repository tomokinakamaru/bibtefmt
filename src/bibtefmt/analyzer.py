# http://bib-it.sourceforge.net/help/fieldsAndEntryTypes.php#Fields

def analyze(dct):
    ws = []
    ws.extend(_find_unknown_types(dct))
    ws.extend(_find_duplicate_entries(dct))
    ws.extend(_find_duplicate_tags(dct))
    ws.extend(_find_ignored_tags(dct))
    ws.extend(_find_missing_or_conflicting_tags(dct))
    ws.extend(_find_optional_tags(dct))
    return ws


def _find_unknown_types(dct):
    known_keys = (
        'article', 'book', 'booklet', 'inbook', 'incollection',
        'inproceedings', 'manual', 'mastersthesis', 'misc', 'phdthesis',
        'proceedings', 'techreport', 'unpublished'
    )
    for key, typ in dct:
        if typ not in known_keys:
            yield f'unknown entry type "{typ}" for "{key}"'


def _find_duplicate_entries(dct):
    lst = [key for key, _ in dct]
    dup = set(e for e in lst if 1 < lst.count(e))
    for d in dup:
        yield f'duplicate entry "{d}"'


def _find_duplicate_tags(dct):
    for (key, _), tags in dct.items():
        lst = _get_names(tags)
        dup = set(e for e in lst if 1 < lst.count(e))
        for d in dup:
            yield f'duplicate tag "{d}" in "{key}"'


def _find_ignored_tags(dct):
    for (key, typ), tags in dct.items():
        if typ == 'article':
            yield from __find_ignored_tags(key, tags, (
                'author', 'title', 'journal', 'year', 'volume', 'number',
                'pages', 'month', 'note'
            ))
        elif typ == 'book':
            yield from __find_ignored_tags(key, tags, (
                'author', 'editor', 'title', 'publisher', 'year', 'volume',
                'number', 'series', 'address', 'edition', 'month', 'note'
            ))
        elif typ == 'booklet':
            yield from __find_ignored_tags(key, tags, (
                'title', 'author', 'howpublished', 'address', 'month', 'year',
                'note'
            ))
        elif typ == 'inbook':
            yield from __find_ignored_tags(key, tags, (
                'author', 'editor', 'title', 'chapter', 'pages', 'publisher',
                'year', 'volume', 'number', 'series', 'type', 'address',
                'edition', 'month', 'note'
            ))
        elif typ == 'incollection':
            yield from __find_ignored_tags(key, tags, (
                'author', 'title', 'booktitle', 'publisher', 'year', 'editor',
                'volume', 'number', 'series', 'type', 'chapter', 'pages',
                'address', 'edition', 'month', 'note'
            ))
        elif typ == 'inproceedings':
            yield from __find_ignored_tags(key, tags, (
                'author', 'title', 'booktitle', 'year', 'editor', 'volume',
                'number', 'series', 'pages', 'address', 'month',
                'organization', 'publisher', 'note'
            ))
        elif typ == 'manual':
            yield from __find_ignored_tags(key, tags, (
                'title', 'author', 'organization', 'address', 'edition',
                'month', 'year', 'note'
            ))
        elif typ == 'mastersthesis':
            yield from __find_ignored_tags(key, tags, (
                'author', 'title', 'school', 'year', 'type', 'address',
                'month', 'note'
            ))
        elif typ == 'misc':
            yield from __find_ignored_tags(key, tags, (
                'author', 'title', 'howpublished', 'month', 'year', 'note'
            ))
        elif typ == 'phdthesis':
            yield from __find_ignored_tags(key, tags, (
                'author', 'title', 'school', 'year', 'type', 'address',
                'month', 'note'
            ))
        elif typ == 'proceedings':
            yield from __find_ignored_tags(key, tags, (
                'title', 'year', 'editor', 'volume', 'number', 'series',
                'address', 'publisher', 'note', 'month', 'organization'
            ))
        elif typ == 'techreport':
            yield from __find_ignored_tags(key, tags, (
                'author', 'title', 'institution', 'year', 'type', 'number',
                'address', 'month', 'note'
            ))
        elif typ == 'unpublished':
            yield from __find_ignored_tags(key, tags, (
                'author', 'title', 'note', 'month', 'year'
            ))


def __find_ignored_tags(key, tags, valid_tags):
    ignores = set(_get_names(tags)) - set(valid_tags)
    for i in ignores:
        yield f'tag "{i}" in "{key}" may be ignored'


def _find_missing_or_conflicting_tags(dct):
    for (key, typ), tags in dct.items():
        if typ == 'article':
            yield from __find_missing_tags(key, tags, (
                'author', 'title', 'journal', 'year'
            ))

        if typ == 'book':
            yield from __find_missing_tags(key, tags, (
                 'title', 'publisher', 'year'
            ))
            names = set(_get_names(tags))
            if 'author' in names:
                if 'editor' in names:
                    yield f'conflicting tags "author" and "editor" in "{key}"'
            else:
                if 'editor' not in names:
                    yield f'missing tag "author" or "editor" in "{key}"'

        if typ == 'booklet':
            yield from __find_missing_tags(key, tags, (
                'title',
            ))

        if typ == 'inbook':
            yield from __find_missing_tags(key, tags, (
                'title', 'publisher', 'year'
            ))
            names = set(_get_names(tags))
            if 'author' in names:
                if 'editor' in names:
                    yield f'conflicting tags "author" and "editor" in "{key}"'
            else:
                if 'editor' not in names:
                    yield f'missing tag "author" or "editor" in "{key}"'

            if 'chapter' not in names and 'pages' not in names:
                yield f'missing tag "chapter" or "pages" in {key}'

        if typ == 'incollection':
            yield from __find_missing_tags(key, tags, (
                'author', 'title', 'booktitle', 'publisher', 'year'
            ))

        if typ == 'inproceedings':
            yield from __find_missing_tags(key, tags, (
                'author', 'title', 'booktitle', 'year'
            ))

        if typ == 'manual':
            yield from __find_missing_tags(key, tags, (
                'title',
            ))

        if typ == 'mastersthesis':
            yield from __find_missing_tags(key, tags, (
                'author', 'title', 'school', 'year'
            ))

        if typ == 'phdthesis':
            yield from __find_missing_tags(key, tags, (
                'author', 'title', 'school', 'year'
            ))

        if typ == 'proceedings':
            yield from __find_missing_tags(key, tags, (
                'title', 'year'
            ))

        if typ == 'techreport':
            yield from __find_missing_tags(key, tags, (
                'author', 'title', 'institution', 'year'
            ))

        if typ == 'unpublished':
            yield from __find_missing_tags(key, tags, (
                'author', 'title', 'note'
            ))


def __find_missing_tags(key, tags, required_tags):
    missing = set(required_tags) - set(_get_names(tags))
    for m in missing:
        yield f'missing tag "{m}" in "{key}"'


def _find_optional_tags(dct):
    for (key, typ), tags in dct.items():
        if typ == 'article':
            yield from __find_optional_tags(key, tags, (
                'volume', 'number', 'pages', 'month', 'note'
            ))
        elif typ == 'book':
            yield from __find_optional_tags(key, tags, (
                'volume', 'number', 'series', 'address', 'edition', 'month',
                'note'
            ))
        elif typ == 'booklet':
            yield from __find_optional_tags(key, tags, (
                'author', 'howpublished', 'address', 'month', 'year', 'note'
            ))
        elif typ == 'inbook':
            yield from __find_optional_tags(key, tags, (
                'volume', 'number', 'series', 'type', 'address', 'edition',
                'month', 'note'
            ))
        elif typ == 'incollection':
            yield from __find_optional_tags(key, tags, (
                'editor', 'volume', 'number', 'series', 'type', 'chapter',
                'pages', 'address', 'edition', 'month', 'note'
            ))
        elif typ == 'inproceedings':
            yield from __find_optional_tags(key, tags, (
                'editor', 'volume', 'number', 'series', 'pages', 'address',
                'month', 'organization', 'publisher', 'note'
            ))
        elif typ == 'manual':
            yield from __find_optional_tags(key, tags, (
                'author', 'organization', 'address', 'edition', 'month',
                'year', 'note'
            ))
        elif typ == 'mastersthesis':
            yield from __find_optional_tags(key, tags, (
                'type', 'address', 'month', 'note'
            ))
        elif typ == 'misc':
            yield from __find_optional_tags(key, tags, (
                'author', 'title', 'howpublished', 'month', 'year', 'note'
            ))
        elif typ == 'phdthesis':
            yield from __find_optional_tags(key, tags, (
                'type', 'address', 'month', 'note'
            ))
        elif typ == 'proceedings':
            yield from __find_optional_tags(key, tags, (
                'editor', 'volume', 'number', 'series', 'address', 'publisher',
                'note', 'month', 'organization'
            ))
        elif typ == 'techreport':
            yield from __find_optional_tags(key, tags, (
                'type', 'number', 'address', 'month', 'note'
            ))
        elif typ == 'unpublished':
            yield from __find_optional_tags(key, tags, (
                'author', 'title', 'note', 'month', 'year'
            ))


def __find_optional_tags(key, tags, valid_tags):
    ignores = set(_get_names(tags)) - set(valid_tags)
    for i in ignores:
        yield f'tag "{i}" in "{key}" can be removed'


def _get_names(tags):
    return [k for k, v in tags]
