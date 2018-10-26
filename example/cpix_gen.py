"""
Fully featured CPIX generator with sensible defaults for all drms

firstly playready + widevine

Work in progress...

general usage

cpix_gen [keys] [drm_systems] [usage_rules]


define (multiple) keys with:

    --key kid:cek

e.g.

    --key E82F184C3AAA57B4ACE8606B5E3FEBAD:C2FAF66E2852CC4C4A751F0A2A941FDB


define DRM systems with specific required options, e.g. playready LA URL

widevine opts:

    --widevine
    --widevine.content_id
    --widevine.provider

playready opts:

    --playready
    --playready.la_url
    --playready.cbcs


usage rules (if not using presets) can be defined
multiple filters can be comma separated

    --usage_rule kid filter_type:filter_parameter=value

e.g.

    --usage_rule kid video:min_pixels=0,video:max_pixels=442368

should produce something like

    <ContentKeyUsageRule kid="kid">
        <VideoFilter minPixels="0" maxPixels="442368" />
        <BitrateFilter maxBitrate="500000" />
    </ContentKeyUsageRule>

usage rule presets can be referred by name:

    audio: audio
    video: video

    video_sd: video - maxPixels = 442368
    video_hd: video - minPixels = 442369, maxPixels = 2073600
    video_uhd1: video - minPixels = 2073601, maxPixels = 8847360
    video_uhd2: video - minPixels = 8847361

e.g.

    --usage_rule_preset kid video_sd

"""
import argparse
import logging
import cpix
from cpix.drm import playready, widevine
from base64 import b16decode, b16encode, b64decode, b64encode
from uuid import UUID


class SmartFormatter(argparse.HelpFormatter):
    def _split_lines(self, text, width):
        if text.startswith('R|'):
            return text[2:].splitlines()
        # this is the RawTextHelpFormatter._split_lines
        return argparse.HelpFormatter._split_lines(self, text, width)


logger = logging.getLogger()


PRESET_USAGE_RULES = [
    "audio", "video", "video_sd", "video_hd", "video_uhd1", "videouhd2"]


def parse_keys(keys):
    parsed_keys = cpix.ContentKeyList()

    for key in keys:
        try:
            kid, cek = key.split(":")
        except ValueError:
            raise Exception("key must be KEY_ID:CONTENT_KEY (missing :)")

        if len(kid) != 32:
            raise Exception("key ID must be 128-bit")
        if len(cek) != 32:
            raise Exception("cek must be 128-bit")

        parsed_keys.append(
            cpix.ContentKey(kid=kid, cek=b64encode(b16decode(cek))))
    return parsed_keys


def main():
    parser = argparse.ArgumentParser(
        description="make complex cpix documents simple",
        formatter_class=SmartFormatter)
    # key(s)
    key_group = parser.add_argument_group("Keys")
    key_group.add_argument(
        "--key",
        action="append",
        dest="keys",
        help="one or more keys as KID:CEK",
        metavar="KID:CEK",
        required=True
    )
    # widevine opts
    widevine_group = parser.add_argument_group("Widevine")
    widevine_group.add_argument(
        "--widevine",
        action="store_true",
        dest="widevine",
        help="enable generation of widevine drm system",
        required=False
    )
    widevine_group.add_argument(
        "--widevine.content_id",
        action="store",
        dest="widevine_content_id",
        help="set content id for widevine pssh",
        required=False
    )
    widevine_group.add_argument(
        "--widevine.provider",
        action="store",
        dest="widevine_provider",
        help="set provider for widevine pssh",
        required=False
    )
    widevine_group.add_argument(
        "--widevine.pssh_version",
        action="store",
        dest="widevine_pssh_version",
        help="widevine pssh box version (default: 1)",
        required=False,
        default=1,
        type=int
    )
    # playready opts
    playready_group = parser.add_argument_group("PlayReady")
    playready_group.add_argument(
        "--playready",
        action="store_true",
        dest="playready",
        help="enable generation of playready drm system",
        required=False
    )
    playready_group.add_argument(
        "--playready.la_url",
        action="store",
        dest="playready_la_url",
        help="set playready license acquisition url",
        required=False
    )
    playready_group.add_argument(
        "--playready.cbcs",
        action="store_const",
        dest="playready_algorithm",
        help="set cbcs mode for playready pssh",
        const="AESCBC",
        default="AESCTR",
        required=False
    )
    playready_group.add_argument(
        "--playready.pssh_version",
        action="store",
        dest="playready_pssh_version",
        help="playready pssh box version (default: 1)",
        required=False,
        default=1,
        type=int
    )
    # custom usage rules
    usage_rule_group = parser.add_argument_group("Usage rules")
    usage_rule_group.add_argument(
        "--usage_rule",
        action="append",
        dest="custom_usage_rules",
        nargs=2,
        metavar=("KID", "USAGE_RULE"),
        help="R|create custom usage rule, format is type:parameter=value, \n"
             "multiples should be comma separated, e.g. \n"
             "video:max_pixels=442368,bitrate:max_bitrate=500000",
        required=False
    )
    # preset usage rules
    usage_rule_group.add_argument(
        "--usage_rule_preset",
        action="append",
        dest="preset_usage_rules",
        nargs=2,
        metavar=("KID", "USAGE_RULE_PRESET"),
        help="R|use preset usage rule \n"
             "(audio, video, video_sd, video_hd, video_uhd1, video_uhd2)",
        required=False
    )
    # generic opts
    output_group = parser.add_argument_group("Output")
    output_group.add_argument(
        "-o", "--output",
        action="store",
        dest="output_filename",
        help="Set output filename",
        required=False
    )
    output_group.add_argument(
        "--stdout",
        action="store_true",
        dest="stdout",
        help="Output CPIX to stdout rather than file"
    )
    parser.add_argument(
        "--log_level",
        action="store",
        dest="log_level",
        help="Set log verbosity (default: WARN)",
        required=False,
        default="WARN"
    )

    args = parser.parse_args()

    logger.setLevel(args.log_level)
    ch = logging.StreamHandler()
    ch.setLevel(args.log_level)
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    logger.debug(args)

    # check conditionally required options are set
    if args.playready and args.playready_la_url is None:
        parser.error(
            "When setting --playready must also set --playready.la_url")

    if args.output_filename is None and not args.stdout:
        parser.error("one of the arguments -o/--output --stdout is required")

    # parse keys
    try:
        keys = parse_keys(args.keys)
    except Exception as e:
        parser.error(e)

    logger.debug(repr(keys))

    # parse drm systems
    drm_systems = cpix.DRMSystemList()

    if args.widevine:
        pssh = widevine.generate_pssh(
            key_ids=[key.kid for key in keys],
            provider=args.widevine_provider,
            content_id=args.widevine_content_id,
            version=args.widevine_pssh_version
        )

        for key in keys:
            drm_systems.append(
                cpix.DRMSystem(
                    kid=key.kid,
                    system_id=cpix.WIDEVINE_SYSTEM_ID,
                    pssh=b64encode(pssh)
                )
            )

    if args.playready:
        pssh = playready.generate_pssh(
            keys=[{"key_id": key.kid, "key": b16encode(
                b64decode(key.cek))} for key in keys],
            url=args.playready_la_url,
            algorithm=args.playready_algorithm,
            version=args.playready_pssh_version
        )

        for key in keys:
            drm_systems.append(
                cpix.DRMSystem(
                    kid=key.kid,
                    system_id=cpix.PLAYREADY_SYSTEM_ID,
                    pssh=b64encode(pssh)
                )
            )

    # usage rules
    usage_rules = cpix.UsageRuleList()

    # presets
    if args.preset_usage_rules:
        for rule in args.preset_usage_rules:
            try:
                kid = UUID(rule[0])
            except ValueError:
                parser.error("Invalid key ID in preset usage rule.")
            if kid not in [key.kid for key in keys]:
                parser.error("Invalid key ID in preset usage rule.")

            if rule[1] == "audio":
                usage_rules.append(cpix.AudioUsageRule(kid))
            elif rule[1] == "video":
                usage_rules.append(cpix.VideoUsageRule(kid))
            elif rule[1] == "video_sd":
                usage_rules.append(cpix.SDVideoUsageRule(kid))
            elif rule[1] == "video_hd":
                usage_rules.append(cpix.HDVideoUsageRule(kid))
            elif rule[1] == "video_uhd1":
                usage_rules.append(cpix.UHD1VideoUsageRule(kid))
            elif rule[1] == "video_uhd2":
                usage_rules.append(cpix.UHD2VideoUsageRule(kid))
            else:
                parser.error("Invalid preset rule. Allowed values are: audio, "
                             "video, video_sd, video_hd, video_uhd1, "
                             "video_uhd2")

    # custom
    if args.custom_usage_rules:
        for rule in args.custom_usage_rules:
            try:
                kid = UUID(rule[0])
            except ValueError:
                parser.error("Invalid key ID in custom usage rule.")
            if kid not in [key.kid for key in keys]:
                parser.error("Invalid key ID in custom usage rule.")

            usage_rule = cpix.UsageRule(kid)

            parsed_filters = {}
            
            # parse the custom filter options
            for _filter in rule[1].split(","):
                filter_type, filter_param = _filter.split(":")
                fp_type, fp_value = filter_param.split("=")

                if filter_type == "audio":
                    if "audio" not in parsed_filters:
                        parsed_filters["audio"] = {}
                    parsed_filters["audio"][fp_type] = fp_value
                if filter_type == "video":
                    if "video" not in parsed_filters:
                        parsed_filters["video"] = {}
                    parsed_filters["video"][fp_type] = fp_value
                if filter_type == "bitrate":
                    if "bitrate" not in parsed_filters:
                        parsed_filters["bitrate"] = {}
                    parsed_filters["bitrate"][fp_type] = fp_value

            # convert parsed filters to proper objects
            if "audio" in parsed_filters:
                try:
                    usage_rule.append(
                        cpix.AudioFilter(**parsed_filters["audio"]))
                except TypeError:
                    parser.error(
                        "Invalid audio filter parameter in usage rule")
            if "video" in parsed_filters:
                try:
                    usage_rule.append(
                        cpix.VideoFilter(**parsed_filters["video"]))
                except TypeError:
                    parser.error(
                        "Invalid video filter parameter in usage rule")
            if "bitrate" in parsed_filters:
                try:
                    usage_rule.append(
                        cpix.BitrateFilter(**parsed_filters["bitrate"]))
                except TypeError:
                    parser.error(
                        "Invalid bitrate filter parameter in usage rule")

            usage_rules.append(usage_rule)

    # create complete CPIX document
    cpix_doc = cpix.CPIX(
        content_keys=keys,
        drm_systems=drm_systems,
        usage_rules=usage_rules
    )

    cpix_xml = cpix_doc.pretty_print(xml_declaration=True, encoding="UTF-8")

    if args.stdout:
        print(str(cpix_xml, "utf-8"))
    else:
        with open(args.output_filename, "wb") as f:
            f.write(cpix_xml)


if (__name__ == "__main__"):
    main()
