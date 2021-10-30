from .node import Node0
from .node import Node1
from .node import Node2


class Entries(Node2):
    head = Node2._left
    tail = Node2._right


class Entry(Node2):
    type = Node2._left
    body = Node2._right


class EntryType(Node0):
    name = Node0._value


class EntryBody(Node2):
    key = Node2._left
    tags = Node2._right


class EntryKey(Node0):
    name = Node0._value


class Tags(Node2):
    head = Node2._left
    tail = Node2._right


class Tag(Node2):
    name = Node2._left
    value = Node2._right


class TagName(Node0):
    value = Node0._value


class TagValue(Node1):
    elems = Node1._child


class TagValueElements(Node2):
    head = Node2._left
    tail = Node2._right


class NonbracedText(Node0):
    value = Node0._value


class QuotedText(Node0):
    value = Node0._value


class BracedText(Node1):
    elems = Node1._child


class BracedTextElements(Node2):
    head = Node2._left
    tail = Node2._right
