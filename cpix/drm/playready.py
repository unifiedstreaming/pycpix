"""
Functions for manipulating Playready DRM
"""
from base64 import b16decode, b16encode, b64decode, b64encode
import uuid
from Crypto.Hash import SHA256
from Crypto.Cipher import AES
from construct.core import Prefixed, Struct, Const, Int8ub, Int24ub, Int32ub, \
    Bytes, GreedyBytes, PrefixedArray, Default, If, this
from lxml import etree


PLAYREADY_SYSTEM_ID = uuid.UUID("9a04f079-9840-4286-ab92-e65be0885f95")

# Construct for a Playready PSSH box
pssh_box = Prefixed(
    Int32ub,
    Struct(
        "type" / Const(b"pssh"),
        "version" / Default(Int8ub, 1),
        "flags" / Const(0, Int24ub),
        "system_id" / Const(PLAYREADY_SYSTEM_ID.bytes, Bytes(16)),
        "key_ids" / If(this.version == 1, PrefixedArray(Int32ub, Bytes(16))),
        "data" / Prefixed(Int32ub, GreedyBytes)
    ),
    includelength=True
)


def generate_content_key(key_id, key_seed):
    """
    Generate content key from key ID
    """
    if len(key_seed) < 30:
        raise Exception("seed must be >= 30 bytes")
    key_seed = b64decode(key_seed)
    # key ID should be a UUID
    if isinstance(key_id, str):
        key_id = uuid.UUID(key_id)
    elif isinstance(key_id, bytes):
        key_id = uuid.UUID(str(key_id, "ASCII"))
    elif isinstance(key_id, uuid.UUID):
        pass
    else:
        raise TypeError("key_id should be a uuid")

    key_id = key_id.bytes_le

    sha = SHA256.new()
    sha.update(key_seed)
    sha.update(key_id)
    sha_a = [x for x in sha.digest()]

    sha = SHA256.new()
    sha.update(key_seed)
    sha.update(key_id)
    sha.update(key_seed)
    sha_b = [x for x in sha.digest()]

    sha = SHA256.new()
    sha.update(key_seed)
    sha.update(key_id)
    sha.update(key_seed)
    sha.update(key_id)
    sha_c = [x for x in sha.digest()]

    content_key = b""
    for i in range(16):
        content_key += (
            sha_a[i] ^ sha_a[i + 16] ^ sha_b[i] ^ sha_b[i + 16] ^ sha_c[i] ^
            sha_c[i + 16]).to_bytes(1, byteorder='big')

    return b16encode(content_key)


def checksum(kid, cek):
    """
    Generate playready key checksum

    From
    https://docs.microsoft.com/en-gb/playready/specifications/playready-header-specification#keychecksum

    For an ALGID value set to “AESCTR”, the 16-byte Key ID is encrypted with a
    16-byte AES content key using ECB mode. The first 8 bytes of the buffer is
    extracted and base64 encoded.
    """
    if isinstance(kid, str):
        kid = uuid.UUID(kid)
    elif isinstance(kid, bytes):
        kid = uuid.UUID(str(kid, "ASCII"))
    cipher = AES.new(b16decode(cek), AES.MODE_ECB)
    ciphertext = cipher.encrypt(kid.bytes_le)

    return b64encode(ciphertext[:8])


def generate_wrmheader(keys, url, algorithm="AESCTR", use_checksum=True):
    """
    Generate Playready header 4.2 or 4.3 depending on the encryption algorithm
    specified
    """
    if algorithm not in ["AESCTR", "AESCBC"]:
        raise ValueError("algorithm must be AESCTR or AESCBC")

    wrmheader = etree.Element(
        "WRMHEADER",
        nsmap={
            None: "http://schemas.microsoft.com/DRM/2007/03/PlayReadyHeader"})

    if algorithm == "AESCBC":
        wrmheader.set("version", "4.3.0.0")
    else:
        wrmheader.set("version", "4.2.0.0")

    data = etree.SubElement(wrmheader, "DATA")
    protect_info = etree.SubElement(data, "PROTECTINFO")
    kids = etree.SubElement(protect_info, "KIDS")

    for key in keys:
        if isinstance(key["key_id"], str):
            key["key_id"] = uuid.UUID(key["key_id"])
        elif isinstance(key["key_id"], bytes):
            key["key_id"] = uuid.UUID(str(key["key_id"], "ASCII"))
        kid = etree.Element("KID")
        kid.set("ALGID", algorithm)
        if algorithm == "AESCTR" and use_checksum:
            kid.set("CHECKSUM", checksum(key["key_id"], key["key"]))
        kid.set("VALUE", b64encode(key["key_id"].bytes_le))
        kid.text = ""
        kids.append(kid)

    la_url = etree.SubElement(data, "LA_URL")
    la_url.text = url

    return etree.tostring(wrmheader, encoding="utf-16le",
                          xml_declaration=False)


def generate_playready_object(wrmheader):
    """
    Generate a playready object from a wrmheader
    """
    return ((len(wrmheader) + 10).to_bytes(4, "little") +   # overall length
            (1).to_bytes(2, "little") +                     # record count
            (1).to_bytes(2, "little") +                     # record type
            len(wrmheader).to_bytes(2, "little") +          # wrmheader length
            wrmheader)                                      # wrmheader


def generate_pssh(keys, url, algorithm="AESCTR", use_checksum=True, version=1):
    """
    Generate a PSSH box including Playready header

    Defaults to version 1 with key IDs listed
    """
    wrmheader = generate_wrmheader(keys, url, algorithm, use_checksum)
    pro = generate_playready_object(wrmheader)

    return pssh_box.build({
        "version": version,
        "key_ids": [key["key_id"].bytes for key in keys],
        "data": pro
    })
