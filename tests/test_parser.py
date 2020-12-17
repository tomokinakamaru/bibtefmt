import pytest
from pyparsing import ParseException
from bibtefmt import parser as p


def test_braced():
    _test_success(p.braced, '{foo}', ['{foo}'])
    _test_success(p.braced, '{{foo}}', ['{{foo}}'])
    _test_success(p.braced, '{{foo} bar}', ['{{foo} bar}'])
    _test_fail(p.braced, '{{}')


def test_quoted():
    _test_success(p.quoted, '"foo"', ['"foo"'])
    _test_success(p.quoted, '"\\""', ['"\\""'])
    _test_fail(p.quoted, '"""')


def test_key():
    _test_success(p.key, 'foo', ['foo'])
    _test_fail(p.key, 'foo bar')
    _test_fail(p.key, 'foo,')


def test_name():
    _test_success(p.name, 'foo', ['foo'])
    _test_fail(p.name, 'foo{}')
    _test_fail(p.name, 'foo=')


def test_value():
    _test_success(p.value, '"foo" # {bar}', ['"foo" # {bar}'])
    _test_success(p.value, 'foo # bar', ['foo # bar'])
    _test_fail(p.value, 'foo bar')


def test_tag():
    _test_success(p.tag, 'foo={bar}', [
        ('foo', '{bar}')
    ])
    _test_fail(p.tag, 'foo {bar}')


def test_tags():
    _test_success(p.tags, 'foo={bar}, baz="qux"', [
        (('foo', '{bar}'), ('baz', '"qux"'))
    ])
    _test_success(p.tags, 'foo={bar}, baz="qux",', [
        (('foo', '{bar}'), ('baz', '"qux"'))
    ])
    _test_fail(p.tags, 'foo={bar}, {baz}=qux')


def test_body():
    _test_success(p.body, 'foo', [
        ('foo', ())
    ])
    _test_success(p.body, 'foo,bar={baz}', [
        ('foo', (('bar', '{baz}'),))
    ])


def test_etype():
    _test_success(p.etype, '@ARTICLE', ['article'])


def test_entry():
    _test_success(p.entry, '@article{foo,}', [
        ('article', 'foo', ())
    ])


def test_entries():
    _test_success(p.entries, '@article{foo}', [
        (('article', 'foo', ()),)
    ])


def test_parser():
    r = p.parse('@article{foo}')
    assert r == {('foo', 'article'): set()}


def _test_success(parser, text, expected):
    pr = parser.parseString(text, parseAll=True)
    assert list(pr) == expected


def _test_fail(parser, text):
    with pytest.raises(ParseException):
        parser.parseString(text, parseAll=True)
