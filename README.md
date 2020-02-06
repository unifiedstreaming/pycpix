# cpix
Python library for working with CPIX 2.2 (DASH-IF Content Protection Information Exchange) documents

For more details on CPIX see:

* https://dashif.org/guidelines/
* https://dash-industry-forum.github.io/docs/CPIX2.2/Cpix.html

## Supported features

* Creation of CPIX documents
* Content keys
* Usage rules
* DRM systems
* Parsing of CPIX documents
* Validation against CPIX XSD

## Not yet implemented

* Validation of document correctness (e.g. kid referenced by usage rule matches a content key)

## Not supported

* Encryption, decryption and signing are not supported.

## Installation

Install using [pip](https://pip.pypa.io/):

```
pip install cpix
```

## Examples

### Scripts

Example scripts which can be used with Widevine and Playready test servers to
get or create keys and produce CPIX documents are available in `example`.

### Simple CPIX

To create a simple CPIX document with a single key:

```python
import cpix

full_cpix = cpix.CPIX(
    content_keys=cpix.ContentKeyList(
        cpix.ContentKey(
            kid="0DC3EC4F-7683-548B-81E7-3C64E582E136",
            cek="WADwG2qCqkq5TVml+U5PXw=="
        )
    ),
    drm_systems=cpix.DRMSystemList(
        cpix.DRMSystem(
            kid="0DC3EC4F-7683-548B-81E7-3C64E582E136",
            system_id="EDEF8BA9-79D6-4ACE-A3C8-27DCD51D21ED",
            pssh=("AAAAxnBzc2gBAAAA7e+LqXnWSs6jyCfc1R0h7QAAAAINw+xPdoNUi4HnPGT"
                  "lguE2FEe37S9mVyu9EwbOfPNhDQAAAIISEBRHt+0vZlcrvRMGznzzYQ0SEF"
                  "rGoR6qL17Vv2aMQByBNMoSEG7hNRbI51h7rp9+zT6Zom4SEPnsEqYaJl1Hj"
                  "4MzTjp40scSEA3D7E92g1SLgec8ZOWC4TYaDXdpZGV2aW5lX3Rlc3QiEXVu"
                  "aWZpZWQtc3RyZWFtaW5nSOPclZsG")
        )
    )
)
```

This can then be printed as a formatted XML document:

```python
print(str(full_cpix.pretty_print(xml_declaration=True), "utf-8'"))
```

```xml
<?xml version='1.0' encoding='utf-8'?>
<CPIX xmlns:pskc="urn:ietf:params:xml:ns:keyprov:pskc" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns="urn:dashif:org:cpix" xsi:schemaLocation="urn:dashif:org:cpix cpix.xsd">
  <ContentKeyList>
    <ContentKey kid="0dc3ec4f-7683-548b-81e7-3c64e582e136">
      <Data>
        <pskc:Secret>
          <pskc:PlainValue>WADwG2qCqkq5TVml+U5PXw==</pskc:PlainValue>
        </pskc:Secret>
      </Data>
    </ContentKey>
  </ContentKeyList>
  <DRMSystemList>
    <DRMSystem kid="0dc3ec4f-7683-548b-81e7-3c64e582e136" systemId="edef8ba9-79d6-4ace-a3c8-27dcd51d21ed">
      <PSSH>AAAAxnBzc2gBAAAA7e+LqXnWSs6jyCfc1R0h7QAAAAINw+xPdoNUi4HnPGTlguE2FEe37S9mVyu9EwbOfPNhDQAAAIISEBRHt+0vZlcrvRMGznzzYQ0SEFrGoR6qL17Vv2aMQByBNMoSEG7hNRbI51h7rp9+zT6Zom4SEPnsEqYaJl1Hj4MzTjp40scSEA3D7E92g1SLgec8ZOWC4TYaDXdpZGV2aW5lX3Rlc3QiEXVuaWZpZWQtc3RyZWFtaW5nSOPclZsG</PSSH>
    </DRMSystem>
  </DRMSystemList>
</CPIX>
```
