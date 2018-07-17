"""
Script to generate Widevine + Playready CENC CPIX documents
Works with both test servers: gets keys from Widevine and re-uses them for
Playready by including kid and cek in the license acquisition URL
"""
import argparse
from base64 import b64encode, b64decode, b16encode, b16decode
import json
import requests
import logging
from lxml import etree
import cpix
from Crypto.Hash import SHA1, SHA256
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from construct.core import Prefixed, Struct, Const, Int8ub, Int24ub, Int32ub, Bytes, GreedyBytes, PrefixedArray
import uuid


logger = logging.getLogger(__name__)

PLAYREADY_SYSTEM_ID = uuid.UUID("9a04f079-9840-4286-ab92-e65be0885f95")
PLAYREADY_TEST_LA_URL = "https://test.playready.microsoft.com/service/rightsmanager.asmx"

VALID_TRACKS = ["AUDIO", "SD", "HD", "UHD1", "UHD2"]

WIDEVINE_TEST_KEY = "1AE8CCD0E7985CC0B6203A55855A1034AFC252980E970CA90E5202689F947AB9"
WIDEVINE_TEST_IV = "D58CE954203B7C9A9A9D467F59839249"

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

# widevine stuff
def sign_request(request):
    """
    Sign request with widevine_test key
    Returns base64 signature
    """
    hashed_request = SHA1.new(bytes(json.dumps(request), "ASCII"))
    logger.debug("hashed request: {}".format(hashed_request.hexdigest()))

    cipher = AES.new(b16decode(WIDEVINE_TEST_KEY),
                     AES.MODE_CBC, b16decode(WIDEVINE_TEST_IV))
    ciphertext = cipher.encrypt(pad(hashed_request.digest(), 16))

    logger.debug("b64ed ciphertext: {}".format(b64encode(ciphertext)))

    return b64encode(ciphertext)


def get_keys(content_id, url, tracks, policy):
    track_list = []

    # remove any invalid track types
    for track in tracks.upper().split(","):
        if track in VALID_TRACKS:
            track_list.append({"type": track})

    request = {
        "content_id": str(b64encode(bytes(content_id, "ASCII")), "ASCII"),
        "policy": policy,
        "drm_types": ["WIDEVINE", ],
        "tracks": track_list,
    }
    logger.debug("request: {}".format(request))

    signature = sign_request(request)

    request_data = {
        "request": str(b64encode(bytes(json.dumps(request), "ASCII")), "ASCII"),
        "signature": str(signature, "ASCII"),
        "signer": "widevine_test"
    }

    r = requests.post(url, data=json.dumps(request_data))
    logger.debug("response: {}".format(r.__dict__))

    response = json.loads(b64decode(json.loads(r.text)["response"]))
    logger.debug("decode widevine response: {}".format(response))

    return response


# playready stuff
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


def generate_pssh(keys, url=PLAYREADY_TEST_LA_URL, algorithm="AESCTR"):
    """
    Generate a PSSH box including Playready header
    """
    wrmheader = generate_wrmheader(keys, url, algorithm)
    pro = generate_playready_object(wrmheader)

    return pssh_box.build({
        "key_ids": [key["key_id"].bytes for key in keys],
        "data": pro
    })


def make_cpix(widevine_response):
    """
    Make CPIX document from Widevine response
    Returns CPIX XML
    """
    # make empty CPIX document structure
    cpix_doc = cpix.CPIX(
        content_keys=cpix.ContentKeyList(),
        drm_systems=cpix.DRMSystemList(),
        usage_rules=cpix.UsageRuleList())

    system_id = widevine_response["drm"][0]["system_id"]

    # generate playready PSSH
    keys = [{"key_id": uuid.UUID(str(b16encode(b64decode(track["key_id"])), "ASCII")), "key": b16encode(b64decode(track["key"]))}
            for track in widevine_response["tracks"]]

    # make playready LA URL with all keys as query params
    la_url = "{base}?cfg={keys}".format(
        base=PLAYREADY_TEST_LA_URL,
        keys=",".join(["(kid:{kid},contentkey:{cek})".format(kid=str(b64encode(key["key_id"].bytes_le), "ASCII"), cek=str(b64encode(b16decode(key["key"])), "ASCII")) for key in keys])
    )
    print(la_url)
    playready_pssh = b64encode(generate_pssh(keys, la_url))

    print(playready_pssh)

    for track in widevine_response["tracks"]:
        kid = str(b16encode(b64decode(track["key_id"])), "ASCII")

        content_key = cpix.ContentKey(
            kid=kid,
            cek=track["key"]
        )
        cpix_doc.content_keys.append(content_key)

        drm_system_wv = cpix.DRMSystem(
            kid=kid,
            system_id=system_id,
            pssh=track["pssh"][0]["boxes"]
        )
        cpix_doc.drm_systems.append(drm_system_wv)

        drm_system_pr = cpix.DRMSystem(
            kid=kid,
            system_id=PLAYREADY_SYSTEM_ID,
            pssh=playready_pssh
        )
        cpix_doc.drm_systems.append(drm_system_pr)

        if track["type"] == "AUDIO":
            usage_rule = cpix.UsageRule(
                kid=kid,
                filters=[
                    cpix.AudioFilter()
                ]
            )
            cpix_doc.usage_rules.append(usage_rule)

        if track["type"] == "SD":
            usage_rule = cpix.UsageRule(
                kid=kid,
                filters=[
                    cpix.VideoFilter(
                        max_pixels=589824  # 1024 * 576
                    )
                ]
            )
            cpix_doc.usage_rules.append(usage_rule)

        if track["type"] == "HD":
            usage_rule = cpix.UsageRule(
                kid=kid,
                filters=[
                    cpix.VideoFilter(
                        min_pixels=589825,  # 1024 * 576 + 1
                        max_pixels=2073600  # 1920 * 1080
                    )
                ]
            )
            cpix_doc.usage_rules.append(usage_rule)

        if track["type"] == "UHD1":
            usage_rule = cpix.UsageRule(
                kid=kid,
                filters=[
                    cpix.VideoFilter(
                        min_pixels=2073601,  # 1920 * 1080 + 1
                        max_pixels=33177599  # 7680 * 4320 - 1
                    )
                ]
            )
            cpix_doc.usage_rules.append(usage_rule)

        if track["type"] == "UHD2":
            usage_rule = cpix.UsageRule(
                kid=kid,
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
                        help="Widevine server URL, if not set defaults to http://license.uat.widevine.com/cenc/getcontentkey/widevine_test",
                        required=False,
                        default="http://license.uat.widevine.com/cenc/getcontentkey/widevine_test")
    parser.add_argument("--content_id",
                        action="store",
                        dest="content_id",
                        help="Content ID, if not set defaults to unified-streaming",
                        required=False,
                        default="unified-streaming")
    parser.add_argument("--tracks",
                        action="store",
                        dest="tracks",
                        help="Track type (SD, HD, UHD1, UHD2, AUDIO)",
                        required=False,
                        default="SD,HD,UHD1,UHD2,AUDIO")
    parser.add_argument("--policy",
                        action="store",
                        dest="policy",
                        help="Policy",
                        required=False,
                        default="")
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

    keys = get_keys(args.content_id, args.url, args.tracks, args.policy)

    for track in keys["tracks"]:
        logger.debug("{type} kid: {kid} cek: {cek} pssh: {pssh}".format(
            type=track["type"],
            kid=b16encode(b64decode(track["key_id"])),
            cek=b16encode(b64decode(track["key"])),
            pssh=track["pssh"][0]["boxes"]
        ))

    cpix_doc = make_cpix(keys)

    cpix_xml = etree.tostring(
        cpix_doc.element(), pretty_print=True, xml_declaration=True, encoding="UTF-8")

    if args.stdout:
        print(str(cpix_xml, "utf-8"))
    else:
        with open(args.output_filename, "wb") as f:
            f.write(cpix_xml)


if (__name__ == "__main__"):
    main()
