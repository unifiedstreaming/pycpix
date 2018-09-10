"""
Simple script to generate Playready Object based on list of key IDs and
a license acquisition URL

PlayReady Header specification: https://docs.microsoft.com/en-us/playready/specifications/playready-header-specification
"""
import argparse
import logging
from cpix.drm import playready
from base64 import b64encode


logger = logging.getLogger()

PLAYREADY_TEST_URL = (
    "https://test.playready.microsoft.com/service/rightsmanager.asmx")

# keys = [{'key_id': '54232edd-bd59-4872-8687-84a35f4f0c95', 'key': '0B2B9A424B80ECFE1D2F4C8083FE24AB'},
#         {'key_id': '01b32ff0-6d5b-44e9-8e55-31af5ea42deb', 'key': '8D2D2D9F3ABBC96164EC7B899C6E4DF6'},
#         {'key_id': 'fff357ac-5f71-4dfe-be0f-688e8d432b37', 'key': 'E7CB694ACC53D5B65DE49599397AFDA7'}]

# la_url = 'https://test.playready.microsoft.com/service/rightsmanager.asmx'

# wrm_header = playready.generate_wrmheader(keys, la_url)
# playready_object = playready.generate_playready_object(wrm_header)

# drm_specific_data = '--iss.drm_specific_data={}'.format(str(b64encode(playready_object), 'ascii'))

# print(drm_specific_data)


def main():
    parser = argparse.ArgumentParser(description="Generate PlayReady Object")
    parser.add_argument(
        "--url",
        "--la_url",
        action="store",
        dest="la_url",
        help="PlayReady license acquisition URL",
        required=False,
        default=PLAYREADY_TEST_URL)
    parser.add_argument(
        "--key_ids",
        action="store",
        dest="key_ids",
        help="List of Key IDs, comma separated. (e.g. --key_ids foo,bar)",
        required=True)
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
        key_ids.append({"key_id": key_id})

    la_url = args.la_url

    wrm_header = playready.generate_wrmheader(key_ids, la_url, use_checksum=False)
    playready_object = playready.generate_playready_object(wrm_header)

    drm_specific_data = '--iss.drm_specific_data={}'.format(str(b64encode(playready_object), 'ascii'))

    print(drm_specific_data)


if (__name__ == "__main__"):
    main()
