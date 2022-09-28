"""
Delivery Data classes
"""
from . import etree, b64decode, BinasciiError, NSMAP, DS, PSKC, ENC, \
    CONTENT_KEY_WRAPPING_ALGORITHM, DOCUMENT_KEY_WRAPPING_ALGORITHM, \
    ENCRYPTED_KEY_MAC_ALGORITHM
from .base import CPIXComparableBase, CPIXListBase


class DeliveryDataList(CPIXListBase):
    """List of DeliveryDatas"""

    def check(self, value):
        if not isinstance(value, DeliveryData):
            raise TypeError("{} is not a DeliveryData".format(value))

    def element(self):
        el = etree.Element("DeliveryDataList", nsmap=NSMAP)
        for delivery_data in self:
            el.append(delivery_data.element())
        return el

    @staticmethod
    def parse(xml):
        """
        Parse and return new DeliveryDataList
        """
        if isinstance(xml, (str, bytes)):
            xml = etree.fromstring(xml)

        new_delivery_data_list = DeliveryDataList()

        for element in xml.getchildren():
            tag = etree.QName(element.tag).localname
            if tag == "DeliveryData":
                new_delivery_data_list.append(DeliveryData.parse(element))

        return new_delivery_data_list


class DeliveryKey():
    """
    DeliveryKey element
    Has child elements:
        X509Data: contains a X509 Certificate
    """
    def __init__(self, certificate):
        self._certificate = None

        self.certificate = certificate

    @property
    def certificate(self):
        return self._certificate

    @certificate.setter
    def certificate(self, certificate):
        if isinstance(certificate, (str, bytes)):
            try:
                b64decode(certificate)
            except BinasciiError:
                raise ValueError("certificate is not a valid base64 string")
            self._certificate = certificate
        else:
            raise TypeError("certificate should be a base64 string")

    def element(self):
        """Returns XML element"""
        dk = etree.Element("DeliveryKey", nsmap=NSMAP)
        data = etree.SubElement(
            dk, "{{{ds}}}X509Data".format(ds=DS), nsmap=NSMAP
        )
        cert = etree.SubElement(
            data, "{{{ds}}}X509Certificate".format(ds=DS), nsmap=NSMAP
        )
        cert.text = self.certificate

        return dk

    @staticmethod
    def parse(xml):
        """
        Parse XML and return DeliveryKey
        """
        if isinstance(xml, (str, bytes)):
            xml = etree.fromstring(xml)

        cert = xml.find(".//{{{ds}}}X509Certificate".format(ds=DS)).text

        return DeliveryKey(cert)


class DocumentKey():
    """
    DocumentKey element
    Has child elements:
        Data: contains the encrypted document Key
    """
    def __init__(self, cipher_value):
        self._cipher_value = None

        self.cipher_value = cipher_value

    @property
    def cipher_value(self):
        return self._cipher_value

    @cipher_value.setter
    def cipher_value(self, cipher_value):
        if isinstance(cipher_value, (str, bytes)):
            try:
                b64decode(cipher_value)
            except BinasciiError:
                raise ValueError("cipher_value is not a valid base64 string")
            self._cipher_value = cipher_value
        else:
            raise TypeError("cipher_value should be a base64 string")

    def element(self):
        """Returns XML element"""
        dk = etree.Element("DocumentKey", nsmap=NSMAP)
        dk.set("Algorithm", CONTENT_KEY_WRAPPING_ALGORITHM)

        data = etree.SubElement(
            dk, "Data", nsmap=NSMAP
        )
        secret = etree.SubElement(
            data, "{{{pskc}}}Secret".format(pskc=PSKC), nsmap=NSMAP
        )
        ev = etree.SubElement(
            secret, "{{{pskc}}}EncryptedValue".format(pskc=PSKC), nsmap=NSMAP
        )
        em = etree.SubElement(
            ev, "{{{enc}}}EncryptionMethod".format(enc=ENC), nsmap=NSMAP
        )
        em.set("Algorithm", DOCUMENT_KEY_WRAPPING_ALGORITHM)
        cd = etree.SubElement(
            ev, "{{{enc}}}CipherData".format(enc=ENC), nsmap=NSMAP
        )
        cv = etree.SubElement(
            cd, "{{{enc}}}CipherValue".format(enc=ENC), nsmap=NSMAP
        )
        cv.text = self.cipher_value

        return dk

    @staticmethod
    def parse(xml):
        """
        Parse XML and return DocumentKey
        """
        if isinstance(xml, (str, bytes)):
            xml = etree.fromstring(xml)

        cipher_value = xml.find(
            ".//{{{enc}}}CipherValue".format(enc=ENC)).text

        return DocumentKey(cipher_value)


class MACMethod():
    """
    MACMethod element
    Has child elements:
        Key: contains encrypted MAC Key
    """
    def __init__(self, cipher_value):
        self._cipher_value = None
        self.cipher_value = cipher_value

    @property
    def cipher_value(self):
        return self._cipher_value

    @cipher_value.setter
    def cipher_value(self, cipher_value):
        if isinstance(cipher_value, (str, bytes)):
            try:
                b64decode(cipher_value)
            except BinasciiError:
                raise ValueError("cipher_value is not a valid base64 string")
            self._cipher_value = cipher_value
        else:
            raise TypeError("cipher_value should be a base64 string")

    def element(self):
        """Returns XML element"""
        dk = etree.Element("MACMethod", nsmap=NSMAP)
        dk.set("Algorithm", ENCRYPTED_KEY_MAC_ALGORITHM)

        key = etree.SubElement(
            dk, "Key", nsmap=NSMAP
        )
        em = etree.SubElement(
            key, "{{{enc}}}EncryptionMethod".format(enc=ENC), nsmap=NSMAP
        )
        em.set("Algorithm", DOCUMENT_KEY_WRAPPING_ALGORITHM)
        cd = etree.SubElement(
            key, "{{{enc}}}CipherData".format(enc=ENC), nsmap=NSMAP
        )
        cv = etree.SubElement(
            cd, "{{{enc}}}CipherValue".format(enc=ENC), nsmap=NSMAP
        )
        cv.text = self.cipher_value

        return dk

    @staticmethod
    def parse(xml):
        """
        Parse XML and return MACMethod
        """
        if isinstance(xml, (str, bytes)):
            xml = etree.fromstring(xml)

        cipher_value = xml.find(".//{{{enc}}}CipherValue".format(enc=ENC)).text

        return MACMethod(cipher_value)


class DeliveryData(CPIXComparableBase):
    """
    DeliveryData element
    Has child elements:
        delivery_key: DeliveryKey
        document_key: DocumentKey
    Has (technically) optional child element:
        mac_method:   MACMethod
    """

    def __init__(self, delivery_key, document_key, mac_method=None):
        self._delivery_key = None
        self._document_key = None
        self._mac_method = None

        self.delivery_key = delivery_key
        self.document_key = document_key
        self.mac_method = mac_method

    @property
    def delivery_key(self):
        return self._delivery_key

    @delivery_key.setter
    def delivery_key(self, delivery_key):
        if isinstance(delivery_key, DeliveryKey):
            self._delivery_key = delivery_key
        else:
            raise TypeError("delivery_key should be a DeliveryKey")

    @property
    def document_key(self):
        return self._document_key

    @document_key.setter
    def document_key(self, document_key):
        if isinstance(document_key, DocumentKey):
            self._document_key = document_key
        else:
            raise TypeError("document_key should be a DocumentKey")

    @property
    def mac_method(self):
        return self._mac_method

    @mac_method.setter
    def mac_method(self, mac_method):
        if mac_method is None:
            return
        if isinstance(mac_method, MACMethod):
            self._mac_method = mac_method
        else:
            raise TypeError("mac_method should be a MACMethod")

    def element(self):
        """Returns XML element"""
        el = etree.Element("DeliveryData", nsmap=NSMAP)

        el.append(self.delivery_key.element())
        el.append(self.document_key.element())
        if self.mac_method is not None:
            el.append(self.mac_method.element())

        return el

    @staticmethod
    def parse(xml):
        """
        Parse XML and return DeliveryData
        """
        if isinstance(xml, (str, bytes)):
            xml = etree.fromstring(xml)

        mac_method = None

        for element in xml.getchildren():
            tag = etree.QName(element.tag).localname
            if tag == "DeliveryKey":
                delivery_key = DeliveryKey.parse(element)
            if tag == "DocumentKey":
                document_key = DocumentKey.parse(element)
            if tag == "MACMethod":
                mac_method = MACMethod.parse(element)

        return DeliveryData(delivery_key, document_key, mac_method)
