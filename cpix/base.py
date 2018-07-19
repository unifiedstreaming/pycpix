"""
Base classes to be extended
"""
from abc import abstractmethod, ABC
from collections import MutableSequence
from lxml import etree


class CPIXComparableBase(ABC):
    def __str__(self):
        return str(etree.tostring(self.element()), "utf-8")

    def __lt__(self, other):
        return str(self).__lt__(str(other))

    def __le__(self, other):
        return str(self).__le__(str(other))

    def __gt__(self, other):
        return str(self).__gt__(str(other))

    def __ge__(self, other):
        return str(self).__ge__(str(other))

    def __eq__(self, other):
        return str(self).__eq__(str(other))

    def pretty_print(self, **kwargs):
        """
        Pretty print XML
        """
        if "pretty_print" not in kwargs:
            kwargs["pretty_print"] = True
        if "encoding" not in kwargs:
            kwargs["encoding"] = "utf-8"
        return etree.tostring(self.element(), **kwargs)

    # Abstract method element must be overriden
    @abstractmethod
    def element(self):
        pass


class CPIXListBase(MutableSequence, CPIXComparableBase):
    """Base list class to be extended"""

    def __init__(self, *args):
        self.list = list()
        self.extend(list(args))

    def __len__(self):
        return len(self.list)

    def __getitem__(self, index):
        return self.list[index]

    def __setitem__(self, index, value):
        self.check(value)
        self.list[index] = value

    def __delitem__(self, index):
        del self.list[index]

    def insert(self, index, value):
        self.check(value)
        self.list.insert(index, value)

    # Abstract method check must be overriden
    @abstractmethod
    def check(self, value):
        pass
