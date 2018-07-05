import pytest
import cpix
from lxml import etree
from uuid import UUID


def test_simple_usage_rule():
    usage_rule = cpix.UsageRule(
        kid="fdde4136-c15c-4953-bd45-ce0f454bd130",
        filters=[
            cpix.VideoFilter(),
            cpix.AudioFilter()
        ]
    )

    assert len(usage_rule) == 2

    xml = etree.tostring(usage_rule.element())

    assert xml == (
        b'<ContentKeyUsageRule kid="fdde4136-c15c-4953-bd45-ce0f454bd130"><VideoFilter/><AudioFilter/></ContentKeyUsageRule>')


def test_two_video_filters():
    usage_rule = cpix.UsageRule(
        kid="ceb5153d-9b2c-45a0-9c8c-2bfc5e8b0d2f",
        filters=[
            cpix.VideoFilter(hdr=True),
            cpix.VideoFilter(hdr=False),
            cpix.AudioFilter()
        ]
    )

    assert len(usage_rule) == 3

    xml = etree.tostring(usage_rule.element())

    assert xml == (
        b'<ContentKeyUsageRule kid="ceb5153d-9b2c-45a0-9c8c-2bfc5e8b0d2f"><VideoFilter hdr="true"/><VideoFilter hdr="false"/><AudioFilter/></ContentKeyUsageRule>')


def test_simple_widevine_drmsystem():
    drm_system = cpix.DRMSystem(
        kid="1447B7ED-2F66-572B-BD13-06CE7CF3610D",
        system_id="edef8ba9-79d6-4ace-a3c8-27dcd51d21ed",
        pssh=(
            "AAAAxnBzc2gBAAAA7e+LqXnWSs6jyCfc1R0h7QAAAAINw+xPdoNUi4HnPGTlguE2FE"
            "e37S9mVyu9EwbOfPNhDQAAAIISEBRHt+0vZlcrvRMGznzzYQ0SEFrGoR6qL17Vv2aM"
            "QByBNMoSEG7hNRbI51h7rp9+zT6Zom4SEPnsEqYaJl1Hj4MzTjp40scSEA3D7E92g1"
            "SLgec8ZOWC4TYaDXdpZGV2aW5lX3Rlc3QiEXVuaWZpZWQtc3RyZWFtaW5nSOPclZsG"
            ),
        content_protection_data=(
            "PCEtLSBXaWRldmluZSAtLT4KPENvbnRlbnRQcm90ZWN0aW9uCiAgeG1sbnM9InVybj"
            "ptcGVnOmRhc2g6c2NoZW1hOm1wZDoyMDExIgogIHhtbG5zOmNlbmM9InVybjptcGVn"
            "OmNlbmM6MjAxMyIKICBzY2hlbWVJZFVyaT0idXJuOnV1aWQ6RURFRjhCQTktNzlENi"
            "00QUNFLUEzQzgtMjdEQ0Q1MUQyMUVEIj4KICA8Y2VuYzpwc3NoPkFBQUF4bkJ6YzJn"
            "QkFBQUE3ZStMcVhuV1NzNmp5Q2ZjMVIwaDdRQUFBQUlOdyt4UGRvTlVpNEhuUEdUbG"
            "d1RTJGRWUzN1M5bVZ5dTlFd2JPZlBOaERRQUFBSUlTRUJSSHQrMHZabGNydlJNR3pu"
            "enpZUTBTRUZyR29SNnFMMTdWdjJhTVFCeUJOTW9TRUc3aE5SYkk1MWg3cnA5K3pUNl"
            "pvbTRTRVBuc0VxWWFKbDFIajRNelRqcDQwc2NTRUEzRDdFOTJnMVNMZ2VjOFpPV0M0"
            "VFlhRFhkcFpHVjJhVzVsWDNSbGMzUWlFWFZ1YVdacFpXUXRjM1J5WldGdGFXNW5TT1"
            "BjbFpzRzwvY2VuYzpwc3NoPgo8L0NvbnRlbnRQcm90ZWN0aW9uPg=="),
        hls_signaling_data=(
            "I0VYVC1YLUtFWTpNRVRIT0Q9U0FNUExFLUFFUyxLRVlJRD0weDE0NDdCN0VEMkY2Nj"
            "U3MkJCRDEzMDZDRTdDRjM2MTBELFVSST0iZGF0YTp0ZXh0L3BsYWluO2Jhc2U2NCxB"
            "QUFBb25CemMyZ0FBQUFBN2UrTHFYbldTczZqeUNmYzFSMGg3UUFBQUlJU0VCUkh0Kz"
            "B2WmxjcnZSTUd6bnp6WVEwU0VGckdvUjZxTDE3VnYyYU1RQnlCTk1vU0VHN2hOUmJJ"
            "NTFoN3JwOSt6VDZab200U0VQbnNFcVlhSmwxSGo0TXpUanA0MHNjU0VBM0Q3RTkyZz"
            "FTTGdlYzhaT1dDNFRZYURYZHBaR1YyYVc1bFgzUmxjM1FpRVhWdWFXWnBaV1F0YzNS"
            "eVpXRnRhVzVuU09QY2xac0ciLEtFWUZPUk1BVD0idXJuOnV1aWQ6ZWRlZjhiYTktNz"
            "lkNi00YWNlLWEzYzgtMjdkY2Q1MWQyMWVkIixLRVlGT1JNQVRWRVJTSU9OUz0iMSIK"
            )
    )

    assert drm_system.kid == UUID("1447B7ED-2F66-572B-BD13-06CE7CF3610D")
    assert drm_system.system_id == UUID("edef8ba9-79d6-4ace-a3c8-27dcd51d21ed")

    xml = etree.tostring(drm_system.element())

    assert xml == (
        b'<DRMSystem kid="1447b7ed-2f66-572b-bd13-06ce7cf3610d" systemId="edef8ba9-79d6-4ace-a3c8-27dcd51d21ed"><PSSH>AAAAxnBzc2gBAAAA7e+LqXnWSs6jyCfc1R0h7QAAAAINw+xPdoNUi4HnPGTlguE2FEe37S9mVyu9EwbOfPNhDQAAAIISEBRHt+0vZlcrvRMGznzzYQ0SEFrGoR6qL17Vv2aMQByBNMoSEG7hNRbI51h7rp9+zT6Zom4SEPnsEqYaJl1Hj4MzTjp40scSEA3D7E92g1SLgec8ZOWC4TYaDXdpZGV2aW5lX3Rlc3QiEXVuaWZpZWQtc3RyZWFtaW5nSOPclZsG</PSSH><ContentProtectionData>PCEtLSBXaWRldmluZSAtLT4KPENvbnRlbnRQcm90ZWN0aW9uCiAgeG1sbnM9InVybjptcGVnOmRhc2g6c2NoZW1hOm1wZDoyMDExIgogIHhtbG5zOmNlbmM9InVybjptcGVnOmNlbmM6MjAxMyIKICBzY2hlbWVJZFVyaT0idXJuOnV1aWQ6RURFRjhCQTktNzlENi00QUNFLUEzQzgtMjdEQ0Q1MUQyMUVEIj4KICA8Y2VuYzpwc3NoPkFBQUF4bkJ6YzJnQkFBQUE3ZStMcVhuV1NzNmp5Q2ZjMVIwaDdRQUFBQUlOdyt4UGRvTlVpNEhuUEdUbGd1RTJGRWUzN1M5bVZ5dTlFd2JPZlBOaERRQUFBSUlTRUJSSHQrMHZabGNydlJNR3puenpZUTBTRUZyR29SNnFMMTdWdjJhTVFCeUJOTW9TRUc3aE5SYkk1MWg3cnA5K3pUNlpvbTRTRVBuc0VxWWFKbDFIajRNelRqcDQwc2NTRUEzRDdFOTJnMVNMZ2VjOFpPV0M0VFlhRFhkcFpHVjJhVzVsWDNSbGMzUWlFWFZ1YVdacFpXUXRjM1J5WldGdGFXNW5TT1BjbFpzRzwvY2VuYzpwc3NoPgo8L0NvbnRlbnRQcm90ZWN0aW9uPg==</ContentProtectionData><HLSSignalingData>I0VYVC1YLUtFWTpNRVRIT0Q9U0FNUExFLUFFUyxLRVlJRD0weDE0NDdCN0VEMkY2NjU3MkJCRDEzMDZDRTdDRjM2MTBELFVSST0iZGF0YTp0ZXh0L3BsYWluO2Jhc2U2NCxBQUFBb25CemMyZ0FBQUFBN2UrTHFYbldTczZqeUNmYzFSMGg3UUFBQUlJU0VCUkh0KzB2WmxjcnZSTUd6bnp6WVEwU0VGckdvUjZxTDE3VnYyYU1RQnlCTk1vU0VHN2hOUmJJNTFoN3JwOSt6VDZab200U0VQbnNFcVlhSmwxSGo0TXpUanA0MHNjU0VBM0Q3RTkyZzFTTGdlYzhaT1dDNFRZYURYZHBaR1YyYVc1bFgzUmxjM1FpRVhWdWFXWnBaV1F0YzNSeVpXRnRhVzVuU09QY2xac0ciLEtFWUZPUk1BVD0idXJuOnV1aWQ6ZWRlZjhiYTktNzlkNi00YWNlLWEzYzgtMjdkY2Q1MWQyMWVkIixLRVlGT1JNQVRWRVJTSU9OUz0iMSIK</HLSSignalingData></DRMSystem>')


def test_content_key_kid_str():
    content_key = cpix.ContentKey(
        kid="0DC3EC4F-7683-548B-81E7-3C64E582E136",
        cek="WADwG2qCqkq5TVml+U5PXw=="
    )

    assert content_key.kid == UUID("0DC3EC4F-7683-548B-81E7-3C64E582E136")
    assert content_key.cek == "WADwG2qCqkq5TVml+U5PXw=="

    xml = etree.tostring(content_key.element())

    assert xml == (
        b'<ContentKey xmlns:pskc="urn:ietf:params:xml:ns:keyprov:pskc" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns="urn:dashif:org:cpix" kid="0dc3ec4f-7683-548b-81e7-3c64e582e136"><Data><pskc:Secret><pskc:PlainValue>WADwG2qCqkq5TVml+U5PXw==</pskc:PlainValue></pskc:Secret></Data></ContentKey>')


def test_content_key_kid_uuid():
    content_key = cpix.ContentKey(
        kid=UUID("0DC3EC4F-7683-548B-81E7-3C64E582E136"),
        cek="WADwG2qCqkq5TVml+U5PXw=="
    )

    assert content_key.kid == UUID("0DC3EC4F-7683-548B-81E7-3C64E582E136")
    assert content_key.cek == "WADwG2qCqkq5TVml+U5PXw=="

    xml = etree.tostring(content_key.element())

    assert xml == (
        b'<ContentKey xmlns:pskc="urn:ietf:params:xml:ns:keyprov:pskc" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns="urn:dashif:org:cpix" kid="0dc3ec4f-7683-548b-81e7-3c64e582e136"><Data><pskc:Secret><pskc:PlainValue>WADwG2qCqkq5TVml+U5PXw==</pskc:PlainValue></pskc:Secret></Data></ContentKey>')



def test_content_key_list_foo():
    content_key_list = cpix.ContentKeyList(
        cpix.ContentKey(
            kid="0DC3EC4F-7683-548B-81E7-3C64E582E136",
            cek="WADwG2qCqkq5TVml+U5PXw=="
        ),
        cpix.ContentKey(
            kid="1447B7ED-2F66-572B-BD13-06CE7CF3610D",
            cek="ydugVLA+K017XoGM4mjxvA=="
        )
    )

    assert len(content_key_list) == 2

    xml = etree.tostring(content_key_list.element())

    assert xml == (
        b'<ContentKeyList xmlns:pskc="urn:ietf:params:xml:ns:keyprov:pskc" xmln'
        b's:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns="urn:dashif:o'
        b'rg:cpix"><ContentKey kid="0dc3ec4f-7683-548b-81e7-3c64e582e136"><Data'
        b'><pskc:Secret><pskc:PlainValue>WADwG2qCqkq5TVml+U5PXw==</pskc:PlainVa'
        b'lue></pskc:Secret></Data></ContentKey><ContentKey kid="1447b7ed-2f66-'
        b'572b-bd13-06ce7cf3610d"><Data><pskc:Secret><pskc:PlainValue>ydugVLA+K'
        b'017XoGM4mjxvA==</pskc:PlainValue></pskc:Secret></Data></ContentKey></'
        b'ContentKeyList>')


def test_content_key_list_append():
    content_key_list = cpix.ContentKeyList()

    assert len(content_key_list) == 0

    content_key = cpix.ContentKey(
        kid="0DC3EC4F-7683-548B-81E7-3C64E582E136",
        cek="WADwG2qCqkq5TVml+U5PXw=="
    )

    content_key_list.append(content_key)

    assert len(content_key_list) == 1

    xml = etree.tostring(content_key_list.element())

    assert xml == b'<ContentKeyList xmlns:pskc="urn:ietf:params:xml:ns:keyprov:pskc" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns="urn:dashif:org:cpix"><ContentKey kid="0dc3ec4f-7683-548b-81e7-3c64e582e136"><Data><pskc:Secret><pskc:PlainValue>WADwG2qCqkq5TVml+U5PXw==</pskc:PlainValue></pskc:Secret></Data></ContentKey></ContentKeyList>'


def test_content_key_list_delete():
    content_key_list = cpix.ContentKeyList(
        cpix.ContentKey(
            kid="0DC3EC4F-7683-548B-81E7-3C64E582E136",
            cek="WADwG2qCqkq5TVml+U5PXw=="
        ),
        cpix.ContentKey(
            kid="1447B7ED-2F66-572B-BD13-06CE7CF3610D",
            cek="ydugVLA+K017XoGM4mjxvA=="
        )
    )

    assert len(content_key_list) == 2

    xml = etree.tostring(content_key_list.element())

    assert xml == (
        b'<ContentKeyList xmlns:pskc="urn:ietf:params:xml:ns:keyprov:pskc" xmln'
        b's:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns="urn:dashif:o'
        b'rg:cpix"><ContentKey kid="0dc3ec4f-7683-548b-81e7-3c64e582e136"><Data'
        b'><pskc:Secret><pskc:PlainValue>WADwG2qCqkq5TVml+U5PXw==</pskc:PlainVa'
        b'lue></pskc:Secret></Data></ContentKey><ContentKey kid="1447b7ed-2f66-'
        b'572b-bd13-06ce7cf3610d"><Data><pskc:Secret><pskc:PlainValue>ydugVLA+K'
        b'017XoGM4mjxvA==</pskc:PlainValue></pskc:Secret></Data></ContentKey></'
        b'ContentKeyList>')

    del content_key_list[1]

    assert len(content_key_list) == 1

    xml = etree.tostring(content_key_list.element())

    assert xml == b'<ContentKeyList xmlns:pskc="urn:ietf:params:xml:ns:keyprov:pskc" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns="urn:dashif:org:cpix"><ContentKey kid="0dc3ec4f-7683-548b-81e7-3c64e582e136"><Data><pskc:Secret><pskc:PlainValue>WADwG2qCqkq5TVml+U5PXw==</pskc:PlainValue></pskc:Secret></Data></ContentKey></ContentKeyList>'

def test_content_key_list_iteration():
    content_key_list = cpix.ContentKeyList(
        cpix.ContentKey(
            kid="0DC3EC4F-7683-548B-81E7-3C64E582E136",
            cek="WADwG2qCqkq5TVml+U5PXw=="
        ),
        cpix.ContentKey(
            kid="1447B7ED-2F66-572B-BD13-06CE7CF3610D",
            cek="ydugVLA+K017XoGM4mjxvA=="
        )
    )

    for content_key in content_key_list:
        assert isinstance(content_key, cpix.ContentKey)


def test_drm_system_list():
    drm_system_list = cpix.DRMSystemList(
        cpix.DRMSystem(
            kid="1447B7ED-2F66-572B-BD13-06CE7CF3610D",
            system_id="edef8ba9-79d6-4ace-a3c8-27dcd51d21ed",
            pssh=(
                "AAAAxnBzc2gBAAAA7e+LqXnWSs6jyCfc1R0h7QAAAAINw+xPdoNUi4HnPGTlguE2FE"
                "e37S9mVyu9EwbOfPNhDQAAAIISEBRHt+0vZlcrvRMGznzzYQ0SEFrGoR6qL17Vv2aM"
                "QByBNMoSEG7hNRbI51h7rp9+zT6Zom4SEPnsEqYaJl1Hj4MzTjp40scSEA3D7E92g1"
                "SLgec8ZOWC4TYaDXdpZGV2aW5lX3Rlc3QiEXVuaWZpZWQtc3RyZWFtaW5nSOPclZsG"
            ),
            content_protection_data=(
                "PCEtLSBXaWRldmluZSAtLT4KPENvbnRlbnRQcm90ZWN0aW9uCiAgeG1sbnM9InVybj"
                "ptcGVnOmRhc2g6c2NoZW1hOm1wZDoyMDExIgogIHhtbG5zOmNlbmM9InVybjptcGVn"
                "OmNlbmM6MjAxMyIKICBzY2hlbWVJZFVyaT0idXJuOnV1aWQ6RURFRjhCQTktNzlENi"
                "00QUNFLUEzQzgtMjdEQ0Q1MUQyMUVEIj4KICA8Y2VuYzpwc3NoPkFBQUF4bkJ6YzJn"
                "QkFBQUE3ZStMcVhuV1NzNmp5Q2ZjMVIwaDdRQUFBQUlOdyt4UGRvTlVpNEhuUEdUbG"
                "d1RTJGRWUzN1M5bVZ5dTlFd2JPZlBOaERRQUFBSUlTRUJSSHQrMHZabGNydlJNR3pu"
                "enpZUTBTRUZyR29SNnFMMTdWdjJhTVFCeUJOTW9TRUc3aE5SYkk1MWg3cnA5K3pUNl"
                "pvbTRTRVBuc0VxWWFKbDFIajRNelRqcDQwc2NTRUEzRDdFOTJnMVNMZ2VjOFpPV0M0"
                "VFlhRFhkcFpHVjJhVzVsWDNSbGMzUWlFWFZ1YVdacFpXUXRjM1J5WldGdGFXNW5TT1"
                "BjbFpzRzwvY2VuYzpwc3NoPgo8L0NvbnRlbnRQcm90ZWN0aW9uPg=="),
            hls_signaling_data=(
                "I0VYVC1YLUtFWTpNRVRIT0Q9U0FNUExFLUFFUyxLRVlJRD0weDE0NDdCN0VEMkY2Nj"
                "U3MkJCRDEzMDZDRTdDRjM2MTBELFVSST0iZGF0YTp0ZXh0L3BsYWluO2Jhc2U2NCxB"
                "QUFBb25CemMyZ0FBQUFBN2UrTHFYbldTczZqeUNmYzFSMGg3UUFBQUlJU0VCUkh0Kz"
                "B2WmxjcnZSTUd6bnp6WVEwU0VGckdvUjZxTDE3VnYyYU1RQnlCTk1vU0VHN2hOUmJJ"
                "NTFoN3JwOSt6VDZab200U0VQbnNFcVlhSmwxSGo0TXpUanA0MHNjU0VBM0Q3RTkyZz"
                "FTTGdlYzhaT1dDNFRZYURYZHBaR1YyYVc1bFgzUmxjM1FpRVhWdWFXWnBaV1F0YzNS"
                "eVpXRnRhVzVuU09QY2xac0ciLEtFWUZPUk1BVD0idXJuOnV1aWQ6ZWRlZjhiYTktNz"
                "lkNi00YWNlLWEzYzgtMjdkY2Q1MWQyMWVkIixLRVlGT1JNQVRWRVJTSU9OUz0iMSIK"
            )
        )
    )

    assert len(drm_system_list) == 1

    xml = etree.tostring(drm_system_list.element())

    assert xml == (
        b'<DRMSystemList><DRMSystem kid="1447b7ed-2f66-572b-bd13-06ce7cf3610d" systemId="edef8ba9-79d6-4ace-a3c8-27dcd51d21ed"><PSSH>AAAAxnBzc2gBAAAA7e+LqXnWSs6jyCfc1R0h7QAAAAINw+xPdoNUi4HnPGTlguE2FEe37S9mVyu9EwbOfPNhDQAAAIISEBRHt+0vZlcrvRMGznzzYQ0SEFrGoR6qL17Vv2aMQByBNMoSEG7hNRbI51h7rp9+zT6Zom4SEPnsEqYaJl1Hj4MzTjp40scSEA3D7E92g1SLgec8ZOWC4TYaDXdpZGV2aW5lX3Rlc3QiEXVuaWZpZWQtc3RyZWFtaW5nSOPclZsG</PSSH><ContentProtectionData>PCEtLSBXaWRldmluZSAtLT4KPENvbnRlbnRQcm90ZWN0aW9uCiAgeG1sbnM9InVybjptcGVnOmRhc2g6c2NoZW1hOm1wZDoyMDExIgogIHhtbG5zOmNlbmM9InVybjptcGVnOmNlbmM6MjAxMyIKICBzY2hlbWVJZFVyaT0idXJuOnV1aWQ6RURFRjhCQTktNzlENi00QUNFLUEzQzgtMjdEQ0Q1MUQyMUVEIj4KICA8Y2VuYzpwc3NoPkFBQUF4bkJ6YzJnQkFBQUE3ZStMcVhuV1NzNmp5Q2ZjMVIwaDdRQUFBQUlOdyt4UGRvTlVpNEhuUEdUbGd1RTJGRWUzN1M5bVZ5dTlFd2JPZlBOaERRQUFBSUlTRUJSSHQrMHZabGNydlJNR3puenpZUTBTRUZyR29SNnFMMTdWdjJhTVFCeUJOTW9TRUc3aE5SYkk1MWg3cnA5K3pUNlpvbTRTRVBuc0VxWWFKbDFIajRNelRqcDQwc2NTRUEzRDdFOTJnMVNMZ2VjOFpPV0M0VFlhRFhkcFpHVjJhVzVsWDNSbGMzUWlFWFZ1YVdacFpXUXRjM1J5WldGdGFXNW5TT1BjbFpzRzwvY2VuYzpwc3NoPgo8L0NvbnRlbnRQcm90ZWN0aW9uPg==</ContentProtectionData><HLSSignalingData>I0VYVC1YLUtFWTpNRVRIT0Q9U0FNUExFLUFFUyxLRVlJRD0weDE0NDdCN0VEMkY2NjU3MkJCRDEzMDZDRTdDRjM2MTBELFVSST0iZGF0YTp0ZXh0L3BsYWluO2Jhc2U2NCxBQUFBb25CemMyZ0FBQUFBN2UrTHFYbldTczZqeUNmYzFSMGg3UUFBQUlJU0VCUkh0KzB2WmxjcnZSTUd6bnp6WVEwU0VGckdvUjZxTDE3VnYyYU1RQnlCTk1vU0VHN2hOUmJJNTFoN3JwOSt6VDZab200U0VQbnNFcVlhSmwxSGo0TXpUanA0MHNjU0VBM0Q3RTkyZzFTTGdlYzhaT1dDNFRZYURYZHBaR1YyYVc1bFgzUmxjM1FpRVhWdWFXWnBaV1F0YzNSeVpXRnRhVzVuU09QY2xac0ciLEtFWUZPUk1BVD0idXJuOnV1aWQ6ZWRlZjhiYTktNzlkNi00YWNlLWEzYzgtMjdkY2Q1MWQyMWVkIixLRVlGT1JNQVRWRVJTSU9OUz0iMSIK</HLSSignalingData></DRMSystem></DRMSystemList>'
    )


def test_empty_cpix():
    empty_cpix = cpix.CPIX()

    assert empty_cpix.content_keys is None
    assert empty_cpix.drm_systems is None
    assert empty_cpix.usage_rules is None

    xml = etree.tostring(empty_cpix.element())

    assert xml == b'<CPIX xmlns:pskc="urn:ietf:params:xml:ns:keyprov:pskc" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns="urn:dashif:org:cpix" xsi:schemaLocation="urn:dashif:org:cpix cpix.xsd"/>'


def test_full_widevine_cpix():
    full_cpix = cpix.CPIX(
        content_keys=cpix.ContentKeyList(
            cpix.ContentKey(
                kid="0DC3EC4F-7683-548B-81E7-3C64E582E136",
                cek="WADwG2qCqkq5TVml+U5PXw=="
            ),
            cpix.ContentKey(
                kid="1447B7ED-2F66-572B-BD13-06CE7CF3610D",
                cek="ydugVLA+K017XoGM4mjxvA=="
            ),
            cpix.ContentKey(
                kid="00000000-0000-0000-0000-000000000002",
                cek="AAAAAAAAAAAAAAAAAAAAAg=="
            )
        ),
        drm_systems=cpix.DRMSystemList(
            cpix.DRMSystem(
                kid="0DC3EC4F-7683-548B-81E7-3C64E582E136",
                system_id="EDEF8BA9-79D6-4ACE-A3C8-27DCD51D21ED",
                pssh="AAAAxnBzc2gBAAAA7e+LqXnWSs6jyCfc1R0h7QAAAAINw+xPdoNUi4HnPGTlguE2FEe37S9mVyu9EwbOfPNhDQAAAIISEBRHt+0vZlcrvRMGznzzYQ0SEFrGoR6qL17Vv2aMQByBNMoSEG7hNRbI51h7rp9+zT6Zom4SEPnsEqYaJl1Hj4MzTjp40scSEA3D7E92g1SLgec8ZOWC4TYaDXdpZGV2aW5lX3Rlc3QiEXVuaWZpZWQtc3RyZWFtaW5nSOPclZsG",
                content_protection_data="PCEtLSBXaWRldmluZSAtLT4KPENvbnRlbnRQcm90ZWN0aW9uCiAgeG1sbnM9InVybjptcGVnOmRhc2g6c2NoZW1hOm1wZDoyMDExIgogIHhtbG5zOmNlbmM9InVybjptcGVnOmNlbmM6MjAxMyIKICBzY2hlbWVJZFVyaT0idXJuOnV1aWQ6RURFRjhCQTktNzlENi00QUNFLUEzQzgtMjdEQ0Q1MUQyMUVEIj4KICA8Y2VuYzpwc3NoPkFBQUF4bkJ6YzJnQkFBQUE3ZStMcVhuV1NzNmp5Q2ZjMVIwaDdRQUFBQUlOdyt4UGRvTlVpNEhuUEdUbGd1RTJGRWUzN1M5bVZ5dTlFd2JPZlBOaERRQUFBSUlTRUJSSHQrMHZabGNydlJNR3puenpZUTBTRUZyR29SNnFMMTdWdjJhTVFCeUJOTW9TRUc3aE5SYkk1MWg3cnA5K3pUNlpvbTRTRVBuc0VxWWFKbDFIajRNelRqcDQwc2NTRUEzRDdFOTJnMVNMZ2VjOFpPV0M0VFlhRFhkcFpHVjJhVzVsWDNSbGMzUWlFWFZ1YVdacFpXUXRjM1J5WldGdGFXNW5TT1BjbFpzRzwvY2VuYzpwc3NoPgo8L0NvbnRlbnRQcm90ZWN0aW9uPg==",
                hls_signaling_data="I0VYVC1YLUtFWTpNRVRIT0Q9U0FNUExFLUFFUyxLRVlJRD0weDBEQzNFQzRGNzY4MzU0OEI4MUU3M0M2NEU1ODJFMTM2LFVSST0iZGF0YTp0ZXh0L3BsYWluO2Jhc2U2NCxBQUFBb25CemMyZ0FBQUFBN2UrTHFYbldTczZqeUNmYzFSMGg3UUFBQUlJU0VCUkh0KzB2WmxjcnZSTUd6bnp6WVEwU0VGckdvUjZxTDE3VnYyYU1RQnlCTk1vU0VHN2hOUmJJNTFoN3JwOSt6VDZab200U0VQbnNFcVlhSmwxSGo0TXpUanA0MHNjU0VBM0Q3RTkyZzFTTGdlYzhaT1dDNFRZYURYZHBaR1YyYVc1bFgzUmxjM1FpRVhWdWFXWnBaV1F0YzNSeVpXRnRhVzVuU09QY2xac0ciLEtFWUZPUk1BVD0idXJuOnV1aWQ6ZWRlZjhiYTktNzlkNi00YWNlLWEzYzgtMjdkY2Q1MWQyMWVkIixLRVlGT1JNQVRWRVJTSU9OUz0iMSIK"
            ),
            cpix.DRMSystem(
                kid="1447B7ED-2F66-572B-BD13-06CE7CF3610D",
                system_id="EDEF8BA9-79D6-4ACE-A3C8-27DCD51D21ED",
                pssh="AAAAxnBzc2gBAAAA7e+LqXnWSs6jyCfc1R0h7QAAAAINw+xPdoNUi4HnPGTlguE2FEe37S9mVyu9EwbOfPNhDQAAAIISEBRHt+0vZlcrvRMGznzzYQ0SEFrGoR6qL17Vv2aMQByBNMoSEG7hNRbI51h7rp9+zT6Zom4SEPnsEqYaJl1Hj4MzTjp40scSEA3D7E92g1SLgec8ZOWC4TYaDXdpZGV2aW5lX3Rlc3QiEXVuaWZpZWQtc3RyZWFtaW5nSOPclZsG",
                content_protection_data="PCEtLSBXaWRldmluZSAtLT4KPENvbnRlbnRQcm90ZWN0aW9uCiAgeG1sbnM9InVybjptcGVnOmRhc2g6c2NoZW1hOm1wZDoyMDExIgogIHhtbG5zOmNlbmM9InVybjptcGVnOmNlbmM6MjAxMyIKICBzY2hlbWVJZFVyaT0idXJuOnV1aWQ6RURFRjhCQTktNzlENi00QUNFLUEzQzgtMjdEQ0Q1MUQyMUVEIj4KICA8Y2VuYzpwc3NoPkFBQUF4bkJ6YzJnQkFBQUE3ZStMcVhuV1NzNmp5Q2ZjMVIwaDdRQUFBQUlOdyt4UGRvTlVpNEhuUEdUbGd1RTJGRWUzN1M5bVZ5dTlFd2JPZlBOaERRQUFBSUlTRUJSSHQrMHZabGNydlJNR3puenpZUTBTRUZyR29SNnFMMTdWdjJhTVFCeUJOTW9TRUc3aE5SYkk1MWg3cnA5K3pUNlpvbTRTRVBuc0VxWWFKbDFIajRNelRqcDQwc2NTRUEzRDdFOTJnMVNMZ2VjOFpPV0M0VFlhRFhkcFpHVjJhVzVsWDNSbGMzUWlFWFZ1YVdacFpXUXRjM1J5WldGdGFXNW5TT1BjbFpzRzwvY2VuYzpwc3NoPgo8L0NvbnRlbnRQcm90ZWN0aW9uPg==",
                hls_signaling_data="I0VYVC1YLUtFWTpNRVRIT0Q9U0FNUExFLUFFUyxLRVlJRD0weDE0NDdCN0VEMkY2NjU3MkJCRDEzMDZDRTdDRjM2MTBELFVSST0iZGF0YTp0ZXh0L3BsYWluO2Jhc2U2NCxBQUFBb25CemMyZ0FBQUFBN2UrTHFYbldTczZqeUNmYzFSMGg3UUFBQUlJU0VCUkh0KzB2WmxjcnZSTUd6bnp6WVEwU0VGckdvUjZxTDE3VnYyYU1RQnlCTk1vU0VHN2hOUmJJNTFoN3JwOSt6VDZab200U0VQbnNFcVlhSmwxSGo0TXpUanA0MHNjU0VBM0Q3RTkyZzFTTGdlYzhaT1dDNFRZYURYZHBaR1YyYVc1bFgzUmxjM1FpRVhWdWFXWnBaV1F0YzNSeVpXRnRhVzVuU09QY2xac0ciLEtFWUZPUk1BVD0idXJuOnV1aWQ6ZWRlZjhiYTktNzlkNi00YWNlLWEzYzgtMjdkY2Q1MWQyMWVkIixLRVlGT1JNQVRWRVJTSU9OUz0iMSIK"
            ),
            cpix.DRMSystem(
                kid="00000000-0000-0000-0000-000000000002",
                system_id="EDEF8BA9-79D6-4ACE-A3C8-27DCD51D21ED",
                pssh="AAAAxnBzc2gBAAAA7e+LqXnWSs6jyCfc1R0h7QAAAAINw+xPdoNUi4HnPGTlguE2FEe37S9mVyu9EwbOfPNhDQAAAIISEBRHt+0vZlcrvRMGznzzYQ0SEFrGoR6qL17Vv2aMQByBNMoSEG7hNRbI51h7rp9+zT6Zom4SEPnsEqYaJl1Hj4MzTjp40scSEA3D7E92g1SLgec8ZOWC4TYaDXdpZGV2aW5lX3Rlc3QiEXVuaWZpZWQtc3RyZWFtaW5nSOPclZsG",
                content_protection_data="",
                hls_signaling_data="I0VYVC1YLUtFWTpNRVRIT0Q9U0FNUExFLUFFUyxLRVlJRD0weDE0NDdCN0VEMkY2NjU3MkJCRDEzMDZDRTdDRjM2MTBELFVSST0iZGF0YTp0ZXh0L3BsYWluO2Jhc2U2NCxBQUFBb25CemMyZ0FBQUFBN2UrTHFYbldTczZqeUNmYzFSMGg3UUFBQUlJU0VCUkh0KzB2WmxjcnZSTUd6bnp6WVEwU0VGckdvUjZxTDE3VnYyYU1RQnlCTk1vU0VHN2hOUmJJNTFoN3JwOSt6VDZab200U0VQbnNFcVlhSmwxSGo0TXpUanA0MHNjU0VBM0Q3RTkyZzFTTGdlYzhaT1dDNFRZYURYZHBaR1YyYVc1bFgzUmxjM1FpRVhWdWFXWnBaV1F0YzNSeVpXRnRhVzVuU09QY2xac0ciLEtFWUZPUk1BVD0idXJuOnV1aWQ6ZWRlZjhiYTktNzlkNi00YWNlLWEzYzgtMjdkY2Q1MWQyMWVkIixLRVlGT1JNQVRWRVJTSU9OUz0iMSIK"
            )
        ),
        usage_rules=cpix.UsageRuleList(
            cpix.UsageRule(
                kid="0DC3EC4F-7683-548B-81E7-3C64E582E136",
                filters=[cpix.AudioFilter()]
            ),
            cpix.UsageRule(
                kid="1447B7ED-2F66-572B-BD13-06CE7CF3610D",
                filters=[cpix.VideoFilter(max_pixels=38912)]
            ),
            cpix.UsageRule(
                kid="00000000-0000-0000-0000-000000000002",
                filters=[cpix.VideoFilter(min_pixels=38913)]
            )
        )
    )

    xml = etree.tostring(full_cpix.element())

    assert xml == b'<CPIX xmlns:pskc="urn:ietf:params:xml:ns:keyprov:pskc" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns="urn:dashif:org:cpix" xsi:schemaLocation="urn:dashif:org:cpix cpix.xsd"><ContentKeyList><ContentKey kid="0dc3ec4f-7683-548b-81e7-3c64e582e136"><Data><pskc:Secret><pskc:PlainValue>WADwG2qCqkq5TVml+U5PXw==</pskc:PlainValue></pskc:Secret></Data></ContentKey><ContentKey kid="1447b7ed-2f66-572b-bd13-06ce7cf3610d"><Data><pskc:Secret><pskc:PlainValue>ydugVLA+K017XoGM4mjxvA==</pskc:PlainValue></pskc:Secret></Data></ContentKey><ContentKey kid="00000000-0000-0000-0000-000000000002"><Data><pskc:Secret><pskc:PlainValue>AAAAAAAAAAAAAAAAAAAAAg==</pskc:PlainValue></pskc:Secret></Data></ContentKey></ContentKeyList><DRMSystemList><DRMSystem kid="0dc3ec4f-7683-548b-81e7-3c64e582e136" systemId="edef8ba9-79d6-4ace-a3c8-27dcd51d21ed"><PSSH>AAAAxnBzc2gBAAAA7e+LqXnWSs6jyCfc1R0h7QAAAAINw+xPdoNUi4HnPGTlguE2FEe37S9mVyu9EwbOfPNhDQAAAIISEBRHt+0vZlcrvRMGznzzYQ0SEFrGoR6qL17Vv2aMQByBNMoSEG7hNRbI51h7rp9+zT6Zom4SEPnsEqYaJl1Hj4MzTjp40scSEA3D7E92g1SLgec8ZOWC4TYaDXdpZGV2aW5lX3Rlc3QiEXVuaWZpZWQtc3RyZWFtaW5nSOPclZsG</PSSH><ContentProtectionData>PCEtLSBXaWRldmluZSAtLT4KPENvbnRlbnRQcm90ZWN0aW9uCiAgeG1sbnM9InVybjptcGVnOmRhc2g6c2NoZW1hOm1wZDoyMDExIgogIHhtbG5zOmNlbmM9InVybjptcGVnOmNlbmM6MjAxMyIKICBzY2hlbWVJZFVyaT0idXJuOnV1aWQ6RURFRjhCQTktNzlENi00QUNFLUEzQzgtMjdEQ0Q1MUQyMUVEIj4KICA8Y2VuYzpwc3NoPkFBQUF4bkJ6YzJnQkFBQUE3ZStMcVhuV1NzNmp5Q2ZjMVIwaDdRQUFBQUlOdyt4UGRvTlVpNEhuUEdUbGd1RTJGRWUzN1M5bVZ5dTlFd2JPZlBOaERRQUFBSUlTRUJSSHQrMHZabGNydlJNR3puenpZUTBTRUZyR29SNnFMMTdWdjJhTVFCeUJOTW9TRUc3aE5SYkk1MWg3cnA5K3pUNlpvbTRTRVBuc0VxWWFKbDFIajRNelRqcDQwc2NTRUEzRDdFOTJnMVNMZ2VjOFpPV0M0VFlhRFhkcFpHVjJhVzVsWDNSbGMzUWlFWFZ1YVdacFpXUXRjM1J5WldGdGFXNW5TT1BjbFpzRzwvY2VuYzpwc3NoPgo8L0NvbnRlbnRQcm90ZWN0aW9uPg==</ContentProtectionData><HLSSignalingData>I0VYVC1YLUtFWTpNRVRIT0Q9U0FNUExFLUFFUyxLRVlJRD0weDBEQzNFQzRGNzY4MzU0OEI4MUU3M0M2NEU1ODJFMTM2LFVSST0iZGF0YTp0ZXh0L3BsYWluO2Jhc2U2NCxBQUFBb25CemMyZ0FBQUFBN2UrTHFYbldTczZqeUNmYzFSMGg3UUFBQUlJU0VCUkh0KzB2WmxjcnZSTUd6bnp6WVEwU0VGckdvUjZxTDE3VnYyYU1RQnlCTk1vU0VHN2hOUmJJNTFoN3JwOSt6VDZab200U0VQbnNFcVlhSmwxSGo0TXpUanA0MHNjU0VBM0Q3RTkyZzFTTGdlYzhaT1dDNFRZYURYZHBaR1YyYVc1bFgzUmxjM1FpRVhWdWFXWnBaV1F0YzNSeVpXRnRhVzVuU09QY2xac0ciLEtFWUZPUk1BVD0idXJuOnV1aWQ6ZWRlZjhiYTktNzlkNi00YWNlLWEzYzgtMjdkY2Q1MWQyMWVkIixLRVlGT1JNQVRWRVJTSU9OUz0iMSIK</HLSSignalingData></DRMSystem><DRMSystem kid="1447b7ed-2f66-572b-bd13-06ce7cf3610d" systemId="edef8ba9-79d6-4ace-a3c8-27dcd51d21ed"><PSSH>AAAAxnBzc2gBAAAA7e+LqXnWSs6jyCfc1R0h7QAAAAINw+xPdoNUi4HnPGTlguE2FEe37S9mVyu9EwbOfPNhDQAAAIISEBRHt+0vZlcrvRMGznzzYQ0SEFrGoR6qL17Vv2aMQByBNMoSEG7hNRbI51h7rp9+zT6Zom4SEPnsEqYaJl1Hj4MzTjp40scSEA3D7E92g1SLgec8ZOWC4TYaDXdpZGV2aW5lX3Rlc3QiEXVuaWZpZWQtc3RyZWFtaW5nSOPclZsG</PSSH><ContentProtectionData>PCEtLSBXaWRldmluZSAtLT4KPENvbnRlbnRQcm90ZWN0aW9uCiAgeG1sbnM9InVybjptcGVnOmRhc2g6c2NoZW1hOm1wZDoyMDExIgogIHhtbG5zOmNlbmM9InVybjptcGVnOmNlbmM6MjAxMyIKICBzY2hlbWVJZFVyaT0idXJuOnV1aWQ6RURFRjhCQTktNzlENi00QUNFLUEzQzgtMjdEQ0Q1MUQyMUVEIj4KICA8Y2VuYzpwc3NoPkFBQUF4bkJ6YzJnQkFBQUE3ZStMcVhuV1NzNmp5Q2ZjMVIwaDdRQUFBQUlOdyt4UGRvTlVpNEhuUEdUbGd1RTJGRWUzN1M5bVZ5dTlFd2JPZlBOaERRQUFBSUlTRUJSSHQrMHZabGNydlJNR3puenpZUTBTRUZyR29SNnFMMTdWdjJhTVFCeUJOTW9TRUc3aE5SYkk1MWg3cnA5K3pUNlpvbTRTRVBuc0VxWWFKbDFIajRNelRqcDQwc2NTRUEzRDdFOTJnMVNMZ2VjOFpPV0M0VFlhRFhkcFpHVjJhVzVsWDNSbGMzUWlFWFZ1YVdacFpXUXRjM1J5WldGdGFXNW5TT1BjbFpzRzwvY2VuYzpwc3NoPgo8L0NvbnRlbnRQcm90ZWN0aW9uPg==</ContentProtectionData><HLSSignalingData>I0VYVC1YLUtFWTpNRVRIT0Q9U0FNUExFLUFFUyxLRVlJRD0weDE0NDdCN0VEMkY2NjU3MkJCRDEzMDZDRTdDRjM2MTBELFVSST0iZGF0YTp0ZXh0L3BsYWluO2Jhc2U2NCxBQUFBb25CemMyZ0FBQUFBN2UrTHFYbldTczZqeUNmYzFSMGg3UUFBQUlJU0VCUkh0KzB2WmxjcnZSTUd6bnp6WVEwU0VGckdvUjZxTDE3VnYyYU1RQnlCTk1vU0VHN2hOUmJJNTFoN3JwOSt6VDZab200U0VQbnNFcVlhSmwxSGo0TXpUanA0MHNjU0VBM0Q3RTkyZzFTTGdlYzhaT1dDNFRZYURYZHBaR1YyYVc1bFgzUmxjM1FpRVhWdWFXWnBaV1F0YzNSeVpXRnRhVzVuU09QY2xac0ciLEtFWUZPUk1BVD0idXJuOnV1aWQ6ZWRlZjhiYTktNzlkNi00YWNlLWEzYzgtMjdkY2Q1MWQyMWVkIixLRVlGT1JNQVRWRVJTSU9OUz0iMSIK</HLSSignalingData></DRMSystem><DRMSystem kid="00000000-0000-0000-0000-000000000002" systemId="edef8ba9-79d6-4ace-a3c8-27dcd51d21ed"><PSSH>AAAAxnBzc2gBAAAA7e+LqXnWSs6jyCfc1R0h7QAAAAINw+xPdoNUi4HnPGTlguE2FEe37S9mVyu9EwbOfPNhDQAAAIISEBRHt+0vZlcrvRMGznzzYQ0SEFrGoR6qL17Vv2aMQByBNMoSEG7hNRbI51h7rp9+zT6Zom4SEPnsEqYaJl1Hj4MzTjp40scSEA3D7E92g1SLgec8ZOWC4TYaDXdpZGV2aW5lX3Rlc3QiEXVuaWZpZWQtc3RyZWFtaW5nSOPclZsG</PSSH><ContentProtectionData></ContentProtectionData><HLSSignalingData>I0VYVC1YLUtFWTpNRVRIT0Q9U0FNUExFLUFFUyxLRVlJRD0weDE0NDdCN0VEMkY2NjU3MkJCRDEzMDZDRTdDRjM2MTBELFVSST0iZGF0YTp0ZXh0L3BsYWluO2Jhc2U2NCxBQUFBb25CemMyZ0FBQUFBN2UrTHFYbldTczZqeUNmYzFSMGg3UUFBQUlJU0VCUkh0KzB2WmxjcnZSTUd6bnp6WVEwU0VGckdvUjZxTDE3VnYyYU1RQnlCTk1vU0VHN2hOUmJJNTFoN3JwOSt6VDZab200U0VQbnNFcVlhSmwxSGo0TXpUanA0MHNjU0VBM0Q3RTkyZzFTTGdlYzhaT1dDNFRZYURYZHBaR1YyYVc1bFgzUmxjM1FpRVhWdWFXWnBaV1F0YzNSeVpXRnRhVzVuU09QY2xac0ciLEtFWUZPUk1BVD0idXJuOnV1aWQ6ZWRlZjhiYTktNzlkNi00YWNlLWEzYzgtMjdkY2Q1MWQyMWVkIixLRVlGT1JNQVRWRVJTSU9OUz0iMSIK</HLSSignalingData></DRMSystem></DRMSystemList><ContentKeyUsageRuleList><ContentKeyUsageRule kid="0dc3ec4f-7683-548b-81e7-3c64e582e136"><AudioFilter/></ContentKeyUsageRule><ContentKeyUsageRule kid="1447b7ed-2f66-572b-bd13-06ce7cf3610d"><VideoFilter maxPixels="38912"/></ContentKeyUsageRule><ContentKeyUsageRule kid="00000000-0000-0000-0000-000000000002"><VideoFilter minPixels="38913"/></ContentKeyUsageRule></ContentKeyUsageRuleList></CPIX>'
