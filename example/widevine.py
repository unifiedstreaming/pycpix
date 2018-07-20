"""
Simple script to call Widevine API to get keys and output CPIX

Requires pycryptodome for signing requests
"""
import argparse
from base64 import b64decode, b16encode
import logging
from lxml import etree
import cpix
from cpix.drm import widevine


logger = logging.getLogger()

VALID_TRACKS = ["AUDIO", "SD", "HD", "UHD1", "UHD2"]

WIDEVINE_TEST_URL = "http://license.uat.widevine.com/cenc/getcontentkey/widevine_test"
WIDEVINE_TEST = "widevine_test"
WIDEVINE_TEST_KEY = "1AE8CCD0E7985CC0B6203A55855A1034AFC252980E970CA90E5202689F947AB9"
WIDEVINE_TEST_IV = "D58CE954203B7C9A9A9D467F59839249"


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

    for track in widevine_response["tracks"]:
        kid = str(b16encode(b64decode(track["key_id"])), "ASCII")

        content_key = cpix.ContentKey(
            kid=kid,
            cek=track["key"]
        )
        cpix_doc.content_keys.append(content_key)

        drm_system = cpix.DRMSystem(
            kid=kid,
            system_id=system_id,
            pssh=track["pssh"][0]["boxes"]
        )
        cpix_doc.drm_systems.append(drm_system)

        if track["type"] == "AUDIO":
            usage_rule = cpix.AudioUsageRule(kid=kid)
            cpix_doc.usage_rules.append(usage_rule)

        if track["type"] == "SD":
            usage_rule = cpix.SDVideoUsageRule(kid=kid)
            cpix_doc.usage_rules.append(usage_rule)

        if track["type"] == "HD":
            usage_rule = cpix.HDVideoUsageRule(kid=kid)
            cpix_doc.usage_rules.append(usage_rule)

        if track["type"] == "UHD1":
            usage_rule = cpix.UHD1VideoUsageRule(kid=kid)
            cpix_doc.usage_rules.append(usage_rule)

        if track["type"] == "UHD2":
            usage_rule = cpix.UHD2VideoUsageRule(kid=kid)
            cpix_doc.usage_rules.append(usage_rule)

    return cpix_doc


def main():
    parser = argparse.ArgumentParser(description="Get Widevine keys")
    parser.add_argument(
        "--url",
        action="store",
        dest="url",
        help="Widevine server URL (Default to Widevine test)",
        required=False,
        default=WIDEVINE_TEST_URL)
    parser.add_argument(
        "--content_id",
        action="store",
        dest="content_id",
        help="Content ID",
        required=True)
    parser.add_argument(
        "--tracks",
        action="store",
        dest="tracks",
        help="Track type (SD, HD, UHD1, UHD2, AUDIO)",
        required=False,
        default="SD,HD,UHD1,UHD2,AUDIO")
    parser.add_argument(
        "--policy",
        action="store",
        dest="policy",
        help="Policy",
        required=False,
        default="")
    parser.add_argument(
        "--widevine_signer",
        action="store",
        dest="widevine_signer",
        help="Widevine signer (Default to widevine_test)",
        required=False,
        default=WIDEVINE_TEST)
    parser.add_argument(
        "--widevine_signer_key",
        action="store",
        dest="widevine_signer_key",
        help="Widevine signer key (Default to widevine_test key)",
        required=False,
        default=WIDEVINE_TEST_KEY)
    parser.add_argument(
        "--widevine_signer_iv",
        action="store",
        dest="widevine_signer_iv",
        help="Widevine signer IV (Default to widevine_test IV)",
        required=False,
        default=WIDEVINE_TEST_IV)
    parser.add_argument(
        "--log_level",
        action="store",
        dest="log_level",
        help="Set log verbosity (DEBUG, INFO, WARN, ERROR, CRITICAL)",
        default="WARN")
    parser.add_argument(
        "--stdout",
        action="store_true",
        dest="stdout",
        help="Output CPIX to stdout rather than file")
    parser.add_argument(
        "output_filename",
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

    keys = widevine.get_keys(
        args.content_id,
        args.url,
        args.tracks,
        args.policy,
        args.widevine_signer,
        args.widevine_signer_key,
        args.widevine_signer_iv)

    for track in keys["tracks"]:
        logger.debug("{type} kid: {kid} cek: {cek} pssh: {pssh}".format(
            type=track["type"],
            kid=b16encode(b64decode(track["key_id"])),
            cek=b16encode(b64decode(track["key"])),
            pssh=track["pssh"][0]["boxes"]
        ))

    cpix_doc = make_cpix(keys)

    cpix_xml = cpix_doc.pretty_print(xml_declaration=True, encoding="UTF-8")

    if args.stdout:
        print(str(cpix_xml, "utf-8"))
    else:
        with open(args.output_filename, "wb") as f:
            f.write(cpix_xml)


if (__name__ == "__main__"):
    main()
