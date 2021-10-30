class Node(object):
    pass


class Node0(Node):
    def __init__(self, value):
        self.__value = value

    @property
    def _value(self):
        return self.__value

    @_value.setter
    def _value(self, value):
        self.__value = value


class Node1(Node):
    def __init__(self, child):
        self.__child = child

    @property
    def _child(self):
        return self.__child

    @_child.setter
    def _child(self, node):
        self.__child = node


class Node2(Node):
    def __init__(self, left, right):
        self.__left = left
        self.__right = right

    @property
    def _left(self):
        return self.__left

    @_left.setter
    def _left(self, node):
        self.__left = node

    @property
    def _right(self):
        return self.__right

    @_right.setter
    def _right(self, node):
        self.__right = node
