# http://bib-it.sourceforge.net/help/fieldsAndEntryTypes.php
from .rule import Rule

address = 'address'

author = 'author'

booktitle = 'booktitle'

chapter = 'chapter'

edition = 'edition'

editor = 'editor'

howpublished = 'howpublished'

institution = 'institution'

journal = 'journal'

month = 'month'

note = 'note'

number = 'number'

organization = 'organization'

pages = 'pages'

publisher = 'publisher'

school = 'school'

series = 'series'

title = 'title'

type = 'type'

volume = 'volume'

year = 'year'

article = Rule(
    req=[author, title, journal, year],
    opt=[volume, number, pages, month, note]
)

book = Rule(
    req=[title, publisher, year],
    req_xor=[(author, editor)],
    opt=[series, address, edition, month, note],
    opt_xor=[(volume, number)]
)

booklet = Rule(
    req=[title],
    opt=[author, howpublished, address, month, year, note]
)

inbook = Rule(
    req=[title, publisher, year],
    req_or=[(chapter, pages)],
    req_xor=[(author, editor)],
    opt=[series, type, address, edition, month, note],
    opt_xor=[(volume, number)]
)

incollection = Rule(
    req=[author, title, booktitle, publisher, year],
    opt=[editor, series, type, chapter, pages, address, edition, month, note],
    opt_xor=[(volume, number)]
)

inproceedings = Rule(
    req=[author, title, booktitle, year],
    opt=[editor, series, pages, address, month, organization, publisher, note],
    opt_xor=[(volume, number)]
)

manual = Rule(
    req=[title],
    opt=[author, organization, address, edition, month, year, note]
)

mastersthesis = Rule(
    req=[author, title, school, year],
    opt=[type, address, month, note]
)

misc = Rule(
    opt=[author, title, howpublished, month, year, note]
)

phdthesis = Rule(
    req=[author, title, school, year],
    opt=[type, address, month, note]
)

proceedings = Rule(
    req=[title, year],
    opt=[editor, series, address, publisher, note, month, organization],
    opt_xor=[(volume, number)]
)

techreport = Rule(
    req=[author, title, institution, year],
    opt=[type, number, address, month, note]
)

unpublished = Rule(
    req=[author, title, note],
    opt=[month, year]
)

rules = dict(
    article=article, book=book, booklet=booklet, inbook=inbook,
    incollection=incollection, inproceedings=inproceedings, manual=manual,
    mastersthesis=mastersthesis, misc=misc, phdthesis=phdthesis,
    proceedings=proceedings, techreport=techreport, unpublished=unpublished
)
