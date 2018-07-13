# cpix
Python library for working with CPIX 2.0 (DASH-IF Content Protection Information Exchange) documents

For more details on CPIX see:

* https://dashif.org/guidelines/
* https://dashif.org/wp-content/uploads/2016/11/DASH-IF-CPIX-v2-0.pdf

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

Encryption, decryption and signing are not supported.