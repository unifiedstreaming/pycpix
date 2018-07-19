"""
Usage rule classes
"""
from . import etree, uuid
from .base import CPIXListBase
from . import AudioFilter, BitrateFilter, VideoFilter, PeriodFilter, \
    LabelFilter


class UsageRuleList(CPIXListBase):
    """List of UsageRules"""

    def check(self, value):
        if not isinstance(value, UsageRule):
            raise TypeError("{} is not a UsageRule".format(value))

    def element(self):
        el = etree.Element("ContentKeyUsageRuleList")
        for usage_rule in self:
            el.append(usage_rule.element())
        return el

    @staticmethod
    def parse(xml):
        """
        Parse and return new UsageRuleList
        """
        new_usage_rule_list = UsageRuleList()

        for element in xml.getchildren():
            tag = etree.QName(element.tag).localname

            if tag == "ContentKeyUsageRule":
                usage_rule = UsageRule.parse(element)
                new_usage_rule_list.append(usage_rule)

        return new_usage_rule_list


class UsageRule(CPIXListBase):
    """
    ContentKeyUsageRule element
    Has required attributes:
        kid: key ID to which this rule applies
    And optional child elements:
        KeyPeriodFilter: not currently supported
        LabelFilter: not currently supported
        VideoFilter: video based filters
        AudioFilter: audio based filters
        BitrateFilter: bitrate based filters
    """

    def __init__(self, kid, filters=[]):
        self.list = list()
        self.extend(list(filters))
        self._kid = None

        self.kid = kid

    @property
    def kid(self):
        return self._kid

    @kid.setter
    def kid(self, kid):
        if isinstance(kid, str):
            self._kid = uuid.UUID(kid)
        elif isinstance(kid, uuid.UUID):
            self._kid = kid
        else:
            raise TypeError("kid should be a uuid")

    def check(self, value):
        if not isinstance(value, (PeriodFilter, LabelFilter, AudioFilter,
                                  VideoFilter, BitrateFilter)):
            raise TypeError(
                "{} is not filter (PeriodFilter, LabelFilter, AudioFilter, "
                "VideoFilter, BitrateFilter)".format(value))

    def element(self):
        """Returns XML element"""
        el = etree.Element("ContentKeyUsageRule")
        if self.kid is not None:
            el.set("kid", str(self.kid))
        for filter in self:
            el.append(filter.element())
        return el

    @staticmethod
    def parse(xml):
        """
        Parse and return a UsageRule
        """
        kid = xml.attrib["kid"]
        new_usage_rule = UsageRule(kid)

        for element in xml.getchildren():
            tag = etree.QName(element.tag).localname

            if tag in ["PeriodFilter", "LabelFilter", "VideoFilter",
                       "AudioFilter", "BitrateFilter"]:
                filter = globals()[tag].parse(element)
                new_usage_rule.append(filter)

        return new_usage_rule
