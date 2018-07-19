import pytest
from cpix.drm import widevine


VALID_TRACKS = ["AUDIO", "SD", "HD", "UHD1", "UHD2"]
WIDEVINE_TEST_URL = "http://license.uat.widevine.com/cenc/getcontentkey/widevine_test"
WIDEVINE_TEST = "widevine_test"
WIDEVINE_TEST_KEY = "1AE8CCD0E7985CC0B6203A55855A1034AFC252980E970CA90E5202689F947AB9"
WIDEVINE_TEST_IV = "D58CE954203B7C9A9A9D467F59839249"



def test_get_keys():
    response = widevine.get_keys(
        content_id="usptestcontent",
        url=WIDEVINE_TEST_URL,
        tracks=VALID_TRACKS,
        policy="",
        signer=WIDEVINE_TEST,
        signer_key=WIDEVINE_TEST_KEY,
        signer_iv=WIDEVINE_TEST_IV)

    assert response["status"] == "OK"
    assert len(response["tracks"]) == 5


def test_get_keys_string_tracks():
    response = widevine.get_keys(
        content_id="usptestcontent",
        url=WIDEVINE_TEST_URL,
        tracks="sd,hd,audio,uhd1,uhd2",
        policy="",
        signer=WIDEVINE_TEST,
        signer_key=WIDEVINE_TEST_KEY,
        signer_iv=WIDEVINE_TEST_IV)

    assert response["status"] == "OK"
    assert len(response["tracks"]) == 5


def test_get_single_key():
    response = widevine.get_keys(
        content_id="usptestcontent",
        url=WIDEVINE_TEST_URL,
        tracks="sd",
        policy="",
        signer=WIDEVINE_TEST,
        signer_key=WIDEVINE_TEST_KEY,
        signer_iv=WIDEVINE_TEST_IV)

    assert response["status"] == "OK"
    assert len(response["tracks"]) == 1
