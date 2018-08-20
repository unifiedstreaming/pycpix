"""
Filter classes
"""
from . import etree
from .base import CPIXComparableBase


def encode_bool(value):
    """Encode booleans to produce valid XML"""
    if value:
        return "true"
    return "false"


class KeyPeriodFilter(CPIXComparableBase):
    """
    KeyPeriodFilter element
    Has single required attribute:
        periodId
    """

    def __init__(self, period_id):
        self.period_id = period_id

    def element(self):
        """Returns XML element"""
        el = etree.Element("KeyPeriodFilter")
        el.set("periodId", str(self.period_id))
        return el

    @staticmethod
    def parse(xml):
        """
        Parse XML and return KeyPeriodFilter
        """
        if isinstance(xml, (str, bytes)):
            xml = etree.fromstring(xml)

        period_id = xml.attrib["periodId"]

        return KeyPeriodFilter(period_id)


class LabelFilter(CPIXComparableBase):
    """
    LabelFilter element
    Not yet implemented
    """


class VideoFilter(CPIXComparableBase):
    """
    VideoFilter element
    Has optional attributes:
        minPixels
        maxPixels
        hdr
        wcg
        minFps
        maxFps
    """

    def __init__(self, min_pixels=None, max_pixels=None, hdr=None, wcg=None,
                 min_fps=None, max_fps=None):
        self.min_pixels = min_pixels
        self.max_pixels = max_pixels
        self.hdr = hdr
        self.wcg = wcg
        self.min_fps = min_fps
        self.max_fps = max_fps

    def element(self):
        """Returns XML element"""
        el = etree.Element("VideoFilter")
        if self.min_pixels is not None:
            el.set("minPixels", str(self.min_pixels))
        if self.max_pixels is not None:
            el.set("maxPixels", str(self.max_pixels))
        if self.hdr is not None:
            el.set("hdr", encode_bool(self.hdr))
        if self.wcg is not None:
            el.set("wcg", encode_bool(self.wcg))
        if self.min_fps is not None:
            el.set("minFps", str(self.min_fps))
        if self.max_fps is not None:
            el.set("maxFps", str(self.max_fps))
        return el

    @staticmethod
    def parse(xml):
        """
        Parse XML and return VideoFilter
        """
        if isinstance(xml, (str, bytes)):
            xml = etree.fromstring(xml)

        min_pixels = None
        max_pixels = None
        hdr = None
        wcg = None
        min_fps = None
        max_fps = None

        if "minPixels" in xml.attrib:
            min_pixels = xml.attrib["minPixels"]
        if "maxPixels" in xml.attrib:
            max_pixels = xml.attrib["maxPixels"]
        if "hdr" in xml.attrib:
            hdr = xml.attrib["hdr"]
        if "wcg" in xml.attrib:
            wcg = xml.attrib["wcg"]
        if "minFps" in xml.attrib:
            min_fps = xml.attrib["minFps"]
        if "maxFps" in xml.attrib:
            max_fps = xml.attrib["maxFps"]

        return VideoFilter(min_pixels, max_pixels, hdr, wcg, min_fps, max_fps)


class AudioFilter(CPIXComparableBase):
    """
    AudioFilter element
    Has optional attributes:
        minChannels
        maxChannels
    """

    def __init__(self, min_channels=None, max_channels=None):
        self.min_channels = min_channels
        self.max_channels = max_channels

    def element(self):
        """Returns XML element"""
        el = etree.Element("AudioFilter")
        if self.min_channels:
            el.set("minChannels", str(self.min_channels))
        if self.max_channels:
            el.set("maxChannels", str(self.max_channels))
        return el

    @staticmethod
    def parse(xml):
        """
        Parse XML and return AudioFilter
        """
        if isinstance(xml, (str, bytes)):
            xml = etree.fromstring(xml)

        min_channels = None
        max_channels = None

        if "minChannels" in xml.attrib:
            min_channels = xml.attrib["minChannels"]
        if "maxChannels" in xml.attrib:
            max_channels = xml.attrib["maxChannels"]

        return AudioFilter(min_channels, max_channels)


class BitrateFilter(CPIXComparableBase):
    """
    BitrateFilter element
    Has optional attributes:
        minBitrate
        maxBitrate
    """

    def __init__(self, min_bitrate=None, max_bitrate=None):
        self.min_bitrate = min_bitrate
        self.max_bitrate = max_bitrate

    def element(self):
        """Returns XML element"""
        el = etree.Element("BitrateFilter")
        if self.min_bitrate:
            el.set("minBitrate", str(self.min_bitrate))
        if self.max_bitrate:
            el.set("maxBitrate", str(self.max_bitrate))
        return el

    @staticmethod
    def parse(xml):
        """
        Parse XML and return BitrateFilter
        """
        if isinstance(xml, (str, bytes)):
            xml = etree.fromstring(xml)

        min_bitrate = None
        max_bitrate = None

        if "minBitrate" in xml.attrib:
            min_bitrate = xml.attrib["minBitrate"]
        if "maxBitrate" in xml.attrib:
            max_bitrate = xml.attrib["maxBitrate"]

        return BitrateFilter(min_bitrate, max_bitrate)
