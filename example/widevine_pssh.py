"""
Simple script to generate a Widevine PSSH box
"""
import argparse
import logging
from cpix.drm import widevine
from base64 import b64encode


logger = logging.getLogger()



def main():
    parser = argparse.ArgumentParser(description="Generate Widevine PSSH")
    parser.add_argument(
        "--key_ids",
        action="store",
        dest="key_ids",
        help="List of Key IDs, comma separated. (e.g. --key_ids foo,bar)",
        required=True)
    parser.add_argument(
        "--content_id",
        action="store",
        dest="content_id",
        help="Optional content ID",
        required=False)
    parser.add_argument(
        "--provider",
        action="store",
        dest="provider",
        help="Optional provider name",
        required=False)
    parser.add_argument(
        "--pssh_version",
        action="store",
        dest="pssh_version",
        help="PSSH box version, default to 1",
        required=False,
        default=1,
        type=int)
    parser.add_argument(
        "--log_level",
        action="store",
        dest="log_level",
        help="Set log verbosity (Default is WARN)",
        required=False,
        default="WARN")
    args = parser.parse_args()

    logger.setLevel(args.log_level)
    ch = logging.StreamHandler()
    ch.setLevel(args.log_level)
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    key_ids = []
    for key_id in args.key_ids.split(","):
        key_ids.append(key_id)

    pssh = widevine.generate_pssh(
        key_ids, args.provider, args.content_id, args.pssh_version)

    drm_specific_data = '--widevine.drm_specific_data={}'.format(str(b64encode(pssh), 'ascii'))

    print(drm_specific_data)


if (__name__ == "__main__"):
    main()
