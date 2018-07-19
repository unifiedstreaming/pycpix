"""
Simple script to generate Playready CPIX documents based on test server
"""
import argparse
from base64 import b64encode, b16decode
import logging
from lxml import etree
import cpix
import cpix.drm.playready
import random
import uuid


logger = logging.getLogger()

PLAYREADY_TEST_URL = "https://test.playready.microsoft.com/service/rightsmanager.asmx"
PLAYREADY_TEST_KEY_SEED = b"XVBovsmzhP9gRIZxWfFta3VVRPzVEWmJsazEJ46I"
PLAYREADY_SYSTEM_ID = uuid.UUID("9a04f079-9840-4286-ab92-e65be0885f95")


def seeded_uuid(seed):
    """
    Generate a seeded UUID
    """
    random.seed(seed)
    return uuid.UUID(
        int=(random.getrandbits(128) | (1 << 63) | (1 << 78)) &
            (~(1 << 79) & ~(1 << 77) & ~(1 << 76) & ~(1 << 62)))


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


def make_cpix(keys, pssh):
    """
    Make a Playready CPIX document based on array of keys and PSSH
    """
    cpix_doc = cpix.CPIX(
        content_keys=cpix.ContentKeyList(),
        drm_systems=cpix.DRMSystemList(),
        usage_rules=cpix.UsageRuleList())

    for key in keys:
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
    parser.add_argument(
        "--url",
        action="store",
        dest="url",
        help="Playready license acquisition URL",
        required=False,
        default=PLAYREADY_TEST_URL)
    parser.add_argument(
        "--content_id",
        action="store",
        dest="content_id",
        help="Content ID",
        required=True)
    parser.add_argument(
        "--key_seed",
        action="store",
        dest="key_seed",
        help="base64 encoded Key Seed",
        default=PLAYREADY_TEST_KEY_SEED)
    parser.add_argument(
        "--tracks",
        action="store",
        dest="tracks",
        help="Track type (SD, HD, UHD1, UHD2, AUDIO)",
        required=False,
        default="SD,HD,UHD1,UHD2,AUDIO")
    parser.add_argument(
        "--log_level",
        action="store",
        dest="log_level",
        help="Set log verbosity (Default is WARN)",
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

    keys = generate_key_ids(args.content_id, args.tracks)

    for key in keys:
        key["key"] = cpix.drm.playready.generate_content_key(
            key["key_id"],
            PLAYREADY_TEST_KEY_SEED)

    pssh = b64encode(cpix.drm.playready.generate_pssh(keys, args.url))

    cpix_doc = make_cpix(keys, pssh)

    cpix_xml = cpix_doc.pretty_print(xml_declaration=True, encoding="UTF-8")

    if args.stdout:
        print(str(cpix_xml, "utf-8"))
    else:
        with open(args.output_filename, "wb") as f:
            f.write(cpix_xml)


if (__name__ == "__main__"):
    main()
