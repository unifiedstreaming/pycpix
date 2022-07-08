"""
Content key classes
"""
from . import etree, uuid, b64decode, BinasciiError, NSMAP, PSKC, ENC, \
    CONTENT_KEY_WRAPPING_ALGORITHM
from .base import CPIXComparableBase, CPIXListBase


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
        if isinstance(xml, (str, bytes)):
            xml = etree.fromstring(xml)

        new_content_key_list = ContentKeyList()

        for element in xml.getchildren():
            tag = etree.QName(element.tag).localname
            if tag == "ContentKey":
                new_content_key_list.append(ContentKey.parse(element))

        return new_content_key_list


class ContentKey(CPIXComparableBase):
    """
    ContentKey element
    Has required attribute:
        kid: key ID
    And child element:
        Data: data element containing content encryption key
    """

    def __init__(self, kid, cek=None, common_encryption_scheme=None,
                 explicit_iv=None, value_mac=None):
        self._kid = None
        self._cek = None
        self._common_encryption_scheme = None
        self._explicit_iv = None
        self._value_mac = None
        self.kid = kid
        self.cek = cek
        self.common_encryption_scheme = common_encryption_scheme
        self.explicit_iv = explicit_iv
        self.value_mac = value_mac

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
        if cek is None:
            return
        if isinstance(cek, (str, bytes)):
            try:
                b64decode(cek)
            except BinasciiError:
                raise ValueError("cek is not a valid base64 string")
            self._cek = cek
        else:
            raise TypeError("cek should be a base64 string")

    @property
    def common_encryption_scheme(self):
        return self._common_encryption_scheme

    @common_encryption_scheme.setter
    def common_encryption_scheme(self, common_encryption_scheme):
        if common_encryption_scheme is None:
            common_encryption_scheme = "cenc"

        if isinstance(common_encryption_scheme, bytes):
            common_encryption_scheme = str(common_encryption_scheme)
        if isinstance(
            common_encryption_scheme, str
        ) and common_encryption_scheme in ["cenc", "cbc1", "cens", "cbcs"]:
            self._common_encryption_scheme = common_encryption_scheme
        else:
            raise TypeError(
                "common_encryption_scheme must be: cenc, cbc1, cens or cbcs"
            )

    @property
    def explicit_iv(self):
        return self._explicit_iv

    @explicit_iv.setter
    def explicit_iv(self, explicit_iv):
        if explicit_iv is None:
            return
        if isinstance(explicit_iv, (str, bytes)):
            try:
                b64decode(explicit_iv)
            except BinasciiError:
                raise ValueError("explicit_iv is not a valid base64 string")
            self._explicit_iv = explicit_iv
        else:
            raise TypeError("explicit_iv should be a base64 string")

    @property
    def value_mac(self):
        return self._value_mac

    @value_mac.setter
    def value_mac(self, value_mac):
        if value_mac is not None:
            if isinstance(value_mac, (str, bytes)):
                try:
                    b64decode(value_mac)
                except BinasciiError:
                    raise ValueError("value_mac is not a valid base64 string")
                self._value_mac = value_mac
            else:
                raise TypeError("value_mac should be a base64 str")
        else:
            self._value_mac = None

    def element(self):
        """Returns XML element"""
        el = etree.Element("ContentKey", nsmap=NSMAP)
        el.set("kid", str(self.kid))
        if self.common_encryption_scheme:
            el.set("commonEncryptionScheme", self.common_encryption_scheme)
        if self.explicit_iv:
            el.set("explicitIV", self.explicit_iv)
        if self.cek:
            data = etree.SubElement(el, "Data", nsmap=NSMAP)
            secret = etree.SubElement(
                data, "{{{pskc}}}Secret".format(pskc=PSKC), nsmap=NSMAP
            )
            # technically, MAC could be provided for plain value keys, but the
            # (cpix) spec states it's for cryptographic protection rather than
            # general authentication and that it is mandatory for encrypted
            # keys. in light of that, use setting of MAC to indicate that the
            # keys are encrypted.
            if self.value_mac is not None:
                ev = etree.SubElement(
                    secret,
                    "{{{pskc}}}EncryptedValue".format(pskc=PSKC),
                    nsmap=NSMAP
                )
                em = etree.SubElement(
                    ev,
                    "{{{enc}}}EncryptionMethod".format(enc=ENC),
                    nsmap=NSMAP
                )
                em.set("Algorithm", CONTENT_KEY_WRAPPING_ALGORITHM)
                cd = etree.SubElement(
                    ev, "{{{enc}}}CipherData".format(enc=ENC), nsmap=NSMAP
                )
                cv = etree.SubElement(
                    cd, "{{{enc}}}CipherValue".format(enc=ENC), nsmap=NSMAP
                )
                cv.text = self.cek
                vm = etree.SubElement(
                    secret, "{{{pskc}}}ValueMAC".format(pskc=PSKC), nsmap=NSMAP
                )
                vm.text = self.value_mac
            else:
                plain_value = etree.SubElement(
                    secret,
                    "{{{pskc}}}PlainValue".format(pskc=PSKC),
                    nsmap=NSMAP
                )
                plain_value.text = self.cek

        return el

    @staticmethod
    def parse(xml):
        """
        Parse XML and return ContentKey
        """
        if isinstance(xml, (str, bytes)):
            xml = etree.fromstring(xml)

        kid = xml.attrib["kid"]

        cek = None
        value_mac = None

        if xml.find(
            "**/{{{pskc}}}EncryptedValue".format(pskc=PSKC)
        ) is not None:
            cek = xml.find(
                ".//{{{enc}}}CipherValue".format(enc=ENC)
            ).text
            value_mac = xml.find(
                ".//{{{pskc}}}ValueMAC".format(pskc=PSKC)
            ).text
        else:
            cek_elem = xml.find("**/{{{pskc}}}PlainValue".format(pskc=PSKC))
            cek = cek_elem.text if cek_elem is not None else None

        common_encryption_scheme = None
        explicit_iv = None

        if "commonEncryptionScheme" in xml.attrib:
            common_encryption_scheme = xml.attrib["commonEncryptionScheme"]
        if "explicitIV" in xml.attrib:
            explicit_iv = xml.attrib["explicitIV"]

        return ContentKey(kid, cek, common_encryption_scheme, explicit_iv,
                          value_mac)
