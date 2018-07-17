"""
Simple script to generate Playready CPIX documents based on test server
"""
import argparse
from base64 import b64encode, b64decode, b16encode, b16decode
import logging
from lxml import etree
import cpix
from Crypto.Hash import SHA256
from Crypto.Cipher import AES
import random
import uuid
from construct.core import Prefixed, Struct, Const, Int8ub, Int24ub, Int32ub, Bytes, GreedyBytes, PrefixedArray


logger = logging.getLogger(__name__)

PLAYREADY_TEST_KEY_SEED = b"XVBovsmzhP9gRIZxWfFta3VVRPzVEWmJsazEJ46I"
PLAYREADY_SYSTEM_ID = uuid.UUID("9a04f079-9840-4286-ab92-e65be0885f95")

# Construct for a Playready PSSH box
pssh_box = Prefixed(
    Int32ub,
    Struct(
        "type" / Const(b"pssh"),
        "version" / Const(1, Int8ub),
        "flags" / Const(0, Int24ub),
        "system_id" / Const(PLAYREADY_SYSTEM_ID.bytes, Bytes(16)),
        "key_ids" / PrefixedArray(Int32ub, Bytes(16)),
        "data" / Prefixed(Int32ub, GreedyBytes)
    ),
    includelength=True
)


def seeded_uuid(seed):
    """
    Generate a seeded UUID
    """
    random.seed(seed)
    return uuid.UUID(
        int=(random.getrandbits(128) | (1 << 63) | (1 << 78)) & (~(1 << 79) & ~(1 << 77) & ~(1 << 76) & ~(1 << 62)))


def generate_key_ids(content_id, tracks):
    """
    From a given content ID generate key IDs matching Widevine style
    Done by generating seeded UUIDs
    """
    keys_base = {
        "AUDIO": "{}-AUDIO",
        "SD": "{}-SD",
        "HD": "{}-HD",
        "UHD1": "{}-UHD1",
        "UHD2": "{}-UHD2",
    }
    keys = []
    for key, value in keys_base.items():
        if key in tracks.upper().split(","):
            keys.append({
                "type": key,
                "key_id": seeded_uuid(value.format(content_id))})

    return keys


def generate_content_key(key_id, key_seed=PLAYREADY_TEST_KEY_SEED):
    """
    Generate content key from key ID
    """
    if len(key_seed) < 30:
        raise Exception("seed must be >= 30 bytes")
    key_seed = b64decode(key_seed)
    # key ID should be a UUID
    if isinstance(key_id, str):
        key_id = uuid.UUID(key_id)
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
            sha_a[i] ^ sha_a[i+16] ^ sha_b[i] ^ sha_b[i+16] ^ sha_c[i] ^ sha_c[i+16]).to_bytes(1, byteorder='big')

    return b16encode(content_key)


def checksum(kid, cek):
    """
    Generate playready key checksum

    From https://docs.microsoft.com/en-gb/playready/specifications/playready-header-specification#keychecksum

    For an ALGID value set to “AESCTR”, the 16-byte Key ID is encrypted with a
    16-byte AES content key using ECB mode. The first 8 bytes of the buffer is
    extracted and base64 encoded.
    """
    cipher = AES.new(b16decode(cek), AES.MODE_ECB)
    ciphertext = cipher.encrypt(kid.bytes_le)

    return b64encode(ciphertext[:8])


def generate_wrmheader(keys, url, algorithm="AESCTR"):
    """
    Generate Playready header 4.2 or 4.3 depending on the encryption algorithm
    specified
    """
    if algorithm not in ["AESCTR", "AESCBC"]:
        raise ValueError("algorithm must be AESCTR or AESCBC")

    wrmheader = etree.Element("WRMHEADER", nsmap={
                              None: "http://schemas.microsoft.com/DRM/2007/03/PlayReadyHeader"})

    if algorithm == "AESCBC":
        wrmheader.set("version", "4.3.0.0")
    else:
        wrmheader.set("version", "4.2.0.0")

    data = etree.SubElement(wrmheader, "DATA")
    protect_info = etree.SubElement(data, "PROTECTINFO")
    kids = etree.SubElement(protect_info, "KIDS")

    for key in keys:
        kid = etree.Element("KID")
        kid.set("ALGID", algorithm)
        if algorithm == "AESCTR":
            kid.set("CHECKSUM", checksum(key["key_id"], key["key"]))
        kid.set("VALUE", b64encode(key["key_id"].bytes_le))
        kid.text = ""
        kids.append(kid)

    la_url = etree.SubElement(data, "LA_URL")
    la_url.text = url

    return etree.tostring(wrmheader, encoding="utf-16le", xml_declaration=False)


def generate_playready_object(wrmheader):
    """
    Generate a playready object from a wrmheader
    """
    return ((len(wrmheader) + 10).to_bytes(4, "little") +   # overall length
            (1).to_bytes(2, "little") +                     # record count
            (1).to_bytes(2, "little") +                     # record type
            len(wrmheader).to_bytes(2, "little") +          # wrmheader length
            wrmheader)                                      # wrmheader


def generate_pssh(keys, url, algorithm="AESCTR"):
    """
    Generate a PSSH box including Playready header
    """
    wrmheader = generate_wrmheader(keys, url, algorithm)
    pro = generate_playready_object(wrmheader)

    return pssh_box.build({
        "key_ids": [key["key_id"].bytes for key in keys],
        "data": pro
    })


def make_cpix(keys, pssh):
    """
    Make a Playready CPIX document based on array of keys and PSSH
    """
    cpix_doc = cpix.CPIX(
        content_keys=cpix.ContentKeyList(),
        drm_systems=cpix.DRMSystemList(),
        usage_rules=cpix.UsageRuleList())

    for key in keys:
        print(key)
        content_key = cpix.ContentKey(
            kid=key["key_id"],
            cek=b64encode(b16decode(key["key"]))
        )
        cpix_doc.content_keys.append(content_key)

        drm_system = cpix.DRMSystem(
            kid=key["key_id"],
            system_id=PLAYREADY_SYSTEM_ID,
            pssh=pssh
        )
        cpix_doc.drm_systems.append(drm_system)

        if key["type"] == "AUDIO":
            usage_rule = cpix.UsageRule(
                kid=key["key_id"],
                filters=[
                    cpix.AudioFilter()
                ]
            )
            cpix_doc.usage_rules.append(usage_rule)

        if key["type"] == "SD":
            usage_rule = cpix.UsageRule(
                kid=key["key_id"],
                filters=[
                    cpix.VideoFilter(
                        max_pixels=589824  # 1024 * 576
                    )
                ]
            )
            cpix_doc.usage_rules.append(usage_rule)

        if key["type"] == "HD":
            usage_rule = cpix.UsageRule(
                kid=key["key_id"],
                filters=[
                    cpix.VideoFilter(
                        min_pixels=589825,  # 1024 * 576 + 1
                        max_pixels=2073600  # 1920 * 1080
                    )
                ]
            )
            cpix_doc.usage_rules.append(usage_rule)

        if key["type"] == "UHD1":
            usage_rule = cpix.UsageRule(
                kid=key["key_id"],
                filters=[
                    cpix.VideoFilter(
                        min_pixels=2073601,  # 1920 * 1080 + 1
                        max_pixels=33177599  # 7680 * 4320 - 1
                    )
                ]
            )
            cpix_doc.usage_rules.append(usage_rule)

        if key["type"] == "UHD2":
            usage_rule = cpix.UsageRule(
                kid=key["key_id"],
                filters=[
                    cpix.VideoFilter(
                        min_pixels=33177600  # 7680 * 4320
                    )
                ]
            )
            cpix_doc.usage_rules.append(usage_rule)

    return cpix_doc


def main():
    parser = argparse.ArgumentParser(description="Get Widevine keys")
    parser.add_argument("--url",
                        action="store",
                        dest="url",
                        help="Playready license acquisition URL",
                        required=False,
                        default="https://test.playready.microsoft.com/service/rightsmanager.asmx")
    parser.add_argument("--content_id",
                        action="store",
                        dest="content_id",
                        help="Content ID",
                        required=True)
    parser.add_argument("--key_seed",
                        action="store",
                        dest="key_seed",
                        help="base64 encoded Key Seed, defaults to playready test server one",
                        default=PLAYREADY_TEST_KEY_SEED)
    parser.add_argument("--tracks",
                        action="store",
                        dest="tracks",
                        help="Track type (SD, HD, UHD1, UHD2, AUDIO)",
                        required=False,
                        default="SD,HD,UHD1,UHD2,AUDIO")
    parser.add_argument("--log_level",
                        action="store",
                        dest="log_level",
                        help="Set log verbosity (DEBUG, INFO, WARN, ERROR, CRITICAL). Default is WARN",
                        default="WARN")
    parser.add_argument("--stdout",
                        action="store_true",
                        dest="stdout",
                        help="Output CPIX to stdout rather than file")
    parser.add_argument("output_filename",
                        help="Output CPIX filename",
                        nargs="?")
    args = parser.parse_args()

    if args.output_filename is None and not args.stdout:
        parser.error("required to set either --stdout or an output filename")

    logger.setLevel(args.log_level)
    ch = logging.StreamHandler()
    ch.setLevel(args.log_level)
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    keys = generate_key_ids(args.content_id, args.tracks)

    for key in keys:
        key["key"] = generate_content_key(key["key_id"])

    pssh = b64encode(generate_pssh(keys, args.url))

    cpix_doc = make_cpix(keys, pssh)

    cpix_xml = etree.tostring(
        cpix_doc.element(), pretty_print=True, xml_declaration=True, encoding="UTF-8")

    if args.stdout:
        print(str(cpix_xml, "utf-8"))
    else:
        with open(args.output_filename, "wb") as f:
            f.write(cpix_xml)


if (__name__ == "__main__"):
    main()
