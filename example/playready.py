"""
Simple script to generate Playready CPIX documents based on test server
"""
import argparse
from base64 import b64encode, b64decode, b16encode, b16decode
import json
import logging
from lxml import etree
import cpix
from Crypto.Hash import MD5, SHA256
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import random
import uuid


logger = logging.getLogger(__name__)

PLAYREADY_TEST_KEY_SEED = b"XVBovsmzhP9gRIZxWfFta3VVRPzVEWmJsazEJ46I"


def seeded_uuid(seed):
    """
    Generate a seeded UUID
    """
    random.seed(seed)
    return uuid.UUID(int=(random.getrandbits(128) | (1 << 63) | (1 << 78)) & (~(1 << 79) & ~(1 << 77) & ~(1 << 76) & ~(1 << 62)))


def generate_key_ids(content_id):
    """
    From a given content ID generate key IDs matching Widevine style
    Done in a somewhat insecure way by MD5 hashing variations on the string
    """
    keys = {
        "AUDIO": "{}-AUDIO",
        "SD": "{}-SD",
        "HD": "{}-HD",
        "UHD1": "{}-UHD1",
        "UHD2": "{}-UHD2",
    }
    for key, value in keys.items():
        keys[key] = seeded_uuid(value.format(content_id))
    
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


def main():
    parser = argparse.ArgumentParser(description="Get Widevine keys")
    parser.add_argument("--url",
                        action="store",
                        dest="url",
                        help="Playready license acquisition URL",
                        required=False,
                        default="http://test.playready.microsoft.com/service/rightsmanager.asmx")
    parser.add_argument("--content_id",
                        action="store",
                        dest="key_id",
                        help="Content ID",
                        required=True)
    parser.add_argument("--key_seed",
                        action="store",
                        dest="key_seed",
                        help="base64 encoded Key Seed, defaults to playready test server one",
                        default=PLAYREADY_TEST_KEY_SEED)
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
