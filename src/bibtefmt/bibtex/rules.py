# http://bib-it.sourceforge.net/help/fieldsAndEntryTypes.php
from functools import cached_property
from itertools import chain


class _Rule(object):
    def __init__(
        self,
        req=(),
        req_or=(),
        req_xor=(),
        opt=(),
        opt_xor=(),
    ):
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
        return self.req + tuple(chain(*self.req_or, *self.req_xor))

    @cached_property
    def known_opt(self):
        return self.opt + tuple(chain(*self.opt_xor))


_address = "address"

_author = "author"

_booktitle = "booktitle"

_chapter = "chapter"

_edition = "edition"

_editor = "editor"

_howpublished = "howpublished"

_institution = "institution"

_journal = "journal"

_month = "month"

_note = "note"

_number = "number"

_organization = "organization"

_pages = "pages"

_publisher = "publisher"

_school = "school"

_series = "series"

_title = "title"

_type = "type"

_volume = "volume"

_year = "year"

_article = _Rule(
    req=[_author, _title, _journal, _year],
    opt=[_volume, _number, _pages, _month, _note],
)

_book = _Rule(
    req=[_title, _publisher, _year],
    req_xor=[(_author, _editor)],
    opt=[_series, _address, _edition, _month, _note],
    opt_xor=[(_volume, _number)],
)

_booklet = _Rule(
    req=[_title],
    opt=[_author, _howpublished, _address, _month, _year, _note],
)

_inbook = _Rule(
    req=[_title, _publisher, _year],
    req_or=[(_chapter, _pages)],
    req_xor=[(_author, _editor)],
    opt=[_series, _type, _address, _edition, _month, _note],
    opt_xor=[(_volume, _number)],
)

_incollection = _Rule(
    req=[_author, _title, _booktitle, _publisher, _year],
    opt=[_editor, _series, _type, _chapter, _pages, _address, _edition, _month, _note],
    opt_xor=[(_volume, _number)],
)

_inproceedings = _Rule(
    req=[_author, _title, _booktitle, _year],
    opt=[_editor, _series, _pages, _address, _month, _organization, _publisher, _note],
    opt_xor=[(_volume, _number)],
)

_manual = _Rule(
    req=[_title],
    opt=[_author, _organization, _address, _edition, _month, _year, _note],
)

_mastersthesis = _Rule(
    req=[_author, _title, _school, _year],
    opt=[_type, _address, _month, _note],
)

_misc = _Rule(
    opt=[_author, _title, _howpublished, _month, _year, _note],
)

_phdthesis = _Rule(
    req=[_author, _title, _school, _year],
    opt=[_type, _address, _month, _note],
)

_proceedings = _Rule(
    req=[_title, _year],
    opt=[_editor, _series, _address, _publisher, _note, _month, _organization],
    opt_xor=[(_volume, _number)],
)

_techreport = _Rule(
    req=[_author, _title, _institution, _year],
    opt=[_type, _number, _address, _month, _note],
)

_unpublished = _Rule(
    req=[_author, _title, _note],
    opt=[_month, _year],
)

rules = dict(
    article=_article,
    book=_book,
    booklet=_booklet,
    inbook=_inbook,
    incollection=_incollection,
    inproceedings=_inproceedings,
    manual=_manual,
    mastersthesis=_mastersthesis,
    misc=_misc,
    phdthesis=_phdthesis,
    proceedings=_proceedings,
    techreport=_techreport,
    unpublished=_unpublished,
)
