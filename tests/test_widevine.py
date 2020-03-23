import pytest
from cpix.drm import widevine
from uuid import UUID


VALID_TRACKS = ["AUDIO", "SD", "HD", "UHD1", "UHD2"]
WIDEVINE_TEST_URL = (
    "http://license.uat.widevine.com/cenc/getcontentkey/widevine_test"
)
WIDEVINE_TEST = "widevine_test"
WIDEVINE_TEST_KEY = (
    "1AE8CCD0E7985CC0B6203A55855A1034AFC252980E970CA90E5202689F947AB9"
)
WIDEVINE_TEST_IV = "D58CE954203B7C9A9A9D467F59839249"


def test_get_keys():
    response = widevine.get_keys(
        content_id="usptestcontent",
        url=WIDEVINE_TEST_URL,
        tracks=VALID_TRACKS,
        policy="",
        signer=WIDEVINE_TEST,
        signer_key=WIDEVINE_TEST_KEY,
        signer_iv=WIDEVINE_TEST_IV,
    )

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
        signer_iv=WIDEVINE_TEST_IV,
    )

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
        signer_iv=WIDEVINE_TEST_IV,
    )

    assert response["status"] == "OK"
    assert len(response["tracks"]) == 1


def test_generate_single_key_widevine_data():
    kids = ["C2FAF66E2852CC4C4A751F0A2A941FDB"]

    data = widevine.generate_widevine_data(
        key_ids=kids, provider=WIDEVINE_TEST, content_id="uspwvtest3"
    )

    assert (
        data.SerializeToString()
        == b'\x12\x10\xc2\xfa\xf6n(R\xccLJu\x1f\n*\x94\x1f\xdb\x1a\rwidevine_test"\nuspwvtest3'
    )

    parsed = widevine.WidevineCencHeader()
    parsed.ParseFromString(data.SerializeToString())

    assert parsed.key_id == [UUID(kid).bytes for kid in kids]
    assert parsed.provider == WIDEVINE_TEST
    assert str(parsed.content_id, "UTF-8") == "uspwvtest3"


def test_generate_multi_key_widevine_data():
    kids = [
        "C2FAF66E2852CC4C4A751F0A2A941FDB",
        "087BCFC6F7A55716B8406AA6EBA3369E",
        "0D6B40238DA15E75AF6875C514C59B63",
    ]

    data = widevine.generate_widevine_data(
        key_ids=kids, provider=WIDEVINE_TEST, content_id="uspwvtest3"
    )

    assert (
        data.SerializeToString()
        == b'\x12\x10\xc2\xfa\xf6n(R\xccLJu\x1f\n*\x94\x1f\xdb\x12\x10\x08{\xcf\xc6\xf7\xa5W\x16\xb8@j\xa6\xeb\xa36\x9e\x12\x10\rk@#\x8d\xa1^u\xafhu\xc5\x14\xc5\x9bc\x1a\rwidevine_test"\nuspwvtest3'
    )

    parsed = widevine.WidevineCencHeader()
    parsed.ParseFromString(data.SerializeToString())

    assert parsed.key_id == [UUID(kid).bytes for kid in kids]
    assert parsed.provider == WIDEVINE_TEST
    assert str(parsed.content_id, "UTF-8") == "uspwvtest3"


def test_single_key_v0_pssh():
    kids = ["C2FAF66E2852CC4C4A751F0A2A941FDB"]

    pssh = widevine.generate_pssh(
        key_ids=kids,
        provider=WIDEVINE_TEST,
        content_id="uspwvtest3",
        version=0,
    )

    assert (
        pssh
        == b"\x00\x00\x00Mpssh\x00\x00\x00\x00\xed\xef\x8b\xa9y\xd6J\xce\xa3\xc8'\xdc\xd5\x1d!\xed\x00\x00\x00-\x12\x10\xc2\xfa\xf6n(R\xccLJu\x1f\n*\x94\x1f\xdb\x1a\rwidevine_test\"\nuspwvtest3"
    )


def test_multiple_key_v0_pssh():
    kids = [
        "C2FAF66E2852CC4C4A751F0A2A941FDB",
        "087BCFC6F7A55716B8406AA6EBA3369E",
        "0D6B40238DA15E75AF6875C514C59B63",
    ]

    pssh = widevine.generate_pssh(
        key_ids=kids,
        provider=WIDEVINE_TEST,
        content_id="uspwvtest3",
        version=0,
    )

    assert (
        pssh
        == b"\x00\x00\x00qpssh\x00\x00\x00\x00\xed\xef\x8b\xa9y\xd6J\xce\xa3\xc8'\xdc\xd5\x1d!\xed\x00\x00\x00Q\x12\x10\xc2\xfa\xf6n(R\xccLJu\x1f\n*\x94\x1f\xdb\x12\x10\x08{\xcf\xc6\xf7\xa5W\x16\xb8@j\xa6\xeb\xa36\x9e\x12\x10\rk@#\x8d\xa1^u\xafhu\xc5\x14\xc5\x9bc\x1a\rwidevine_test\"\nuspwvtest3"
    )


def test_single_key_v1_pssh():
    kids = ["C2FAF66E2852CC4C4A751F0A2A941FDB"]

    pssh = widevine.generate_pssh(
        key_ids=kids,
        provider=WIDEVINE_TEST,
        content_id="uspwvtest3",
        version=0,
    )

    assert (
        pssh
        == b"\x00\x00\x00Mpssh\x00\x00\x00\x00\xed\xef\x8b\xa9y\xd6J\xce\xa3\xc8'\xdc\xd5\x1d!\xed\x00\x00\x00-\x12\x10\xc2\xfa\xf6n(R\xccLJu\x1f\n*\x94\x1f\xdb\x1a\rwidevine_test\"\nuspwvtest3"
    )


def test_multiple_key_v1_pssh():
    kids = [
        "C2FAF66E2852CC4C4A751F0A2A941FDB",
        "087BCFC6F7A55716B8406AA6EBA3369E",
        "0D6B40238DA15E75AF6875C514C59B63",
    ]

    pssh = widevine.generate_pssh(
        key_ids=kids,
        provider=WIDEVINE_TEST,
        content_id="uspwvtest3",
        version=0,
    )

    assert (
        pssh
        == b"\x00\x00\x00qpssh\x00\x00\x00\x00\xed\xef\x8b\xa9y\xd6J\xce\xa3\xc8'\xdc\xd5\x1d!\xed\x00\x00\x00Q\x12\x10\xc2\xfa\xf6n(R\xccLJu\x1f\n*\x94\x1f\xdb\x12\x10\x08{\xcf\xc6\xf7\xa5W\x16\xb8@j\xa6\xeb\xa36\x9e\x12\x10\rk@#\x8d\xa1^u\xafhu\xc5\x14\xc5\x9bc\x1a\rwidevine_test\"\nuspwvtest3"
    )
