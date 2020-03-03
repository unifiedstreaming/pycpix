"""
Functions for manipulating Widevine DRM
"""
from Crypto.Cipher import AES
from Crypto.Hash import SHA1
from Crypto.Util.Padding import pad
from base64 import b16decode, b64decode, b64encode
import requests
import json
from uuid import UUID
from .widevine_pb2 import WidevineCencHeader
from construct.core import (
    Prefixed,
    Struct,
    Const,
    Int8ub,
    Int24ub,
    Int32ub,
    Bytes,
    GreedyBytes,
    PrefixedArray,
    Default,
    If,
    this,
)


WIDEVINE_SYSTEM_ID = UUID("edef8ba9-79d6-4ace-a3c8-27dcd51d21ed")

# Construct for a Widevine PSSH box
PSSH_BOX = Prefixed(
    Int32ub,
    Struct(
        "type" / Const(b"pssh"),
        "version" / Default(Int8ub, 1),
        "flags" / Const(0, Int24ub),
        "system_id" / Const(WIDEVINE_SYSTEM_ID.bytes, Bytes(16)),
        "key_ids" / If(this.version == 1, PrefixedArray(Int32ub, Bytes(16))),
        "data" / Prefixed(Int32ub, GreedyBytes),
    ),
    includelength=True,
)

VALID_TRACKS = ["AUDIO", "SD", "HD", "UHD1", "UHD2"]
PROTECTION_SCHEME = {
    "cenc": 1667591779,
    "cens": 1667591795,
    "cbc1": 1667392305,
    "cbcs": 1667392371,
}


def sign_request(request, key, iv):
    """
    Sign request
    Returns base64 signature
    """
    hashed_request = SHA1.new(bytes(json.dumps(request), "ASCII"))

    cipher = AES.new(b16decode(key), AES.MODE_CBC, b16decode(iv))
    ciphertext = cipher.encrypt(pad(hashed_request.digest(), 16))

    return b64encode(ciphertext)


def get_keys(
    content_id, url, tracks, policy, signer, signer_key=None, signer_iv=None
):
    """
    Get keys from widevine key server
    """
    track_list = []

    if isinstance(tracks, str):
        tracks = tracks.upper().split(",")

    # remove any invalid track types
    for track in tracks:
        if track in VALID_TRACKS:
            track_list.append({"type": track})

    request = {
        "content_id": str(b64encode(bytes(content_id, "ASCII")), "ASCII"),
        "policy": policy,
        "drm_types": ["WIDEVINE"],
        "tracks": track_list,
    }

    request_data = {
        "request": str(
            b64encode(bytes(json.dumps(request), "ASCII")), "ASCII"
        ),
        "signer": signer,
    }

    if signer_key is not None and signer_iv is not None:
        signature = sign_request(request, signer_key, signer_iv)
        request_data["signature"] = str(signature, "ASCII")

    r = requests.post(url, data=json.dumps(request_data))

    if r.status_code != 200:
        raise Exception(
            "Widevine request failed with status code {}".format(r.status_code)
        )

    response = json.loads(b64decode(json.loads(r.text)["response"]))

    return response


def generate_widevine_data(
    key_ids=None, provider=None, content_id=None, protection_scheme=None
):
    """
    Generate basic Widevine PSSH data

    Following Widevine requirements must have either a list a key IDs or a
    content ID
    """
    if key_ids is None and content_id is None:
        raise Exception("Must provide either list of key IDs or content ID")

    pssh_data = WidevineCencHeader()

    if provider is not None:
        pssh_data.provider = provider

    if key_ids is not None:
        for key_id in key_ids:
            if isinstance(key_id, str):
                key_id = UUID(key_id).bytes
            elif isinstance(key_id, bytes) and len(key_id) == 32:
                # assume a length 32 byte string is an encoded hex string
                key_id = UUID(str(key_id, "ASCII")).bytes
            elif isinstance(key_id, UUID):
                key_id = key_id.bytes
            pssh_data.key_id.append(key_id)

    if content_id is not None:
        if isinstance(content_id, str):
            pssh_data.content_id = bytes(content_id, "UTF-8")
        elif isinstance(content_id, bytes):
            pssh_data.content_id = content_id
        else:
            raise TypeError("content_id should be string or bytes")

    if (
        protection_scheme is not None
        and protection_scheme in PROTECTION_SCHEME
    ):
        pssh_data.protection_scheme = PROTECTION_SCHEME[protection_scheme]

    return pssh_data


def generate_pssh(
    key_ids=None,
    provider=None,
    content_id=None,
    version=1,
    protection_scheme=None,
):
    """
    Generate basic Widevine PSSH box

    Defaults to creating version 1 PSSH box, with key IDs listed
    """
    if key_ids is None:
        raise Exception("Must provide a list of key IDs")

    kids = []
    for key_id in key_ids:
        if isinstance(key_id, str):
            key_id = UUID(key_id).bytes
        elif isinstance(key_id, bytes):
            key_id = UUID(str(key_id, "ASCII")).bytes
        elif isinstance(key_id, UUID):
            key_id = key_id.bytes
        kids.append(key_id)

    pssh_data = generate_widevine_data(
        kids, provider, content_id, protection_scheme
    )

    pssh = PSSH_BOX.build(
        {
            "version": version,
            "key_ids": kids,
            "data": pssh_data.SerializeToString(),
        }
    )

    return pssh
