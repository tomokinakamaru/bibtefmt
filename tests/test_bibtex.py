# REF: http://www.bibtex.org/Format/
from bibtefmt import bibtex


def test_empty():
    assert bibtex.parse("") == []


def test_one_entry():
    assert bibtex.parse("@foo{}") == [
        ["foo", None, []],
    ]


def test_two_entries():
    assert bibtex.parse("@foo{} @bar{}") == [
        ["foo", None, []],
        ["bar", None, []],
    ]


def test_key_only():
    assert bibtex.parse("@foo{bar}") == [
        ["foo", "bar", []],
    ]


def test_one_tag():
    assert bibtex.parse("@foo{bar,baz=1}") == [
        ["foo", "bar", [["baz", ["1"]]]],
    ]


def test_two_tags():
    assert bibtex.parse("@foo{bar,baz=1,qux=2}") == [
        ["foo", "bar", [["baz", ["1"]], ["qux", ["2"]]]],
    ]


def test_braced():
    assert bibtex.parse("@foo{bar,baz={1}}") == [
        ["foo", "bar", [["baz", ["{1}"]]]],
    ]


def test_braced_nest():
    assert bibtex.parse("@foo{bar,baz={1 {2} 3}}") == [
        ["foo", "bar", [["baz", ["{1 {2} 3}"]]]],
    ]


def test_quoted():
    assert bibtex.parse('@foo{bar,baz="1"}') == [
        ["foo", "bar", [["baz", ['"1"']]]],
    ]


def test_concat():
    assert bibtex.parse("@foo{bar,baz=1#2}") == [
        ["foo", "bar", [["baz", ["1", "2"]]]],
    ]
