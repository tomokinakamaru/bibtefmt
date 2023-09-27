from bibtefmt import bibtex, printer


def test_empty():
    assert _test("") == ""


def test_one_entry():
    assert _test("@foo{}") == "@foo{}"


def test_two_entries():
    assert _test("@foo{}@bar{}") == "@foo{}\n\n@bar{}"


def test_key_only():
    assert _test("@foo{bar}") == "@foo{bar}"


def test_one_tag():
    assert _test("@foo{bar,baz=1}") == "@foo{bar,\n  baz = 1\n}"


def test_two_tags():
    assert _test("@foo{bar,baz=1,quxx=2}") == "@foo{bar,\n  baz  = 1,\n  quxx = 2\n}"


def test_concat():
    assert _test("@foo{bar,baz=1 # 2}") == "@foo{bar,\n  baz = 1 # 2\n}"


def _test(text):
    return printer.print(bibtex.parse(text))
