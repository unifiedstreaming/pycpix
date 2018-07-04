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
        b'<ContentKeyUsageRuleType kid="fdde4136-c15c-4953-bd45-ce0f454bd130"><'
        b'VideoFilter/><AudioFilter/></ContentKeyUsageRuleType>')


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
        b'<ContentKeyUsageRuleType kid="ceb5153d-9b2c-45a0-9c8c-2bfc5e8b0d2f"><'
        b'VideoFilter hdr="true"/><VideoFilter hdr="false"/><AudioFilter/></Con'
        b'tentKeyUsageRuleType>')


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
        hls_signalling_data=(
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
        b'<DRMSystem kid="1447b7ed-2f66-572b-bd13-06ce7cf3610d" systemId="edef8'
        b'ba9-79d6-4ace-a3c8-27dcd51d21ed"><PSSH>AAAAxnBzc2gBAAAA7e+LqXnWSs6jyC'
        b'fc1R0h7QAAAAINw+xPdoNUi4HnPGTlguE2FEe37S9mVyu9EwbOfPNhDQAAAIISEBRHt+0'
        b'vZlcrvRMGznzzYQ0SEFrGoR6qL17Vv2aMQByBNMoSEG7hNRbI51h7rp9+zT6Zom4SEPns'
        b'EqYaJl1Hj4MzTjp40scSEA3D7E92g1SLgec8ZOWC4TYaDXdpZGV2aW5lX3Rlc3QiEXVua'
        b'WZpZWQtc3RyZWFtaW5nSOPclZsG</PSSH><ContentProtectionData>PCEtLSBXaWRl'
        b'dmluZSAtLT4KPENvbnRlbnRQcm90ZWN0aW9uCiAgeG1sbnM9InVybjptcGVnOmRhc2g6c'
        b'2NoZW1hOm1wZDoyMDExIgogIHhtbG5zOmNlbmM9InVybjptcGVnOmNlbmM6MjAxMyIKIC'
        b'BzY2hlbWVJZFVyaT0idXJuOnV1aWQ6RURFRjhCQTktNzlENi00QUNFLUEzQzgtMjdEQ0Q'
        b'1MUQyMUVEIj4KICA8Y2VuYzpwc3NoPkFBQUF4bkJ6YzJnQkFBQUE3ZStMcVhuV1NzNmp5'
        b'Q2ZjMVIwaDdRQUFBQUlOdyt4UGRvTlVpNEhuUEdUbGd1RTJGRWUzN1M5bVZ5dTlFd2JPZ'
        b'lBOaERRQUFBSUlTRUJSSHQrMHZabGNydlJNR3puenpZUTBTRUZyR29SNnFMMTdWdjJhTV'
        b'FCeUJOTW9TRUc3aE5SYkk1MWg3cnA5K3pUNlpvbTRTRVBuc0VxWWFKbDFIajRNelRqcDQ'
        b'wc2NTRUEzRDdFOTJnMVNMZ2VjOFpPV0M0VFlhRFhkcFpHVjJhVzVsWDNSbGMzUWlFWFZ1'
        b'YVdacFpXUXRjM1J5WldGdGFXNW5TT1BjbFpzRzwvY2VuYzpwc3NoPgo8L0NvbnRlbnRQc'
        b'm90ZWN0aW9uPg==</ContentProtectionData><HLSSignalingData>I0VYVC1YLUt'
        b'FWTpNRVRIT0Q9U0FNUExFLUFFUyxLRVlJRD0weDE0NDdCN0VEMkY2NjU3MkJCRDEzMDZD'
        b'RTdDRjM2MTBELFVSST0iZGF0YTp0ZXh0L3BsYWluO2Jhc2U2NCxBQUFBb25CemMyZ0FBQ'
        b'UFBN2UrTHFYbldTczZqeUNmYzFSMGg3UUFBQUlJU0VCUkh0KzB2WmxjcnZSTUd6bnp6WV'
        b'EwU0VGckdvUjZxTDE3VnYyYU1RQnlCTk1vU0VHN2hOUmJJNTFoN3JwOSt6VDZab200U0V'
        b'QbnNFcVlhSmwxSGo0TXpUanA0MHNjU0VBM0Q3RTkyZzFTTGdlYzhaT1dDNFRZYURYZHBa'
        b'R1YyYVc1bFgzUmxjM1FpRVhWdWFXWnBaV1F0YzNSeVpXRnRhVzVuU09QY2xac0ciLEtFW'
        b'UZPUk1BVD0idXJuOnV1aWQ6ZWRlZjhiYTktNzlkNi00YWNlLWEzYzgtMjdkY2Q1MWQyMW'
        b'VkIixLRVlGT1JNQVRWRVJTSU9OUz0iMSIK</HLSSignalingData></DRMSystem>')


def test_simple_content_key():
    content_key = cpix.ContentKey(
        kid="0DC3EC4F-7683-548B-81E7-3C64E582E136",
        cek="WADwG2qCqkq5TVml+U5PXw=="
    )

    assert content_key.kid == UUID("0DC3EC4F-7683-548B-81E7-3C64E582E136")
    assert content_key.cek == "WADwG2qCqkq5TVml+U5PXw=="

    xml = etree.tostring(content_key.element())

    assert xml == (
        b'<ContentKey xmlns:pskc="urn:ietf:params:xml:ns:keyprov:pskc" xmlns:xs'
        b'i="http://www.w3.org/2001/XMLSchema-instance" xmlns="urn:dashif:org:c'
        b'pix" kid="0dc3ec4f-7683-548b-81e7-3c64e582e136"><Data><pskc:Secret><p'
        b'skc:PlainValue>WADwG2qCqkq5TVml+U5PXw==</pskc:PlainValue></pskc:Secre'
        b't></Data></ContentKey>')



def test_content_key_list():
    content_key_list = cpix.ContentKeyList(
        content_keys=[
            cpix.ContentKey(
                kid="0DC3EC4F-7683-548B-81E7-3C64E582E136",
                cek="WADwG2qCqkq5TVml+U5PXw=="
            ),
            cpix.ContentKey(
                kid="1447B7ED-2F66-572B-BD13-06CE7CF3610D",
                cek="ydugVLA+K017XoGM4mjxvA=="
            ),
        ]
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


def test_drm_system_list():
    drm_system_list = cpix.DRMSystemList(
        drm_systems=[
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
                hls_signalling_data=(
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
        ]
    )

    assert len(drm_system_list) == 1

    xml = etree.tostring(drm_system_list.element())

    assert xml == (
        b'<DRMSystemList><DRMSystem kid="1447b7ed-2f66-572b-bd13-06ce7cf3610d" systemId="edef8ba9-79d6-4ace-a3c8-27dcd51d21ed"><PSSH>AAAAxnBzc2gBAAAA7e+LqXnWSs6jyCfc1R0h7QAAAAINw+xPdoNUi4HnPGTlguE2FEe37S9mVyu9EwbOfPNhDQAAAIISEBRHt+0vZlcrvRMGznzzYQ0SEFrGoR6qL17Vv2aMQByBNMoSEG7hNRbI51h7rp9+zT6Zom4SEPnsEqYaJl1Hj4MzTjp40scSEA3D7E92g1SLgec8ZOWC4TYaDXdpZGV2aW5lX3Rlc3QiEXVuaWZpZWQtc3RyZWFtaW5nSOPclZsG</PSSH><ContentProtectionData>PCEtLSBXaWRldmluZSAtLT4KPENvbnRlbnRQcm90ZWN0aW9uCiAgeG1sbnM9InVybjptcGVnOmRhc2g6c2NoZW1hOm1wZDoyMDExIgogIHhtbG5zOmNlbmM9InVybjptcGVnOmNlbmM6MjAxMyIKICBzY2hlbWVJZFVyaT0idXJuOnV1aWQ6RURFRjhCQTktNzlENi00QUNFLUEzQzgtMjdEQ0Q1MUQyMUVEIj4KICA8Y2VuYzpwc3NoPkFBQUF4bkJ6YzJnQkFBQUE3ZStMcVhuV1NzNmp5Q2ZjMVIwaDdRQUFBQUlOdyt4UGRvTlVpNEhuUEdUbGd1RTJGRWUzN1M5bVZ5dTlFd2JPZlBOaERRQUFBSUlTRUJSSHQrMHZabGNydlJNR3puenpZUTBTRUZyR29SNnFMMTdWdjJhTVFCeUJOTW9TRUc3aE5SYkk1MWg3cnA5K3pUNlpvbTRTRVBuc0VxWWFKbDFIajRNelRqcDQwc2NTRUEzRDdFOTJnMVNMZ2VjOFpPV0M0VFlhRFhkcFpHVjJhVzVsWDNSbGMzUWlFWFZ1YVdacFpXUXRjM1J5WldGdGFXNW5TT1BjbFpzRzwvY2VuYzpwc3NoPgo8L0NvbnRlbnRQcm90ZWN0aW9uPg==</ContentProtectionData><HLSSignalingData>I0VYVC1YLUtFWTpNRVRIT0Q9U0FNUExFLUFFUyxLRVlJRD0weDE0NDdCN0VEMkY2NjU3MkJCRDEzMDZDRTdDRjM2MTBELFVSST0iZGF0YTp0ZXh0L3BsYWluO2Jhc2U2NCxBQUFBb25CemMyZ0FBQUFBN2UrTHFYbldTczZqeUNmYzFSMGg3UUFBQUlJU0VCUkh0KzB2WmxjcnZSTUd6bnp6WVEwU0VGckdvUjZxTDE3VnYyYU1RQnlCTk1vU0VHN2hOUmJJNTFoN3JwOSt6VDZab200U0VQbnNFcVlhSmwxSGo0TXpUanA0MHNjU0VBM0Q3RTkyZzFTTGdlYzhaT1dDNFRZYURYZHBaR1YyYVc1bFgzUmxjM1FpRVhWdWFXWnBaV1F0YzNSeVpXRnRhVzVuU09QY2xac0ciLEtFWUZPUk1BVD0idXJuOnV1aWQ6ZWRlZjhiYTktNzlkNi00YWNlLWEzYzgtMjdkY2Q1MWQyMWVkIixLRVlGT1JNQVRWRVJTSU9OUz0iMSIK</HLSSignalingData></DRMSystem></DRMSystemList>'
    )


def test_full_cpix():
    full_cpix = cpix.CPIX(
        content_keys=cpix.ContentKeyList(
            content_keys=[
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
            ]
        ),
        drm_systems=cpix.DRMSystemList(
            drm_systems=[
                cpix.DRMSystem(
                    kid="0DC3EC4F-7683-548B-81E7-3C64E582E136",
                    system_id="EDEF8BA9-79D6-4ACE-A3C8-27DCD51D21ED",
                    pssh="AAAAxnBzc2gBAAAA7e+LqXnWSs6jyCfc1R0h7QAAAAINw+xPdoNUi4HnPGTlguE2FEe37S9mVyu9EwbOfPNhDQAAAIISEBRHt+0vZlcrvRMGznzzYQ0SEFrGoR6qL17Vv2aMQByBNMoSEG7hNRbI51h7rp9+zT6Zom4SEPnsEqYaJl1Hj4MzTjp40scSEA3D7E92g1SLgec8ZOWC4TYaDXdpZGV2aW5lX3Rlc3QiEXVuaWZpZWQtc3RyZWFtaW5nSOPclZsG",
                    content_protection_data="PCEtLSBXaWRldmluZSAtLT4KPENvbnRlbnRQcm90ZWN0aW9uCiAgeG1sbnM9InVybjptcGVnOmRhc2g6c2NoZW1hOm1wZDoyMDExIgogIHhtbG5zOmNlbmM9InVybjptcGVnOmNlbmM6MjAxMyIKICBzY2hlbWVJZFVyaT0idXJuOnV1aWQ6RURFRjhCQTktNzlENi00QUNFLUEzQzgtMjdEQ0Q1MUQyMUVEIj4KICA8Y2VuYzpwc3NoPkFBQUF4bkJ6YzJnQkFBQUE3ZStMcVhuV1NzNmp5Q2ZjMVIwaDdRQUFBQUlOdyt4UGRvTlVpNEhuUEdUbGd1RTJGRWUzN1M5bVZ5dTlFd2JPZlBOaERRQUFBSUlTRUJSSHQrMHZabGNydlJNR3puenpZUTBTRUZyR29SNnFMMTdWdjJhTVFCeUJOTW9TRUc3aE5SYkk1MWg3cnA5K3pUNlpvbTRTRVBuc0VxWWFKbDFIajRNelRqcDQwc2NTRUEzRDdFOTJnMVNMZ2VjOFpPV0M0VFlhRFhkcFpHVjJhVzVsWDNSbGMzUWlFWFZ1YVdacFpXUXRjM1J5WldGdGFXNW5TT1BjbFpzRzwvY2VuYzpwc3NoPgo8L0NvbnRlbnRQcm90ZWN0aW9uPg==",
                    hls_signalling_data="I0VYVC1YLUtFWTpNRVRIT0Q9U0FNUExFLUFFUyxLRVlJRD0weDBEQzNFQzRGNzY4MzU0OEI4MUU3M0M2NEU1ODJFMTM2LFVSST0iZGF0YTp0ZXh0L3BsYWluO2Jhc2U2NCxBQUFBb25CemMyZ0FBQUFBN2UrTHFYbldTczZqeUNmYzFSMGg3UUFBQUlJU0VCUkh0KzB2WmxjcnZSTUd6bnp6WVEwU0VGckdvUjZxTDE3VnYyYU1RQnlCTk1vU0VHN2hOUmJJNTFoN3JwOSt6VDZab200U0VQbnNFcVlhSmwxSGo0TXpUanA0MHNjU0VBM0Q3RTkyZzFTTGdlYzhaT1dDNFRZYURYZHBaR1YyYVc1bFgzUmxjM1FpRVhWdWFXWnBaV1F0YzNSeVpXRnRhVzVuU09QY2xac0ciLEtFWUZPUk1BVD0idXJuOnV1aWQ6ZWRlZjhiYTktNzlkNi00YWNlLWEzYzgtMjdkY2Q1MWQyMWVkIixLRVlGT1JNQVRWRVJTSU9OUz0iMSIK"
                ),
                cpix.DRMSystem(
                    kid="1447B7ED-2F66-572B-BD13-06CE7CF3610D",
                    system_id="EDEF8BA9-79D6-4ACE-A3C8-27DCD51D21ED",
                    pssh="AAAAxnBzc2gBAAAA7e+LqXnWSs6jyCfc1R0h7QAAAAINw+xPdoNUi4HnPGTlguE2FEe37S9mVyu9EwbOfPNhDQAAAIISEBRHt+0vZlcrvRMGznzzYQ0SEFrGoR6qL17Vv2aMQByBNMoSEG7hNRbI51h7rp9+zT6Zom4SEPnsEqYaJl1Hj4MzTjp40scSEA3D7E92g1SLgec8ZOWC4TYaDXdpZGV2aW5lX3Rlc3QiEXVuaWZpZWQtc3RyZWFtaW5nSOPclZsG",
                    content_protection_data="PCEtLSBXaWRldmluZSAtLT4KPENvbnRlbnRQcm90ZWN0aW9uCiAgeG1sbnM9InVybjptcGVnOmRhc2g6c2NoZW1hOm1wZDoyMDExIgogIHhtbG5zOmNlbmM9InVybjptcGVnOmNlbmM6MjAxMyIKICBzY2hlbWVJZFVyaT0idXJuOnV1aWQ6RURFRjhCQTktNzlENi00QUNFLUEzQzgtMjdEQ0Q1MUQyMUVEIj4KICA8Y2VuYzpwc3NoPkFBQUF4bkJ6YzJnQkFBQUE3ZStMcVhuV1NzNmp5Q2ZjMVIwaDdRQUFBQUlOdyt4UGRvTlVpNEhuUEdUbGd1RTJGRWUzN1M5bVZ5dTlFd2JPZlBOaERRQUFBSUlTRUJSSHQrMHZabGNydlJNR3puenpZUTBTRUZyR29SNnFMMTdWdjJhTVFCeUJOTW9TRUc3aE5SYkk1MWg3cnA5K3pUNlpvbTRTRVBuc0VxWWFKbDFIajRNelRqcDQwc2NTRUEzRDdFOTJnMVNMZ2VjOFpPV0M0VFlhRFhkcFpHVjJhVzVsWDNSbGMzUWlFWFZ1YVdacFpXUXRjM1J5WldGdGFXNW5TT1BjbFpzRzwvY2VuYzpwc3NoPgo8L0NvbnRlbnRQcm90ZWN0aW9uPg==",
                    hls_signalling_data="I0VYVC1YLUtFWTpNRVRIT0Q9U0FNUExFLUFFUyxLRVlJRD0weDE0NDdCN0VEMkY2NjU3MkJCRDEzMDZDRTdDRjM2MTBELFVSST0iZGF0YTp0ZXh0L3BsYWluO2Jhc2U2NCxBQUFBb25CemMyZ0FBQUFBN2UrTHFYbldTczZqeUNmYzFSMGg3UUFBQUlJU0VCUkh0KzB2WmxjcnZSTUd6bnp6WVEwU0VGckdvUjZxTDE3VnYyYU1RQnlCTk1vU0VHN2hOUmJJNTFoN3JwOSt6VDZab200U0VQbnNFcVlhSmwxSGo0TXpUanA0MHNjU0VBM0Q3RTkyZzFTTGdlYzhaT1dDNFRZYURYZHBaR1YyYVc1bFgzUmxjM1FpRVhWdWFXWnBaV1F0YzNSeVpXRnRhVzVuU09QY2xac0ciLEtFWUZPUk1BVD0idXJuOnV1aWQ6ZWRlZjhiYTktNzlkNi00YWNlLWEzYzgtMjdkY2Q1MWQyMWVkIixLRVlGT1JNQVRWRVJTSU9OUz0iMSIK"
                ),
                cpix.DRMSystem(
                    kid="00000000-0000-0000-0000-000000000002",
                    system_id="EDEF8BA9-79D6-4ACE-A3C8-27DCD51D21ED",
                    pssh="AAAAxnBzc2gBAAAA7e+LqXnWSs6jyCfc1R0h7QAAAAINw+xPdoNUi4HnPGTlguE2FEe37S9mVyu9EwbOfPNhDQAAAIISEBRHt+0vZlcrvRMGznzzYQ0SEFrGoR6qL17Vv2aMQByBNMoSEG7hNRbI51h7rp9+zT6Zom4SEPnsEqYaJl1Hj4MzTjp40scSEA3D7E92g1SLgec8ZOWC4TYaDXdpZGV2aW5lX3Rlc3QiEXVuaWZpZWQtc3RyZWFtaW5nSOPclZsG",
                    content_protection_data="",
                    hls_signalling_data="I0VYVC1YLUtFWTpNRVRIT0Q9U0FNUExFLUFFUyxLRVlJRD0weDE0NDdCN0VEMkY2NjU3MkJCRDEzMDZDRTdDRjM2MTBELFVSST0iZGF0YTp0ZXh0L3BsYWluO2Jhc2U2NCxBQUFBb25CemMyZ0FBQUFBN2UrTHFYbldTczZqeUNmYzFSMGg3UUFBQUlJU0VCUkh0KzB2WmxjcnZSTUd6bnp6WVEwU0VGckdvUjZxTDE3VnYyYU1RQnlCTk1vU0VHN2hOUmJJNTFoN3JwOSt6VDZab200U0VQbnNFcVlhSmwxSGo0TXpUanA0MHNjU0VBM0Q3RTkyZzFTTGdlYzhaT1dDNFRZYURYZHBaR1YyYVc1bFgzUmxjM1FpRVhWdWFXWnBaV1F0YzNSeVpXRnRhVzVuU09QY2xac0ciLEtFWUZPUk1BVD0idXJuOnV1aWQ6ZWRlZjhiYTktNzlkNi00YWNlLWEzYzgtMjdkY2Q1MWQyMWVkIixLRVlGT1JNQVRWRVJTSU9OUz0iMSIK"
                )
            ]
        ),
        usage_rules=cpix.UsageRuleList(
            usage_rules=[
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
            ]
        )
    )

    xml = etree.tostring(full_cpix.element())

    assert xml == b'<CPIX xmlns:pskc="urn:ietf:params:xml:ns:keyprov:pskc" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns="urn:dashif:org:cpix" xsi:schemaLocation="urn:dashif:org:cpix cpix.xsd"><ContentKeyList><ContentKey kid="0dc3ec4f-7683-548b-81e7-3c64e582e136"><Data><pskc:Secret><pskc:PlainValue>WADwG2qCqkq5TVml+U5PXw==</pskc:PlainValue></pskc:Secret></Data></ContentKey><ContentKey kid="1447b7ed-2f66-572b-bd13-06ce7cf3610d"><Data><pskc:Secret><pskc:PlainValue>ydugVLA+K017XoGM4mjxvA==</pskc:PlainValue></pskc:Secret></Data></ContentKey><ContentKey kid="00000000-0000-0000-0000-000000000002"><Data><pskc:Secret><pskc:PlainValue>AAAAAAAAAAAAAAAAAAAAAg==</pskc:PlainValue></pskc:Secret></Data></ContentKey></ContentKeyList><DRMSystemList><DRMSystem kid="0dc3ec4f-7683-548b-81e7-3c64e582e136" systemId="edef8ba9-79d6-4ace-a3c8-27dcd51d21ed"><PSSH>AAAAxnBzc2gBAAAA7e+LqXnWSs6jyCfc1R0h7QAAAAINw+xPdoNUi4HnPGTlguE2FEe37S9mVyu9EwbOfPNhDQAAAIISEBRHt+0vZlcrvRMGznzzYQ0SEFrGoR6qL17Vv2aMQByBNMoSEG7hNRbI51h7rp9+zT6Zom4SEPnsEqYaJl1Hj4MzTjp40scSEA3D7E92g1SLgec8ZOWC4TYaDXdpZGV2aW5lX3Rlc3QiEXVuaWZpZWQtc3RyZWFtaW5nSOPclZsG</PSSH><ContentProtectionData>PCEtLSBXaWRldmluZSAtLT4KPENvbnRlbnRQcm90ZWN0aW9uCiAgeG1sbnM9InVybjptcGVnOmRhc2g6c2NoZW1hOm1wZDoyMDExIgogIHhtbG5zOmNlbmM9InVybjptcGVnOmNlbmM6MjAxMyIKICBzY2hlbWVJZFVyaT0idXJuOnV1aWQ6RURFRjhCQTktNzlENi00QUNFLUEzQzgtMjdEQ0Q1MUQyMUVEIj4KICA8Y2VuYzpwc3NoPkFBQUF4bkJ6YzJnQkFBQUE3ZStMcVhuV1NzNmp5Q2ZjMVIwaDdRQUFBQUlOdyt4UGRvTlVpNEhuUEdUbGd1RTJGRWUzN1M5bVZ5dTlFd2JPZlBOaERRQUFBSUlTRUJSSHQrMHZabGNydlJNR3puenpZUTBTRUZyR29SNnFMMTdWdjJhTVFCeUJOTW9TRUc3aE5SYkk1MWg3cnA5K3pUNlpvbTRTRVBuc0VxWWFKbDFIajRNelRqcDQwc2NTRUEzRDdFOTJnMVNMZ2VjOFpPV0M0VFlhRFhkcFpHVjJhVzVsWDNSbGMzUWlFWFZ1YVdacFpXUXRjM1J5WldGdGFXNW5TT1BjbFpzRzwvY2VuYzpwc3NoPgo8L0NvbnRlbnRQcm90ZWN0aW9uPg==</ContentProtectionData><HLSSignalingData>I0VYVC1YLUtFWTpNRVRIT0Q9U0FNUExFLUFFUyxLRVlJRD0weDBEQzNFQzRGNzY4MzU0OEI4MUU3M0M2NEU1ODJFMTM2LFVSST0iZGF0YTp0ZXh0L3BsYWluO2Jhc2U2NCxBQUFBb25CemMyZ0FBQUFBN2UrTHFYbldTczZqeUNmYzFSMGg3UUFBQUlJU0VCUkh0KzB2WmxjcnZSTUd6bnp6WVEwU0VGckdvUjZxTDE3VnYyYU1RQnlCTk1vU0VHN2hOUmJJNTFoN3JwOSt6VDZab200U0VQbnNFcVlhSmwxSGo0TXpUanA0MHNjU0VBM0Q3RTkyZzFTTGdlYzhaT1dDNFRZYURYZHBaR1YyYVc1bFgzUmxjM1FpRVhWdWFXWnBaV1F0YzNSeVpXRnRhVzVuU09QY2xac0ciLEtFWUZPUk1BVD0idXJuOnV1aWQ6ZWRlZjhiYTktNzlkNi00YWNlLWEzYzgtMjdkY2Q1MWQyMWVkIixLRVlGT1JNQVRWRVJTSU9OUz0iMSIK</HLSSignalingData></DRMSystem><DRMSystem kid="1447b7ed-2f66-572b-bd13-06ce7cf3610d" systemId="edef8ba9-79d6-4ace-a3c8-27dcd51d21ed"><PSSH>AAAAxnBzc2gBAAAA7e+LqXnWSs6jyCfc1R0h7QAAAAINw+xPdoNUi4HnPGTlguE2FEe37S9mVyu9EwbOfPNhDQAAAIISEBRHt+0vZlcrvRMGznzzYQ0SEFrGoR6qL17Vv2aMQByBNMoSEG7hNRbI51h7rp9+zT6Zom4SEPnsEqYaJl1Hj4MzTjp40scSEA3D7E92g1SLgec8ZOWC4TYaDXdpZGV2aW5lX3Rlc3QiEXVuaWZpZWQtc3RyZWFtaW5nSOPclZsG</PSSH><ContentProtectionData>PCEtLSBXaWRldmluZSAtLT4KPENvbnRlbnRQcm90ZWN0aW9uCiAgeG1sbnM9InVybjptcGVnOmRhc2g6c2NoZW1hOm1wZDoyMDExIgogIHhtbG5zOmNlbmM9InVybjptcGVnOmNlbmM6MjAxMyIKICBzY2hlbWVJZFVyaT0idXJuOnV1aWQ6RURFRjhCQTktNzlENi00QUNFLUEzQzgtMjdEQ0Q1MUQyMUVEIj4KICA8Y2VuYzpwc3NoPkFBQUF4bkJ6YzJnQkFBQUE3ZStMcVhuV1NzNmp5Q2ZjMVIwaDdRQUFBQUlOdyt4UGRvTlVpNEhuUEdUbGd1RTJGRWUzN1M5bVZ5dTlFd2JPZlBOaERRQUFBSUlTRUJSSHQrMHZabGNydlJNR3puenpZUTBTRUZyR29SNnFMMTdWdjJhTVFCeUJOTW9TRUc3aE5SYkk1MWg3cnA5K3pUNlpvbTRTRVBuc0VxWWFKbDFIajRNelRqcDQwc2NTRUEzRDdFOTJnMVNMZ2VjOFpPV0M0VFlhRFhkcFpHVjJhVzVsWDNSbGMzUWlFWFZ1YVdacFpXUXRjM1J5WldGdGFXNW5TT1BjbFpzRzwvY2VuYzpwc3NoPgo8L0NvbnRlbnRQcm90ZWN0aW9uPg==</ContentProtectionData><HLSSignalingData>I0VYVC1YLUtFWTpNRVRIT0Q9U0FNUExFLUFFUyxLRVlJRD0weDE0NDdCN0VEMkY2NjU3MkJCRDEzMDZDRTdDRjM2MTBELFVSST0iZGF0YTp0ZXh0L3BsYWluO2Jhc2U2NCxBQUFBb25CemMyZ0FBQUFBN2UrTHFYbldTczZqeUNmYzFSMGg3UUFBQUlJU0VCUkh0KzB2WmxjcnZSTUd6bnp6WVEwU0VGckdvUjZxTDE3VnYyYU1RQnlCTk1vU0VHN2hOUmJJNTFoN3JwOSt6VDZab200U0VQbnNFcVlhSmwxSGo0TXpUanA0MHNjU0VBM0Q3RTkyZzFTTGdlYzhaT1dDNFRZYURYZHBaR1YyYVc1bFgzUmxjM1FpRVhWdWFXWnBaV1F0YzNSeVpXRnRhVzVuU09QY2xac0ciLEtFWUZPUk1BVD0idXJuOnV1aWQ6ZWRlZjhiYTktNzlkNi00YWNlLWEzYzgtMjdkY2Q1MWQyMWVkIixLRVlGT1JNQVRWRVJTSU9OUz0iMSIK</HLSSignalingData></DRMSystem><DRMSystem kid="00000000-0000-0000-0000-000000000002" systemId="edef8ba9-79d6-4ace-a3c8-27dcd51d21ed"><PSSH>AAAAxnBzc2gBAAAA7e+LqXnWSs6jyCfc1R0h7QAAAAINw+xPdoNUi4HnPGTlguE2FEe37S9mVyu9EwbOfPNhDQAAAIISEBRHt+0vZlcrvRMGznzzYQ0SEFrGoR6qL17Vv2aMQByBNMoSEG7hNRbI51h7rp9+zT6Zom4SEPnsEqYaJl1Hj4MzTjp40scSEA3D7E92g1SLgec8ZOWC4TYaDXdpZGV2aW5lX3Rlc3QiEXVuaWZpZWQtc3RyZWFtaW5nSOPclZsG</PSSH><ContentProtectionData></ContentProtectionData><HLSSignalingData>I0VYVC1YLUtFWTpNRVRIT0Q9U0FNUExFLUFFUyxLRVlJRD0weDE0NDdCN0VEMkY2NjU3MkJCRDEzMDZDRTdDRjM2MTBELFVSST0iZGF0YTp0ZXh0L3BsYWluO2Jhc2U2NCxBQUFBb25CemMyZ0FBQUFBN2UrTHFYbldTczZqeUNmYzFSMGg3UUFBQUlJU0VCUkh0KzB2WmxjcnZSTUd6bnp6WVEwU0VGckdvUjZxTDE3VnYyYU1RQnlCTk1vU0VHN2hOUmJJNTFoN3JwOSt6VDZab200U0VQbnNFcVlhSmwxSGo0TXpUanA0MHNjU0VBM0Q3RTkyZzFTTGdlYzhaT1dDNFRZYURYZHBaR1YyYVc1bFgzUmxjM1FpRVhWdWFXWnBaV1F0YzNSeVpXRnRhVzVuU09QY2xac0ciLEtFWUZPUk1BVD0idXJuOnV1aWQ6ZWRlZjhiYTktNzlkNi00YWNlLWEzYzgtMjdkY2Q1MWQyMWVkIixLRVlGT1JNQVRWRVJTSU9OUz0iMSIK</HLSSignalingData></DRMSystem></DRMSystemList><UsageRuleList><ContentKeyUsageRuleType kid="0DC3EC4F-7683-548B-81E7-3C64E582E136"><AudioFilter/></ContentKeyUsageRuleType><ContentKeyUsageRuleType kid="1447B7ED-2F66-572B-BD13-06CE7CF3610D"><VideoFilter maxPixels="38912"/></ContentKeyUsageRuleType><ContentKeyUsageRuleType kid="00000000-0000-0000-0000-000000000002"><VideoFilter minPixels="38913"/></ContentKeyUsageRuleType></UsageRuleList></CPIX>'
