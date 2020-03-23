import pytest
import cpix
import isodate
from lxml import etree
from uuid import UUID


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
            "BjbFpzRzwvY2VuYzpwc3NoPgo8L0NvbnRlbnRQcm90ZWN0aW9uPg=="
        ),
        hls_signaling_data=(
            "I0VYVC1YLUtFWTpNRVRIT0Q9U0FNUExFLUFFUyxLRVlJRD0weDE0NDdCN0VEMkY2Nj"
            "U3MkJCRDEzMDZDRTdDRjM2MTBELFVSST0iZGF0YTp0ZXh0L3BsYWluO2Jhc2U2NCxB"
            "QUFBb25CemMyZ0FBQUFBN2UrTHFYbldTczZqeUNmYzFSMGg3UUFBQUlJU0VCUkh0Kz"
            "B2WmxjcnZSTUd6bnp6WVEwU0VGckdvUjZxTDE3VnYyYU1RQnlCTk1vU0VHN2hOUmJJ"
            "NTFoN3JwOSt6VDZab200U0VQbnNFcVlhSmwxSGo0TXpUanA0MHNjU0VBM0Q3RTkyZz"
            "FTTGdlYzhaT1dDNFRZYURYZHBaR1YyYVc1bFgzUmxjM1FpRVhWdWFXWnBaV1F0YzNS"
            "eVpXRnRhVzVuU09QY2xac0ciLEtFWUZPUk1BVD0idXJuOnV1aWQ6ZWRlZjhiYTktNz"
            "lkNi00YWNlLWEzYzgtMjdkY2Q1MWQyMWVkIixLRVlGT1JNQVRWRVJTSU9OUz0iMSIK"
        ),
    )

    assert drm_system.kid == UUID("1447B7ED-2F66-572B-BD13-06CE7CF3610D")
    assert drm_system.system_id == UUID("edef8ba9-79d6-4ace-a3c8-27dcd51d21ed")

    xml = etree.tostring(drm_system.element())

    assert xml == (
        b'<DRMSystem kid="1447b7ed-2f66-572b-bd13-06ce7cf3610d" systemId="edef8ba9-79d6-4ace-a3c8-27dcd51d21ed"><PSSH>AAAAxnBzc2gBAAAA7e+LqXnWSs6jyCfc1R0h7QAAAAINw+xPdoNUi4HnPGTlguE2FEe37S9mVyu9EwbOfPNhDQAAAIISEBRHt+0vZlcrvRMGznzzYQ0SEFrGoR6qL17Vv2aMQByBNMoSEG7hNRbI51h7rp9+zT6Zom4SEPnsEqYaJl1Hj4MzTjp40scSEA3D7E92g1SLgec8ZOWC4TYaDXdpZGV2aW5lX3Rlc3QiEXVuaWZpZWQtc3RyZWFtaW5nSOPclZsG</PSSH><ContentProtectionData>PCEtLSBXaWRldmluZSAtLT4KPENvbnRlbnRQcm90ZWN0aW9uCiAgeG1sbnM9InVybjptcGVnOmRhc2g6c2NoZW1hOm1wZDoyMDExIgogIHhtbG5zOmNlbmM9InVybjptcGVnOmNlbmM6MjAxMyIKICBzY2hlbWVJZFVyaT0idXJuOnV1aWQ6RURFRjhCQTktNzlENi00QUNFLUEzQzgtMjdEQ0Q1MUQyMUVEIj4KICA8Y2VuYzpwc3NoPkFBQUF4bkJ6YzJnQkFBQUE3ZStMcVhuV1NzNmp5Q2ZjMVIwaDdRQUFBQUlOdyt4UGRvTlVpNEhuUEdUbGd1RTJGRWUzN1M5bVZ5dTlFd2JPZlBOaERRQUFBSUlTRUJSSHQrMHZabGNydlJNR3puenpZUTBTRUZyR29SNnFMMTdWdjJhTVFCeUJOTW9TRUc3aE5SYkk1MWg3cnA5K3pUNlpvbTRTRVBuc0VxWWFKbDFIajRNelRqcDQwc2NTRUEzRDdFOTJnMVNMZ2VjOFpPV0M0VFlhRFhkcFpHVjJhVzVsWDNSbGMzUWlFWFZ1YVdacFpXUXRjM1J5WldGdGFXNW5TT1BjbFpzRzwvY2VuYzpwc3NoPgo8L0NvbnRlbnRQcm90ZWN0aW9uPg==</ContentProtectionData><HLSSignalingData playlist="media">I0VYVC1YLUtFWTpNRVRIT0Q9U0FNUExFLUFFUyxLRVlJRD0weDE0NDdCN0VEMkY2NjU3MkJCRDEzMDZDRTdDRjM2MTBELFVSST0iZGF0YTp0ZXh0L3BsYWluO2Jhc2U2NCxBQUFBb25CemMyZ0FBQUFBN2UrTHFYbldTczZqeUNmYzFSMGg3UUFBQUlJU0VCUkh0KzB2WmxjcnZSTUd6bnp6WVEwU0VGckdvUjZxTDE3VnYyYU1RQnlCTk1vU0VHN2hOUmJJNTFoN3JwOSt6VDZab200U0VQbnNFcVlhSmwxSGo0TXpUanA0MHNjU0VBM0Q3RTkyZzFTTGdlYzhaT1dDNFRZYURYZHBaR1YyYVc1bFgzUmxjM1FpRVhWdWFXWnBaV1F0YzNSeVpXRnRhVzVuU09QY2xac0ciLEtFWUZPUk1BVD0idXJuOnV1aWQ6ZWRlZjhiYTktNzlkNi00YWNlLWEzYzgtMjdkY2Q1MWQyMWVkIixLRVlGT1JNQVRWRVJTSU9OUz0iMSIK</HLSSignalingData></DRMSystem>'
    )

    parsed = cpix.DRMSystem.parse(xml)

    assert parsed.kid == drm_system.kid
    assert parsed.system_id == drm_system.system_id
    assert parsed.pssh == drm_system.pssh
    assert parsed.content_protection_data == drm_system.content_protection_data
    assert parsed.hls_signaling_data == drm_system.hls_signaling_data


def test_hls_signaling_data():
    drm_system = cpix.DRMSystem(
        kid="3f0f9c37-bc82-5742-a780-71caaad6d23b",
        system_id="94ce86fb-07ff-4f43-adb8-93d2fa968ca2",
        hls_signaling_data="I0VYVC1YLUtFWTpNRVRIT0Q9U0FNUExFLUFFUyxVUkk9aHR0cHM6Ly9rZXlzZXJ2ZXIudW5pZmllZC1zdHJlYW1pbmcuY29tL2tleS9MMHBPU3J6dmtZV19LVW5DcTlxUFp3PT0sS0VZRk9STUFUPWlkZW50aXR5LElWPTB4M0YwRjlDMzdCQzgyNTc0MkE3ODA3MUNBQUFENkQyM0I=",
        hls_signaling_data_master="I0VYVC1YLVNFU1NJT04tS0VZOk1FVEhPRD1TQU1QTEUtQUVTLFVSST1odHRwczovL2tleXNlcnZlci51bmlmaWVkLXN0cmVhbWluZy5jb20va2V5L0wwcE9Tcnp2a1lXX0tVbkNxOXFQWnc9PSxLRVlGT1JNQVQ9aWRlbnRpdHksSVY9MHgzRjBGOUMzN0JDODI1NzQyQTc4MDcxQ0FBQUQ2RDIzQg==",
    )

    xml = etree.tostring(drm_system.element())

    assert (
        xml
        == b'<DRMSystem kid="3f0f9c37-bc82-5742-a780-71caaad6d23b" systemId="94ce86fb-07ff-4f43-adb8-93d2fa968ca2"><HLSSignalingData playlist="media">I0VYVC1YLUtFWTpNRVRIT0Q9U0FNUExFLUFFUyxVUkk9aHR0cHM6Ly9rZXlzZXJ2ZXIudW5pZmllZC1zdHJlYW1pbmcuY29tL2tleS9MMHBPU3J6dmtZV19LVW5DcTlxUFp3PT0sS0VZRk9STUFUPWlkZW50aXR5LElWPTB4M0YwRjlDMzdCQzgyNTc0MkE3ODA3MUNBQUFENkQyM0I=</HLSSignalingData><HLSSignalingData playlist="master">I0VYVC1YLVNFU1NJT04tS0VZOk1FVEhPRD1TQU1QTEUtQUVTLFVSST1odHRwczovL2tleXNlcnZlci51bmlmaWVkLXN0cmVhbWluZy5jb20va2V5L0wwcE9Tcnp2a1lXX0tVbkNxOXFQWnc9PSxLRVlGT1JNQVQ9aWRlbnRpdHksSVY9MHgzRjBGOUMzN0JDODI1NzQyQTc4MDcxQ0FBQUQ2RDIzQg==</HLSSignalingData></DRMSystem>'
    )

    parsed = cpix.DRMSystem.parse(xml)

    assert parsed.kid == drm_system.kid
    assert parsed.system_id == drm_system.system_id
    assert parsed.hls_signaling_data == drm_system.hls_signaling_data
    assert (
        parsed.hls_signaling_data_master
        == drm_system.hls_signaling_data_master
    )
