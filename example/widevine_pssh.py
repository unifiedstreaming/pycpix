"""
Simple script to generate a Widevine PSSH box for use with Unified Streaming
Packager and Origin

Examples:

    python widevine_pssh.py \
        --key_ids e82f184c-3aaa-57b4-ace8-606b5e3febad

Outputs:
    --widevine.drm_specific_data=AAAARnBzc2gBAAAA7e+LqXnWSs6jyCfc1R0h7QAAAAHoLxhMOqpXtKzoYGteP+utAAAAEhIQ6C8YTDqqV7Ss6GBrXj/rrQ==

Optionally add multiple keys comma-separated, content ID, provider, or desired
PSSH box version:

    python widevine_pssh.py \
        --key_ids e82f184c-3aaa-57b4-ace8-606b5e3febad,087bcfc6-f7a5-5716-b840-6aa6eba3369e,0d6b4023-8da1-5e75-af68-75c514c59b63 \
        --content_id uspwvtest3 \
        --pssh_version 1

Outputs:
    --widevine.drm_specific_data=AAAAlnBzc2gBAAAA7e+LqXnWSs6jyCfc1R0h7QAAAAPoLxhMOqpXtKzoYGteP+utCHvPxvelVxa4QGqm66M2ng1rQCONoV51r2h1xRTFm2MAAABCEhDoLxhMOqpXtKzoYGteP+utEhAIe8/G96VXFrhAaqbrozaeEhANa0AjjaFeda9odcUUxZtjIgp1c3B3dnRlc3Qz
"""
import argparse
import logging
from cpix.drm import widevine
from base64 import b64encode


logger = logging.getLogger()


def main():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description="""
Simple script to generate a Widevine PSSH box for use with Unified Streaming
Packager and Origin

Examples:

    python widevine_pssh.py \\
        --key_ids e82f184c-3aaa-57b4-ace8-606b5e3febad

Outputs:
    --widevine.drm_specific_data=AAAARnBzc2gBAAAA7e+LqXnWSs6jyCfc1R0h7QAAAAHoLxhMOqpXtKzoYGteP+utAAAAEhIQ6C8YTDqqV7Ss6GBrXj/rrQ==

Optionally add multiple keys comma-separated, content ID, provider, or desired
PSSH box version:

    python widevine_pssh.py \\
        --key_ids e82f184c-3aaa-57b4-ace8-606b5e3febad,087bcfc6-f7a5-5716-b840-6aa6eba3369e,0d6b4023-8da1-5e75-af68-75c514c59b63 \\
        --content_id uspwvtest3 \\
        --pssh_version 1

Outputs:
    --widevine.drm_specific_data=AAAAlnBzc2gBAAAA7e+LqXnWSs6jyCfc1R0h7QAAAAPoLxhMOqpXtKzoYGteP+utCHvPxvelVxa4QGqm66M2ng1rQCONoV51r2h1xRTFm2MAAABCEhDoLxhMOqpXtKzoYGteP+utEhAIe8/G96VXFrhAaqbrozaeEhANa0AjjaFeda9odcUUxZtjIgp1c3B3dnRlc3Qz
""",
    )
    parser.add_argument(
        "--key_ids",
        action="store",
        dest="key_ids",
        help="List of Key IDs, comma separated. (e.g. --key_ids foo,bar)",
        required=True,
    )
    parser.add_argument(
        "--content_id",
        action="store",
        dest="content_id",
        help="Optional content ID",
        required=False,
    )
    parser.add_argument(
        "--provider",
        action="store",
        dest="provider",
        help="Optional provider name",
        required=False,
    )
    parser.add_argument(
        "--pssh_version",
        action="store",
        dest="pssh_version",
        help="PSSH box version, default to 1",
        required=False,
        default=1,
        type=int,
    )
    parser.add_argument(
        "--protection_scheme",
        action="store",
        dest="protection_scheme",
        help="Optional protection scheme (cenc, cbc1, cens, cbcs)",
        required=False,
    )
    parser.add_argument(
        "--log_level",
        action="store",
        dest="log_level",
        help="Set log verbosity (Default is WARN)",
        required=False,
        default="WARN",
    )
    args = parser.parse_args()

    logger.setLevel(args.log_level)
    ch = logging.StreamHandler()
    ch.setLevel(args.log_level)
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    key_ids = []
    for key_id in args.key_ids.split(","):
        key_ids.append(key_id)

    pssh = widevine.generate_pssh(
        key_ids,
        args.provider,
        args.content_id,
        args.pssh_version,
        args.protection_scheme,
    )

    drm_specific_data = "--widevine.drm_specific_data={}".format(
        str(b64encode(pssh), "ascii")
    )

    print(drm_specific_data)


if __name__ == "__main__":
    main()
