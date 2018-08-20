"""
Content key classes
"""
from . import etree, uuid, b64decode, BinasciiError, NSMAP, PSKC
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
        if isinstance(xml, (str, bytes)):
            xml = etree.fromstring(xml)

        kid = xml.attrib["kid"]
        cek = xml.find("**/{{{pskc}}}PlainValue".format(pskc=PSKC)).text

        return ContentKey(kid, cek)
