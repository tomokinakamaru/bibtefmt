from functools import cached_property
from itertools import chain


class Rule(object):
    def __init__(self, req=(), req_or=(), req_xor=(), opt=(), opt_xor=()):
        self.req = tuple(req)
        self.req_or = tuple(req_or)
        self.req_xor = tuple(req_xor)
        self.opt = tuple(opt)
        self.opt_xor = tuple(opt_xor)

    @cached_property
    def req_or_xor(self):
        return self.req_or + self.req_xor

    @cached_property
    def known(self):
        return self.known_req + self.known_opt

    @cached_property
    def known_req(self):
        return self.req + tuple(chain(self.req_or, self.req_xor))

    @cached_property
    def known_opt(self):
        return self.opt + tuple(chain(self.opt_xor))
