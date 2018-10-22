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

    def __repr__(self):
        props = {p: repr(getattr(self, p)) for p in dir(type(self))
                 if isinstance(getattr(type(self), p), property)}

        return "{name}({prop})".format(
            name=type(self).__name__,
            prop=", ".join(["{k}={v}".format(k=k, v=v)
                            for k, v in props.items()])
        )

    def pretty_print(self, **kwargs):
        """
        Pretty print XML
        """
        if "pretty_print" not in kwargs:
            kwargs["pretty_print"] = True
        if "encoding" not in kwargs:
            kwargs["encoding"] = "utf-8"
        return etree.tostring(self.element(), **kwargs)

    # Abstract methods element and parse must be overriden
    @abstractmethod
    def element(self):
        pass

    @abstractmethod
    def parse(self):
        pass


class CPIXListBase(MutableSequence, CPIXComparableBase):
    """Base list class to be extended"""

    def __init__(self, *args, **kwargs):
        self._list = list()
        self.list = list()
        if len(args) == 1 and len(kwargs) == 0 and isinstance(args[0], list):
            self.extend(args[0])
        elif (len(args) == 0 and len(kwargs) == 1 and
                "list" in kwargs and
                isinstance(kwargs["list"], list)):
            self.extend(kwargs["list"])
        else:
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

    @property
    def list(self):
        return self._list

    @list.setter
    def list(self, l):
        if not isinstance(l, list):
            raise TypeError("must be a list")
        elif all([self.check(x) for x in l]):
            self._list = l

    # Abstract method check must be overriden
    @abstractmethod
    def check(self, value):
        pass
