"""
Functions for manipulating Widevine DRM
"""
from Crypto.Cipher import AES
from Crypto.Hash import SHA1
from Crypto.Util.Padding import pad
from base64 import b16decode, b64decode, b64encode
import requests
import json


VALID_TRACKS = ["AUDIO", "SD", "HD", "UHD1", "UHD2"]


def sign_request(request, key, iv):
    """
    Sign request
    Returns base64 signature
    """
    hashed_request = SHA1.new(bytes(json.dumps(request), "ASCII"))

    cipher = AES.new(b16decode(key),
                     AES.MODE_CBC, b16decode(iv))
    ciphertext = cipher.encrypt(pad(hashed_request.digest(), 16))

    return b64encode(ciphertext)


def get_keys(content_id, url, tracks, policy, signer, signer_key=None,
             signer_iv=None):
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
        "drm_types": ["WIDEVINE", ],
        "tracks": track_list,
    }

    request_data = {
        "request": str(b64encode(bytes(json.dumps(request), "ASCII")),
                       "ASCII"),
        "signer": signer
    }

    if signer_key is not None and signer_iv is not None:
        signature = sign_request(request, signer_key, signer_iv)
        request_data["signature"] = str(signature, "ASCII")

    r = requests.post(url, data=json.dumps(request_data))

    if r.status_code != 200:
        raise Exception("Widevine request failed with status code {}".format(
            r.status_code))

    response = json.loads(b64decode(json.loads(r.text)["response"]))

    return response
