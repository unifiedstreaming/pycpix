import cpix
from lxml import etree


def test_delivery_key_dump():
    delivery_key = cpix.DeliveryKey(
        "bm90X2FfcmVhbF9jZXJ0Cg=="
    )

    xml = etree.tostring(delivery_key.element())

    assert(xml == b'<DeliveryKey xmlns="urn:dashif:org:cpix" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:pskc="urn:ietf:params:xml:ns:keyprov:pskc" xmlns:ds="http://www.w3.org/2000/09/xmldsig#" xmlns:enc="http://www.w3.org/2001/04/xmlenc#"><ds:X509Data><ds:X509Certificate>bm90X2FfcmVhbF9jZXJ0Cg==</ds:X509Certificate></ds:X509Data></DeliveryKey>')


def test_document_key_dump():
    document_key = cpix.DocumentKey(
        "bm90X2FfcmVhbF9jaXBoZXJfdmFsdWUK"
    )

    xml = etree.tostring(document_key.element())

    assert(xml == b'<DocumentKey xmlns="urn:dashif:org:cpix" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:pskc="urn:ietf:params:xml:ns:keyprov:pskc" xmlns:ds="http://www.w3.org/2000/09/xmldsig#" xmlns:enc="http://www.w3.org/2001/04/xmlenc#" Algorithm="http://www.w3.org/2001/04/xmlenc#aes256-cbc"><Data><pskc:Secret><pskc:EncryptedValue><enc:EncryptionMethod Algorithm="http://www.w3.org/2001/04/xmlenc#rsa-oaep-mgf1p"/><enc:CipherData><enc:CipherValue>bm90X2FfcmVhbF9jaXBoZXJfdmFsdWUK</enc:CipherValue></enc:CipherData></pskc:EncryptedValue></pskc:Secret></Data></DocumentKey>')


def test_mac_method_dump():
    mac_method = cpix.MACMethod(
        "YWxzb19ub3RfYV9yZWFsX2NpcGhlcl92YWx1ZQo="
    )

    xml = etree.tostring(mac_method.element())

    assert(xml == b'<MACMethod xmlns="urn:dashif:org:cpix" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:pskc="urn:ietf:params:xml:ns:keyprov:pskc" xmlns:ds="http://www.w3.org/2000/09/xmldsig#" xmlns:enc="http://www.w3.org/2001/04/xmlenc#" Algorithm="http://www.w3.org/2001/04/xmldsig-more#hmac-sha512"><Key><enc:EncryptionMethod Algorithm="http://www.w3.org/2001/04/xmlenc#rsa-oaep-mgf1p"/><enc:CipherData><enc:CipherValue>YWxzb19ub3RfYV9yZWFsX2NpcGhlcl92YWx1ZQo=</enc:CipherValue></enc:CipherData></Key></MACMethod>')


def test_delivery_data_parse():
    xml = b'<DeliveryData xmlns:pskc="urn:ietf:params:xml:ns:keyprov:pskc" xmlns:ds="http://www.w3.org/2000/09/xmldsig#" xmlns:enc="http://www.w3.org/2001/04/xmlenc#"><DeliveryKey><ds:X509Data><ds:X509Certificate>bm90X2FfcmVhbF9jZXJ0Cg==</ds:X509Certificate></ds:X509Data></DeliveryKey><DocumentKey Algorithm="http://www.w3.org/2001/04/xmlenc#aes256-cbc"><Data><pskc:Secret><pskc:EncryptedValue><enc:EncryptionMethod Algorithm="http://www.w3.org/2001/04/xmlenc#rsa-oaep-mgf1p"/><enc:CipherData><enc:CipherValue>bm90X2FfcmVhbF9jaXBoZXJfdmFsdWUK</enc:CipherValue></enc:CipherData></pskc:EncryptedValue></pskc:Secret></Data></DocumentKey><MACMethod Algorithm="http://www.w3.org/2001/04/xmldsig-more#hmac-sha512"><Key><enc:EncryptionMethod Algorithm="http://www.w3.org/2001/04/xmlenc#rsa-oaep-mgf1p"/><enc:CipherData><enc:CipherValue>YWxzb19ub3RfYV9yZWFsX2NpcGhlcl92YWx1ZQo=</enc:CipherValue></enc:CipherData></Key></MACMethod></DeliveryData>'

    delivery_data = cpix.parse(xml)

    assert delivery_data.delivery_key.certificate == "bm90X2FfcmVhbF9jZXJ0Cg=="
    assert delivery_data.document_key.cipher_value == "bm90X2FfcmVhbF9jaXBoZXJfdmFsdWUK"
    assert delivery_data.mac_method.cipher_value == "YWxzb19ub3RfYV9yZWFsX2NpcGhlcl92YWx1ZQo="
