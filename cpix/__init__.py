"""
CPIX stuff
"""
import uuid
from lxml import etree


VALID_SYSTEM_IDS = [
    uuid.UUID("edef8ba9-79d6-4ace-a3c8-27dcd51d21ed"),  # widevine
]

def encode_bool(value):
    """Encode booleans to produce valid XML"""
    if value:
        return "true"
    return "false"


class CPIX(object):
    def __init__(self, cpix=None):
        if cpix:
            # do some magic to create object from existing CPIX
            pass
        # set up empty structure
        self.usage_rules = {}
        self.content_keys = {}
        self.drm_systems = {}



class ContentKey(object):
    """
    ContentKey element
    Has required attribute:
        kid: key ID
    And child element:
        Data: data element containing content encryption key
    """
    def __init__(self, kid=None, cek=None):
        self.kid = kid
        self.cek = cek
    

class DRMSystem(object):
    """
    DRMSystem element
    Has required attributes:
        kid: key ID
        systemId: DRM system ID
    And optional child elements depending on context (all are base64 encoded):
        PSSH: PSSH box for insertion in ISOBMFF output
        ContentProtectionData: ContentProtection XML for DASH manifest
        HLSSignalingData: Signalling information for HLS manifest
    """
    def __init__(self, kid, system_id=None, pssh=None,
                 content_protection_data=None, hls_signalling_data=None):
        if kid is not None and not isinstance(kid, (str, uuid.UUID)):
            raise TypeError("kid should be a uuid")
        self.kid = uuid.UUID(kid)
        if system_id is not None and not isinstance(system_id, (str, uuid.UUID)):
            raise TypeError("system_id should be a uuid")
        if system_id is not None and uuid.UUID(system_id) not in VALID_SYSTEM_IDS:
            raise ValueError("system_id is unknown")
        self.system_id=uuid.UUID(system_id)
        if pssh is not None and not isinstance(pssh, str):
            raise TypeError("pssh should be a string")
        self.pssh = pssh
        if content_protection_data is not None and not isinstance(content_protection_data, str):
            raise TypeError("content_protection_data should be a string")
        self.content_protection_data = content_protection_data
        if hls_signalling_data is not None and not isinstance(hls_signalling_data, str):
            raise TypeError("hls_signalling_data should be a string")
        self.hls_signalling_data = hls_signalling_data

    def element(self):
        """Returns XML element"""
        el = etree.Element("DRMSystem")
        if self.kid is not None:
            el.set("kid", str(self.kid))
        if self.system_id is not None:
            el.set("systemId", str(self.system_id))
        if self.pssh is not None:
            pssh_element = etree.Element("PSSH")
            pssh_element.text = self.pssh
            el.append(pssh_element)
        if self.content_protection_data is not None:
            cpd_element = etree.Element("ContentProtectionData")
            cpd_element.text = self.content_protection_data
            el.append(cpd_element)
        if self.hls_signalling_data is not None:
            hls_element = etree.Element("HLSSignallingData")
            hls_element.text = self.hls_signalling_data
            el.append(hls_element)
        return el


class UsageRule(object):
    """
    ContentKeyUsageRule element
    Has required attributes:
        kid: key ID to which this rule applies
    And optional child elements:
        KeyPeriodFilter: time based filters for key rotation (not currently supported by USP)
        LabelFilter: label based filters (not currently supported by USP)
        VideoFilter: video based filters
        AudioFilter: audio based filters
        BitrateFilter: bitrate based filters
    """
    def __init__(self, kid, filters=[]):
        if kid is not None and not isinstance(kid, str):
            raise TypeError("kid should be a string")
        self.kid = kid

        if filters is not None and not isinstance(filters, list) and not all(isinstance(x, (PeriodFilter, LabelFilter, AudioFilter, VideoFilter, BitrateFilter)) for x in filters):
            raise TypeError(
                "filters should be a list of filters (PeriodFilter, LabelFilter, AudioFilter, VideoFilter, BitrateFilter)")
        self.filters = filters

    def element(self):
        """Returns XML element"""
        el = etree.Element("ContentKeyUsageRuleType")
        if self.kid is not None:
            el.set("kid", str(self.kid))
        for filter in self.filters:
            el.append(filter.element())
        return el


class PeriodFilter(object):
    """
    PeriodFilter element
    Not yet implemented
    """


class LabelFilter(object):
    """
    LabelFilter element
    Not yet implemented
    """


class VideoFilter(object):
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


class AudioFilter(object):
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
            el.set("minChannels", self.min_channels)
        if self.max_channels:
            el.set("maxChannels", self.max_channels)
        return el


class BitrateFilter(object):
    """
    BitrateFilter element
    Has optional attributes:
        minBitrate
        maxBitrate
    """
    def __init__(self, min_bitrate=None, max_bitrate=None):
        self.min_bitrate = min_bitrate
        self.max_bitrate = max_bitrate
