"""
Simple script to generate a PlayReady WRM Header for use with Unified Streaming
Packager and Origin

If license URL is not specified defaults to PlayReady test server:
    https://test.playready.microsoft.com/service/rightsmanager.asmx

Examples:

    python playready_object.py \
        --key_ids 54232EDDBD594872868784A35f4F0C95

Outputs:
    --iss.drm_specific_data=XgIAAAEAAQBUAjwAVwBSAE0ASABFAEEARABFAFIAIAB4AG0AbABuAHMAPQAiAGgAdAB0AHAAOgAvAC8AcwBjAGgAZQBtAGEAcwAuAG0AaQBjAHIAbwBzAG8AZgB0AC4AYwBvAG0ALwBEAFIATQAvADIAMAAwADcALwAwADMALwBQAGwAYQB5AFIAZQBhAGQAeQBIAGUAYQBkAGUAcgAiACAAdgBlAHIAcwBpAG8AbgA9ACIANAAuADIALgAwAC4AMAAiAD4APABEAEEAVABBAD4APABQAFIATwBUAEUAQwBUAEkATgBGAE8APgA8AEsASQBEAFMAPgA8AEsASQBEACAAQQBMAEcASQBEAD0AIgBBAEUAUwBDAFQAUgAiACAAVgBBAEwAVQBFAD0AIgAzAFMANABqAFYARgBtADkAYwBrAGkARwBoADQAUwBqAFgAMAA4AE0AbABRAD0APQAiAD4APAAvAEsASQBEAD4APAAvAEsASQBEAFMAPgA8AC8AUABSAE8AVABFAEMAVABJAE4ARgBPAD4APABMAEEAXwBVAFIATAA+AGgAdAB0AHAAcwA6AC8ALwB0AGUAcwB0AC4AcABsAGEAeQByAGUAYQBkAHkALgBtAGkAYwByAG8AcwBvAGYAdAAuAGMAbwBtAC8AcwBlAHIAdgBpAGMAZQAvAHIAaQBnAGgAdABzAG0AYQBuAGEAZwBlAHIALgBhAHMAbQB4ADwALwBMAEEAXwBVAFIATAA+ADwALwBEAEEAVABBAD4APAAvAFcAUgBNAEgARQBBAEQARQBSAD4A

Multiple keys comma-separated, set CBCS scheme:

    python widevine_pssh.py \
        --key_ids 54232edd-bd59-4872-8687-84a35f4f0c95,01b32ff0-6d5b-44e9-8e55-31af5ea42deb \
        --cbcs

Outputs:
    --iss.drm_specific_data=1AIAAAEAAQDKAjwAVwBSAE0ASABFAEEARABFAFIAIAB4AG0AbABuAHMAPQAiAGgAdAB0AHAAOgAvAC8AcwBjAGgAZQBtAGEAcwAuAG0AaQBjAHIAbwBzAG8AZgB0AC4AYwBvAG0ALwBEAFIATQAvADIAMAAwADcALwAwADMALwBQAGwAYQB5AFIAZQBhAGQAeQBIAGUAYQBkAGUAcgAiACAAdgBlAHIAcwBpAG8AbgA9ACIANAAuADMALgAwAC4AMAAiAD4APABEAEEAVABBAD4APABQAFIATwBUAEUAQwBUAEkATgBGAE8APgA8AEsASQBEAFMAPgA8AEsASQBEACAAQQBMAEcASQBEAD0AIgBBAEUAUwBDAEIAQwAiACAAVgBBAEwAVQBFAD0AIgAzAFMANABqAFYARgBtADkAYwBrAGkARwBoADQAUwBqAFgAMAA4AE0AbABRAD0APQAiAD4APAAvAEsASQBEAD4APABLAEkARAAgAEEATABHAEkARAA9ACIAQQBFAFMAQwBCAEMAIgAgAFYAQQBMAFUARQA9ACIAOABDACsAegBBAFYAdAB0ADYAVQBTAE8AVgBUAEcAdgBYAHEAUQB0ADYAdwA9AD0AIgA+ADwALwBLAEkARAA+ADwALwBLAEkARABTAD4APAAvAFAAUgBPAFQARQBDAFQASQBOAEYATwA+ADwATABBAF8AVQBSAEwAPgBoAHQAdABwAHMAOgAvAC8AdABlAHMAdAAuAHAAbABhAHkAcgBlAGEAZAB5AC4AbQBpAGMAcgBvAHMAbwBmAHQALgBjAG8AbQAvAHMAZQByAHYAaQBjAGUALwByAGkAZwBoAHQAcwBtAGEAbgBhAGcAZQByAC4AYQBzAG0AeAA8AC8ATABBAF8AVQBSAEwAPgA8AC8ARABBAFQAQQA+ADwALwBXAFIATQBIAEUAQQBEAEUAUgA+AA==

PlayReady Header specification: https://docs.microsoft.com/en-us/playready/specifications/playready-header-specification
"""
import argparse
import logging
from cpix.drm import playready
from base64 import b64encode


logger = logging.getLogger()

PLAYREADY_TEST_URL = (
    "https://test.playready.microsoft.com/service/rightsmanager.asmx")


def main():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description="""
Simple script to generate a PlayReady WRM Header for use with Unified Streaming
Packager and Origin

If license URL is not specified defaults to PlayReady test server:
    https://test.playready.microsoft.com/service/rightsmanager.asmx


Examples:

    python playready_object.py \\
        --key_ids 54232EDDBD594872868784A35f4F0C95

Outputs:
    --iss.drm_specific_data=XgIAAAEAAQBUAjwAVwBSAE0ASABFAEEARABFAFIAIAB4AG0AbABuAHMAPQAiAGgAdAB0AHAAOgAvAC8AcwBjAGgAZQBtAGEAcwAuAG0AaQBjAHIAbwBzAG8AZgB0AC4AYwBvAG0ALwBEAFIATQAvADIAMAAwADcALwAwADMALwBQAGwAYQB5AFIAZQBhAGQAeQBIAGUAYQBkAGUAcgAiACAAdgBlAHIAcwBpAG8AbgA9ACIANAAuADIALgAwAC4AMAAiAD4APABEAEEAVABBAD4APABQAFIATwBUAEUAQwBUAEkATgBGAE8APgA8AEsASQBEAFMAPgA8AEsASQBEACAAQQBMAEcASQBEAD0AIgBBAEUAUwBDAFQAUgAiACAAVgBBAEwAVQBFAD0AIgAzAFMANABqAFYARgBtADkAYwBrAGkARwBoADQAUwBqAFgAMAA4AE0AbABRAD0APQAiAD4APAAvAEsASQBEAD4APAAvAEsASQBEAFMAPgA8AC8AUABSAE8AVABFAEMAVABJAE4ARgBPAD4APABMAEEAXwBVAFIATAA+AGgAdAB0AHAAcwA6AC8ALwB0AGUAcwB0AC4AcABsAGEAeQByAGUAYQBkAHkALgBtAGkAYwByAG8AcwBvAGYAdAAuAGMAbwBtAC8AcwBlAHIAdgBpAGMAZQAvAHIAaQBnAGgAdABzAG0AYQBuAGEAZwBlAHIALgBhAHMAbQB4ADwALwBMAEEAXwBVAFIATAA+ADwALwBEAEEAVABBAD4APAAvAFcAUgBNAEgARQBBAEQARQBSAD4A

Multiple keys comma-separated, set CBCS scheme:

    python widevine_pssh.py \\
        --key_ids 54232edd-bd59-4872-8687-84a35f4f0c95,01b32ff0-6d5b-44e9-8e55-31af5ea42deb \\
        --cbcs

Outputs:
    --iss.drm_specific_data=1AIAAAEAAQDKAjwAVwBSAE0ASABFAEEARABFAFIAIAB4AG0AbABuAHMAPQAiAGgAdAB0AHAAOgAvAC8AcwBjAGgAZQBtAGEAcwAuAG0AaQBjAHIAbwBzAG8AZgB0AC4AYwBvAG0ALwBEAFIATQAvADIAMAAwADcALwAwADMALwBQAGwAYQB5AFIAZQBhAGQAeQBIAGUAYQBkAGUAcgAiACAAdgBlAHIAcwBpAG8AbgA9ACIANAAuADMALgAwAC4AMAAiAD4APABEAEEAVABBAD4APABQAFIATwBUAEUAQwBUAEkATgBGAE8APgA8AEsASQBEAFMAPgA8AEsASQBEACAAQQBMAEcASQBEAD0AIgBBAEUAUwBDAEIAQwAiACAAVgBBAEwAVQBFAD0AIgAzAFMANABqAFYARgBtADkAYwBrAGkARwBoADQAUwBqAFgAMAA4AE0AbABRAD0APQAiAD4APAAvAEsASQBEAD4APABLAEkARAAgAEEATABHAEkARAA9ACIAQQBFAFMAQwBCAEMAIgAgAFYAQQBMAFUARQA9ACIAOABDACsAegBBAFYAdAB0ADYAVQBTAE8AVgBUAEcAdgBYAHEAUQB0ADYAdwA9AD0AIgA+ADwALwBLAEkARAA+ADwALwBLAEkARABTAD4APAAvAFAAUgBPAFQARQBDAFQASQBOAEYATwA+ADwATABBAF8AVQBSAEwAPgBoAHQAdABwAHMAOgAvAC8AdABlAHMAdAAuAHAAbABhAHkAcgBlAGEAZAB5AC4AbQBpAGMAcgBvAHMAbwBmAHQALgBjAG8AbQAvAHMAZQByAHYAaQBjAGUALwByAGkAZwBoAHQAcwBtAGEAbgBhAGcAZQByAC4AYQBzAG0AeAA8AC8ATABBAF8AVQBSAEwAPgA8AC8ARABBAFQAQQA+ADwALwBXAFIATQBIAEUAQQBEAEUAUgA+AA==
""")
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
        "--cbcs",
        action="store_true",
        dest="cbcs",
        help="Generate for CMAF cbcs scheme, i.e. AESCBC mode",
        required=False)
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

    if args.cbcs:
        algorithm = "AESCBC"
    else:
        algorithm = "AESCTR"

    wrm_header = playready.generate_wrmheader(
        key_ids, la_url, algorithm, use_checksum=False)
    playready_object = playready.generate_playready_object(wrm_header)

    drm_specific_data = '--iss.drm_specific_data={}'.format(
        str(b64encode(playready_object), 'ascii'))

    print(drm_specific_data)


if (__name__ == "__main__"):
    main()
