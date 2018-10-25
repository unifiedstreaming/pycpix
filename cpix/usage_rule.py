"""
Usage rule classes
"""
from . import etree, uuid
from .base import CPIXListBase
from . import AudioFilter, BitrateFilter, VideoFilter, KeyPeriodFilter, \
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
        if isinstance(xml, (str, bytes)):
            xml = etree.fromstring(xml)

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
        if not isinstance(value, (KeyPeriodFilter, LabelFilter, AudioFilter,
                                  VideoFilter, BitrateFilter)):
            raise TypeError(
                "{} is not filter (KeyPeriodFilter, LabelFilter, AudioFilter, "
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
        if isinstance(xml, (str, bytes)):
            xml = etree.fromstring(xml)

        kid = xml.attrib["kid"]
        new_usage_rule = UsageRule(kid)

        for element in xml.getchildren():
            tag = etree.QName(element.tag).localname

            if tag in ["KeyPeriodFilter", "LabelFilter", "VideoFilter",
                       "AudioFilter", "BitrateFilter"]:
                filter = globals()[tag].parse(element)
                new_usage_rule.append(filter)

        return new_usage_rule


class AudioUsageRule(UsageRule):
    """
    Default usage rule for audio, with a single AudioFilter with no parameters
    """
    def __init__(self, kid):
        super().__init__(
            kid=kid,
            filters=[AudioFilter()])


class VideoUsageRule(UsageRule):
    """
    Default usage rule for vide, with a single VideoFilter with no parameters
    """

    def __init__(self, kid):
        super().__init__(
            kid=kid,
            filters=[VideoFilter()])


class SDVideoUsageRule(UsageRule):
    """
    Default usage rule for SD Video
    VideoFilter maxPixels <= 768 * 576
    """

    def __init__(self, kid):
        super().__init__(
            kid=kid,
            filters=[VideoFilter(max_pixels=442368)])


class HDVideoUsageRule(UsageRule):
    """
    Default usage rule for HD Video
    VideoFilter
        minPixels > 768 * 576
        maxPixels <= 1920 * 1080
    """

    def __init__(self, kid):
        super().__init__(
            kid=kid,
            filters=[VideoFilter(
                min_pixels=442369,
                max_pixels=2073600)])


class UHD1VideoUsageRule(UsageRule):
    """
    Default usage rule for UHD1 / 4K Video
    VideoFilter
        minPixels > 1920 * 1080
        maxPixels <= 4096 * 2160
    """

    def __init__(self, kid):
        super().__init__(
            kid=kid,
            filters=[VideoFilter(
                min_pixels=2073601,
                max_pixels=8847360)])


class UHD2VideoUsageRule(UsageRule):
    """
    Default usage rule for UHD2 / 8K Video
    VideoFilter
        minPixels > 4096 * 2160
    """

    def __init__(self, kid):
        super().__init__(
            kid=kid,
            filters=[VideoFilter(min_pixels=8847361)])
