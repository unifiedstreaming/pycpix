"""
Content key classes
"""
from . import etree, NSMAP
from .base import CPIXComparableBase, CPIXListBase
from datetime import datetime
from isodate import datetime_isoformat, parse_datetime


class PeriodList(CPIXListBase):
    """List of Periods"""

    def check(self, value):
        if not isinstance(value, Period):
            raise TypeError("{} is not a Period".format(value))

    def element(self):
        el = etree.Element("ContentKeyPeriodList", nsmap=NSMAP)
        for period in self:
            el.append(period.element())
        return el

    @staticmethod
    def parse(xml):
        """
        Parse and return new PeriodList
        """
        if isinstance(xml, (str, bytes)):
            xml = etree.fromstring(xml)

        new_period_list = PeriodList()

        for element in xml.getchildren():
            tag = etree.QName(element.tag).localname
            if tag == "ContentKeyPeriod":
                new_period_list.append(Period.parse(element))

        return new_period_list


class Period(CPIXComparableBase):
    """
    Period element
    Has required attribute:
        id: key ID
    And either:
        index: integer index for the key period
    Or both:
        start: datetime for start of period, either wallclock or media time
        end: datetime for end of period, either wallclock or media time

    index is mutually exclusive with start and end, which are mutually
    inclusive
    """

    def __init__(self, id, index=None, start=None, end=None):
        self._id = None
        self._index = None
        self._start = None
        self._end = None

        self.id = id
        self.index = index
        self.start = start
        self.end = end

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, id):
        if isinstance(id, str):
            self._id = id
        else:
            raise TypeError("id should be a string")

    @property
    def index(self):
        return self._index

    @index.setter
    def index(self, index):
        if index is not None:
            if self.start is not None or self.end is not None:
                raise ValueError(
                    "index is mutually exclusive with start and end")
            if isinstance(index, int):
                self._index = index
            else:
                raise TypeError("index should be a int")

    @property
    def start(self):
        return self._start

    @start.setter
    def start(self, start):
        if start is not None:
            if self.index is not None:
                raise ValueError("start is mutually exclusive with index")
            if isinstance(start, datetime):
                self._start = start
            else:
                # if not passed a datetime, try to parse it
                try:
                    self._start = parse_datetime(start)
                except Exception:
                    raise TypeError("start should be a datetime")

    @property
    def end(self):
        return self._end

    @end.setter
    def end(self, end):
        if end is not None:
            if self.index is not None:
                raise ValueError("end is mutually exclusive with index")
            if isinstance(end, datetime):
                self._end = end
            else:
                # if not passed a datetime, try to parse it
                try:
                    self._end = parse_datetime(end)
                except Exception:
                    raise TypeError("end should be a datetime")

    def element(self):
        """Returns XML element"""
        el = etree.Element("ContentKeyPeriod", nsmap=NSMAP)
        el.set("id", str(self.id))
        if self.index is not None:
            el.set("index", str(self.index))
        if self.start is not None:
            el.set("start", datetime_isoformat(self.start))
        if self.end is not None:
            el.set("end", datetime_isoformat(self.end))
        return el

    @staticmethod
    def parse(xml):
        """
        Parse XML and return Period
        """
        if isinstance(xml, (str, bytes)):
            xml = etree.fromstring(xml)

        id = xml.attrib["id"]

        if "index" in xml.attrib:
            index = xml.attrib["index"]
        else:
            index = None
        if "start" in xml.attrib:
            start = xml.attrib["start"]
        else:
            start = None
        if "end" in xml.attrib:
            end = xml.attrib["end"]
        else:
            end = None

        return Period(
            id=id,
            index=index,
            start=start,
            end=end
        )
