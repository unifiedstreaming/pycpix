"""
CPIX stuff
"""
import uuid
from lxml import etree
from base64 import b64decode
from binascii import Error as BinasciiError
from collections import MutableSequence
from abc import abstractmethod


VALID_SYSTEM_IDS = [
    uuid.UUID("1077efec-c0b2-4d02-ace3-3c1e52e2fb4b"),  # org.w3.clearkey
    uuid.UUID("9a04f079-9840-4286-ab92-e65be0885f95"),  # Microsoft Playready
    uuid.UUID("F239E769-EFA3-4850-9C16-A903C6932EFB"),  # Adobe Primetime DRM, version 4
    uuid.UUID("5E629AF5-38DA-4063-8977-97FFBD9902D4"),  # Marlin
    uuid.UUID("9a27dd82-fde2-4725-8cbc-4234aa06ec09"),  # Verimatrix
    uuid.UUID("edef8ba9-79d6-4ace-a3c8-27dcd51d21ed"),  # Widevine
    uuid.UUID("80a6be7e-1448-4c37-9e70-d5aebe04c8d2"),  # Irdeto
    uuid.UUID("279fe473-512c-48fe-ade8-d176fee6b40f"),  # Latens
    uuid.UUID("B4413586-C58C-FFB0-94A5-D4896C1AF6C3"),  # Viaccess-Orca DRM (VODRM)
    uuid.UUID("94CE86FB-07FF-4F43-ADB8-93D2FA968CA2"),  # Apple FairPlay
]
PSKC = "urn:ietf:params:xml:ns:keyprov:pskc"
XSI = "http://www.w3.org/2001/XMLSchema-instance"
NSMAP = {
    None: "urn:dashif:org:cpix",
    "xsi": XSI,
    "pskc": PSKC}

def encode_bool(value):
    """Encode booleans to produce valid XML"""
    if value:
        return "true"
    return "false"


class CPIX(object):
    def __init__(self, content_keys=None, drm_systems=None, usage_rules=None):
        self._content_keys = None
        self._drm_systems = None
        self._usage_rules = None

        if content_keys is not None:
            self.content_keys = content_keys
        if drm_systems is not None:
            self.drm_systems = drm_systems
        if usage_rules is not None:
            self.usage_rules = usage_rules
        
    @property
    def content_keys(self):
        return self._content_keys
    
    @content_keys.setter
    def content_keys(self, content_keys):
        if isinstance(content_keys, ContentKeyList):
            self._content_keys = content_keys
        else:
            raise TypeError("content_keys should be a ContentKeyList")

    @property
    def drm_systems(self):
        return self._drm_systems

    @drm_systems.setter
    def drm_systems(self, drm_systems):
        if isinstance(drm_systems, DRMSystemList):
            self._drm_systems = drm_systems
        else:
            raise TypeError("drm_systems should be a DRMSystemList")

    @property
    def usage_rules(self):
        return self._usage_rules

    @usage_rules.setter
    def usage_rules(self, usage_rules):
        if isinstance(usage_rules, UsageRuleList):
            self._usage_rules = usage_rules
        else:
            raise TypeError("usage_rules should be a UsageRuleList")

    def __str__(self):
        return str(etree.tostring(self.element()), "utf-8")

    def element(self):
        el = etree.Element("CPIX", nsmap=NSMAP)
        el.set("{{{xsi}}}schemaLocation".format(
            xsi=XSI), "urn:dashif:org:cpix cpix.xsd")
        if self.content_keys is not None and isinstance(self.content_keys, ContentKeyList):
            el.append(self.content_keys.element())
        if self.drm_systems is not None and isinstance(self.drm_systems, DRMSystemList):
            el.append(self.drm_systems.element())
        if self.usage_rules is not None and isinstance(self.usage_rules, UsageRuleList):
            el.append(self.usage_rules.element())
        return el

    @staticmethod
    def parse(xml):
        """
        Parse a CPIX xml
        """
        new_cpix = CPIX()
        parsed_xml = etree.fromstring(xml)
        new_cpix.parsed_xml = parsed_xml

        for element in parsed_xml.getchildren():
            tag = etree.QName(element.tag).localname

            if tag == "ContentKeyList":
                new_cpix.content_keys = ContentKeyList.parse(element)
            if tag == "DRMSystemList":
                new_cpix.drm_systems = DRMSystemList.parse(element)
            if tag == "ContentKeyUsageRuleList":
                new_cpix.usage_rules = UsageRuleList.parse(element)
        
        return new_cpix


class CPIXListBase(MutableSequence):
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

    def __str__(self):
        return str(etree.tostring(self.element()), "utf-8")

    # Abstract methods check and element must be overriden 
    @abstractmethod
    def check(self, value):
        pass
    
    @abstractmethod
    def element(self):
        pass


class ContentKeyList(CPIXListBase):
    """List of ContentKeys"""
    def check(self, value):
        if not isinstance(value, ContentKey):
            raise TypeError("{} is not a ContentKey".format(value))

    def element(self):
        el = etree.Element("ContentKeyList", nsmap=NSMAP)
        for content_key in self:
            el.append(content_key.element())
        return el

    @staticmethod
    def parse(xml):
        """
        Parse and return new ContentKeyList
        """
        new_content_key_list = ContentKeyList()

        for element in xml.getchildren():
            tag = etree.QName(element.tag).localname
            if tag == "ContentKey":
                new_content_key_list.append(ContentKey.parse(element))

        return new_content_key_list


class ContentKey(object):
    """
    ContentKey element
    Has required attribute:
        kid: key ID
    And child element:
        Data: data element containing content encryption key
    """
    def __init__(self, kid, cek):
        self._kid = None
        self._cek = None
        self.kid = kid
        self.cek = cek
    
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

    @property
    def cek(self):
        return self._cek
    
    @cek.setter
    def cek(self, cek):
        if isinstance(cek, (str, bytes)):   
            try:
                b64decode(cek)
            except BinasciiError:
                raise ValueError("cek is not a valid base64 string")
            self._cek = cek
        else:
            raise TypeError("cek should be a base64 string")

    def __str__(self):
        return str(etree.tostring(self.element()), "utf-8")

    def element(self):
        """Returns XML element"""
        el = etree.Element("ContentKey", nsmap=NSMAP)
        el.set("kid", str(self.kid))
        data = etree.SubElement(el, "Data", nsmap=NSMAP)
        secret = etree.SubElement(
            data, "{{{pskc}}}Secret".format(pskc=PSKC), nsmap=NSMAP)
        plain_value = etree.SubElement(
            secret, "{{{pskc}}}PlainValue".format(pskc=PSKC), nsmap=NSMAP)
        plain_value.text = self.cek
        return el

    @staticmethod
    def parse(xml):
        """
        Parse XML and return ContentKey
        """
        kid = xml.attrib["kid"]
        cek = xml.find("**/{{{pskc}}}PlainValue".format(pskc=PSKC)).text

        return ContentKey(kid, cek)
        

class DRMSystemList(CPIXListBase):
    """List of DRMSystems"""
    def check(self, value):
        if not isinstance(value, DRMSystem):
            raise TypeError("{} is not a DRMSystem".format(value))

    def element(self):
        el = etree.Element("DRMSystemList")
        for drm_system in self:
            el.append(drm_system.element())
        return el

    @staticmethod
    def parse(xml):
        """
        Parse and return new DRMSystemList
        """
        new_drm_system_list = DRMSystemList()

        for element in xml.getchildren():
            tag = etree.QName(element.tag).localname
            if tag == "DRMSystem":
                new_drm_system_list.append(DRMSystem.parse(element))

        return new_drm_system_list

class DRMSystem(object):
    """
    DRMSystem element
    Has required attributes:
        kid: key ID
        systemId: DRM system ID
    And optional child elements depending on context (all are base64 encoded):
        PSSH: PSSH box for insertion in ISOBMFF output
        ContentProtectionData: ContentProtection XML for DASH manifest
        HLSSignalingData: signaling information for HLS manifest
    """
    def __init__(self, kid, system_id, pssh=None,
                 content_protection_data=None, hls_signaling_data=None):
        self._kid = None
        self._system_id = None
        self._pssh = None
        self._content_protection_data = None
        self._hls_signaling_data = None

        self.kid = kid
        self.system_id = system_id
        if pssh is not None:
            self.pssh = pssh
        if content_protection_data is not None:
            self.content_protection_data = content_protection_data
        if hls_signaling_data is not None:
            self.hls_signaling_data = hls_signaling_data

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

    @property
    def system_id(self):
        return self._system_id

    @system_id.setter
    def system_id(self, system_id):
        tmp_system_id = None
        if isinstance(system_id, str):
            tmp_system_id = uuid.UUID(system_id)
        elif isinstance(system_id, uuid.UUID):
            tmp_system_id = system_id
        else:
            raise TypeError("system_id should be a uuid")
        
        if tmp_system_id in VALID_SYSTEM_IDS:
            self._system_id = tmp_system_id
        else:
            raise ValueError("system_id is unknown")

    @property
    def pssh(self):
        return self._pssh
    
    @pssh.setter
    def pssh(self, pssh):
        if isinstance(pssh, str):
            try:
                b64decode(pssh)
            except BinasciiError:
                raise ValueError("pssh is not a valid base64 string")
            self._pssh = pssh
        else:
            raise TypeError("pssh should be a base64 string")

    @property
    def content_protection_data(self):
        return self._content_protection_data

    @content_protection_data.setter
    def content_protection_data(self, content_protection_data):
        if isinstance(content_protection_data, str):
            try:
                b64decode(content_protection_data)
            except BinasciiError:
                raise ValueError("content_protection_data is not a valid base64 string")
            self._content_protection_data = content_protection_data
        else:
            raise TypeError("content_protection_data should be a base64 string")
    
    @property
    def hls_signaling_data(self):
        return self._hls_signaling_data

    @hls_signaling_data.setter
    def hls_signaling_data(self, hls_signaling_data):
        if isinstance(hls_signaling_data, str):
            try:
                b64decode(hls_signaling_data)
            except BinasciiError:
                raise ValueError(
                    "hls_signaling_data is not a valid base64 string")
            self._hls_signaling_data = hls_signaling_data
        else:
            raise TypeError(
                "hls_signaling_data should be a base64 string")

    def __str__(self):
        return str(etree.tostring(self.element()), "utf-8")

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
        if self.hls_signaling_data is not None:
            hls_element = etree.Element("HLSSignalingData")
            hls_element.text = self.hls_signaling_data
            el.append(hls_element)
        return el

    @staticmethod
    def parse(xml):
        """
        Parse XML and return DRMSystem
        """
        kid = xml.attrib["kid"]
        system_id = xml.attrib["systemId"]

        pssh = None
        content_protection_data = None
        hls_signaling_data = None

        if xml.find("PSSH"):
            pssh = xml.find("PSSH").text
        if xml.find("ContentProtectionData"):
            content_protection_data = xml.find("ContentProtectionData").text
        if xml.find("HLSSignalingData"):
            hls_signaling_data = xml.find("HLSSignalingData").text

        return DRMSystem(kid, system_id, pssh, content_protection_data, hls_signaling_data)


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
        KeyPeriodFilter: time based filters for key rotation (not currently supported by USP)
        LabelFilter: label based filters (not currently supported by USP)
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
        if not isinstance(value, (PeriodFilter, LabelFilter, AudioFilter, VideoFilter, BitrateFilter)):
            raise TypeError(
                "{} is not filter (PeriodFilter, LabelFilter, AudioFilter, VideoFilter, BitrateFilter)".format(value))

    def __eq__(self, other):
        if not isinstance(other, UsageRule):
            return False
        if self.kid != other.kid or len(self) != len(other):
            return False
        # sort filter lists based on their xml strings
        self.list.sort(key=lambda x:str(x))
        other.list.sort(key=lambda x:str(x))
        for i in range(len(self)):
            if self[i] != other[i]:
                return False
        return True     

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

            if tag in ["PeriodFilter", "LabelFilter", "VideoFilter", "AudioFilter", "BitrateFilter"]:
                filter = globals()[tag].parse(element)
                new_usage_rule.append(filter)

        return new_usage_rule


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
    
    def __str__(self):
        return str(etree.tostring(self.element()), "utf-8")
    
    def __eq__(self, other):
        if not isinstance(other, VideoFilter):
            return False
        if (self.min_pixels != other.min_pixels
            or self.max_pixels != other.max_pixels
            or self.max_pixels != other.max_pixels
            or self.hdr != other.hdr
            or self.wcg != other.wcg
            or self.max_fps != other.max_fps
            or self.max_fps != other.max_fps):
                return False
        else:
            return True

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
        min_pixels=None
        max_pixels=None
        hdr=None
        wcg=None
        min_fps=None
        max_fps=None

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

    def __str__(self):
        return str(etree.tostring(self.element()), "utf-8")

    def __eq__(self, other):
        if not isinstance(other, AudioFilter):
            return False
        if (self.min_channels != other.min_channels
            or self.max_channels != other.max_channels):
                return False
        else:
            return True

    def element(self):
        """Returns XML element"""
        el = etree.Element("AudioFilter")
        if self.min_channels:
            el.set("minChannels", self.min_channels)
        if self.max_channels:
            el.set("maxChannels", self.max_channels)
        return el

    @staticmethod
    def parse(xml):
        """
        Parse XML and return AudioFilter
        """
        min_channels = None
        max_channels = None

        if "minChannels" in xml.attrib:
            min_channels = xml.attrib["minChannels"]
        if "maxChannels" in xml.attrib:
            max_channels = xml.attrib["maxChannels"]

        return AudioFilter(min_channels, max_channels)


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

    def __str__(self):
        return str(etree.tostring(self.element()), "utf-8")

    def __eq__(self, other):
        if not isinstance(other, BitrateFilter):
            return False
        if (self.min_bitrate != other.min_bitrate
            or self.max_bitrate != other.max_bitrate):
                return False
        else:
            return True

    def element(self):
        """Returns XML element"""
        el = etree.Element("BitrateFilter")
        if self.min_bitrate:
            el.set("minBitrate", self.min_bitrate)
        if self.max_bitrate:
            el.set("maxBitrate", self.max_bitrate)
        return el

    @staticmethod
    def parse(xml):
        """
        Parse XML and return BitrateFilter
        """
        min_bitrate = None
        max_bitrate = None

        if "minBitrate" in xml.attrib:
            min_bitrate = xml.attrib["minBitrate"]
        if "maxBitrate" in xml.attrib:
            max_bitrate = xml.attrib["maxBitrate"]

        return BitrateFilter(min_bitrate, max_bitrate)
