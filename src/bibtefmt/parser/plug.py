def create1(cls):
    def _(toks):
        t = _read(toks)
        return cls(t)
    return _


def create2(cls):
    def _(toks):
        t1 = _read(toks)
        t2 = _read(toks)
        return cls(t1, t2)
    return _


def create_rec(cls):
    return _create_rec(cls, VOID)


def _create_rec(cls, none):
    def _(toks):
        if len(toks) == 0:
            return none
        t = _read(toks)
        f = _create_rec(cls, None)
        return cls(t, f(toks))
    return _


def _read(toks):
    if len(toks) == 0:
        return None
    t = toks.pop(0)
    return None if t is VOID else t


VOID = object()
