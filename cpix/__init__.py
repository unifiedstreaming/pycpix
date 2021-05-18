"""
CPIX stuff
"""
import uuid
from lxml import etree
from base64 import b64decode
from binascii import Error as BinasciiError
import pkg_resources
import sys


CPIX_SCHEMA_DOC = pkg_resources.resource_stream("cpix", "schema/cpix.xsd")
CPIX_SCHEMA = etree.XMLSchema(etree.parse(CPIX_SCHEMA_DOC))

PLAYREADY_SYSTEM_ID = uuid.UUID("9a04f079-9840-4286-ab92-e65be0885f95")
WIDEVINE_SYSTEM_ID = uuid.UUID("edef8ba9-79d6-4ace-a3c8-27dcd51d21ed")

VALID_SYSTEM_IDS = [
    uuid.UUID("1077efec-c0b2-4d02-ace3-3c1e52e2fb4b"),  # org.w3.clearkey
    PLAYREADY_SYSTEM_ID,  # Microsoft Playready
    uuid.UUID("F239E769-EFA3-4850-9C16-A903C6932EFB"),  # Adobe Primetime DRM
    uuid.UUID("5E629AF5-38DA-4063-8977-97FFBD9902D4"),  # Marlin
    uuid.UUID("9a27dd82-fde2-4725-8cbc-4234aa06ec09"),  # Verimatrix
    WIDEVINE_SYSTEM_ID,  # Widevine
    uuid.UUID("80a6be7e-1448-4c37-9e70-d5aebe04c8d2"),  # Irdeto
    uuid.UUID("279fe473-512c-48fe-ade8-d176fee6b40f"),  # Latens
    uuid.UUID("B4413586-C58C-FFB0-94A5-D4896C1AF6C3"),  # Viaccess-Orca DRM
    uuid.UUID("94CE86FB-07FF-4F43-ADB8-93D2FA968CA2"),  # Apple FairPlay
    uuid.UUID("81376844-F976-481E-A84E-CC25D39B0B33"),  # AES-128
    uuid.UUID("3D5E6D35-9B9A-41E8-B843-DD3C6E72C42C"),  # ChinaDRM
]
PSKC = "urn:ietf:params:xml:ns:keyprov:pskc"
XSI = "http://www.w3.org/2001/XMLSchema-instance"
NSMAP = {
    None: "urn:dashif:org:cpix",
    "xsi": XSI,
    "pskc": PSKC}


def parse(xml):
    """
    Parse function, does an initial read to figure out the root element then
    attempts to call the relevant parser
    """
    if isinstance(xml, (str, bytes)):
        xml = etree.fromstring(xml)
    if not isinstance(xml, etree._Element):
        raise TypeError("not valid xml")

    tag = etree.QName(xml).localname

    return getattr(sys.modules[__name__], tag).parse(xml)


def validate(xml):
    """
    Validate a CPIX XML against the schema

    Returns a tuple of valid true/false and if false the error(s)
    """
    if isinstance(xml, (str, bytes)):
        xml = etree.fromstring(xml)
    if not isinstance(xml, etree._Element):
        raise TypeError("not valid xml")

    try:
        CPIX_SCHEMA.assertValid(xml)
    except etree.DocumentInvalid as e:
        return (False, e)
    return (True, "")


from .content_key import ContentKey, ContentKeyList
from .drm_system import DRMSystem, DRMSystemList
from .filters import AudioFilter, BitrateFilter, VideoFilter, KeyPeriodFilter,\
    LabelFilter
from .usage_rule import UsageRule, UsageRuleList, AudioUsageRule, \
    VideoUsageRule, SDVideoUsageRule, HDVideoUsageRule, UHD1VideoUsageRule, \
    UHD2VideoUsageRule
from .period import Period, PeriodList
from .cpix import CPIX
