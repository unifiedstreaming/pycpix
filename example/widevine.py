"""
Simple script to call Widevine API to get keys and output CPIX
"""
import argparse
from base64 import b64encode, b64decode, b16encode
import json
import requests
import logging
from lxml import etree
import cpix

logger = logging.getLogger(__name__)

valid_tracks = ["AUDIO", "SD", "HD", "UHD1", "UHD2"]


def get_keys(content_id, url, tracks):
    track_list = []

    #remove any invalid track types
    for track in tracks.upper().split(","):
        if track in valid_tracks:
            track_list.append({"type": track})

    request = {
        "content_id": str(b64encode(bytes(content_id, "ASCII")), "ASCII"),
        "policy": "",
        "drm_types": ("WIDEVINE",),
        "tracks": track_list,
    }
    logger.debug("request: {}".format(request))

    request_data = {
        "request": str(b64encode(bytes(json.dumps(request), "ASCII")), "ASCII"),
        "signer": "widevine_test"
    }

    r = requests.post(url, data=json.dumps(request_data))
    response = json.loads(b64decode(json.loads(r.text)["response"]))
    logger.debug("decode widevine response: {}".format(response))

    return response


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

    keys = get_keys(args.content_id, args.url, args.tracks)

    for track in keys["tracks"]:
        logger.debug("{type} kid: {kid} cek: {cek} pssh: {pssh}".format(
            type=track["type"],
            kid=track["key_id"],
            cek=track["key"],
            pssh=track["pssh"][0]["data"]
        ))

    cpix_doc = make_cpix(keys)

    cpix_xml = etree.tostring(
        cpix_doc.element(), pretty_print=True, xml_declaration=True, encoding="UTF-8")

    if args.stdout:
        print(str(cpix_xml, "utf-8"))
    else:
        with open(args.output_filename,"wb") as f:
            f.write(cpix_xml)

if (__name__ == "__main__"):
    main()
