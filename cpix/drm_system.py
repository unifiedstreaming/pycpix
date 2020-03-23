"""
DRM System classes
"""
from . import etree, uuid, b64decode, BinasciiError, VALID_SYSTEM_IDS
from .base import CPIXComparableBase, CPIXListBase


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
        if isinstance(xml, (str, bytes)):
            xml = etree.fromstring(xml)

        new_drm_system_list = DRMSystemList()

        for element in xml.getchildren():
            tag = etree.QName(element.tag).localname
            if tag == "DRMSystem":
                new_drm_system_list.append(DRMSystem.parse(element))

        return new_drm_system_list


class DRMSystem(CPIXComparableBase):
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

    def __init__(
        self,
        kid,
        system_id,
        pssh=None,
        content_protection_data=None,
        hls_signaling_data=None,
        hls_signaling_data_master=None,
    ):
        self._kid = None
        self._system_id = None
        self._pssh = None
        self._content_protection_data = None
        self._hls_signaling_data = None
        self._hls_signaling_data_master = None

        self.kid = kid
        self.system_id = system_id
        if pssh is not None:
            self.pssh = pssh
        if content_protection_data is not None:
            self.content_protection_data = content_protection_data
        if hls_signaling_data is not None:
            self.hls_signaling_data = hls_signaling_data
        if hls_signaling_data_master is not None:
            self.hls_signaling_data_master = hls_signaling_data_master

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
        if isinstance(pssh, (str, bytes)):
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
                raise ValueError(
                    "content_protection_data is not a valid base64 string"
                )
            self._content_protection_data = content_protection_data
        else:
            raise TypeError("content_protection_data must be a base64 string")

    @property
    def hls_signaling_data(self):
        return self._hls_signaling_data

    @hls_signaling_data.setter
    def hls_signaling_data(self, hls_signaling_data):
        if isinstance(hls_signaling_data, (str, bytes)):
            try:
                b64decode(hls_signaling_data)
            except BinasciiError:
                raise ValueError(
                    "hls_signaling_data is not a valid base64 string"
                )
            self._hls_signaling_data = hls_signaling_data
        else:
            raise TypeError("hls_signaling_data should be a base64 string")

    @property
    def hls_signaling_data_master(self):
        return self._hls_signaling_data_master

    @hls_signaling_data_master.setter
    def hls_signaling_data_master(self, hls_signaling_data_master):
        if isinstance(hls_signaling_data_master, (str, bytes)):
            try:
                b64decode(hls_signaling_data_master)
            except BinasciiError:
                raise ValueError(
                    "hls_signaling_data_master is not a valid base64 string"
                )
            self._hls_signaling_data_master = hls_signaling_data_master
        else:
            raise TypeError(
                "hls_signaling_data_master should be a base64 string"
            )

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
            hls_element.set("playlist", "media")
            hls_element.text = self.hls_signaling_data
            el.append(hls_element)
        if self.hls_signaling_data_master is not None:
            hls_element = etree.Element("HLSSignalingData")
            hls_element.set("playlist", "master")
            hls_element.text = self.hls_signaling_data_master
            el.append(hls_element)
        return el

    @staticmethod
    def parse(xml):
        """
        Parse XML and return DRMSystem
        """
        if isinstance(xml, (str, bytes)):
            xml = etree.fromstring(xml)

        kid = xml.attrib["kid"]
        system_id = xml.attrib["systemId"]

        pssh = None
        content_protection_data = None
        hls_signaling_data = None
        hls_signaling_data_master = None

        if xml.find("{*}PSSH") is not None:
            pssh = xml.find("{*}PSSH").text
        if xml.find("{*}ContentProtectionData") is not None:
            content_protection_data = xml.find("{*}ContentProtectionData").text
        for element in xml.findall("{*}HLSSignalingData"):
            if (
                "playlist" not in element.attrib
                or element.attrib["playlist"] == "media"
                or element.attrib["playlist"] == "variant"
            ):
                hls_signaling_data = element.text
            elif (
                "playlist" in element.attrib
                and element.attrib["playlist"] == "master"
            ):
                hls_signaling_data_master = element.text

        return DRMSystem(
            kid,
            system_id,
            pssh,
            content_protection_data,
            hls_signaling_data,
            hls_signaling_data_master,
        )
