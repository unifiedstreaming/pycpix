"""
Root CPIX class
"""
from . import etree, ContentKeyList, DRMSystemList, UsageRuleList,\
    CPIX_SCHEMA, XSI, NSMAP
from .base import CPIXComparableBase


class CPIX(CPIXComparableBase):
    def __init__(self, content_keys=None, drm_systems=None, usage_rules=None):
        self._content_keys = None
        self._drm_systems = None
        self._usage_rules = None

        if content_keys is not None:
            self.content_keys = content_keys
        if drm_systems is not None:
            self.drm_systems = drm_systems
        if usage_rules is not None:
            self.usage_rules = usage_rules

    @property
    def content_keys(self):
        return self._content_keys

    @content_keys.setter
    def content_keys(self, content_keys):
        if isinstance(content_keys, ContentKeyList):
            self._content_keys = content_keys
        else:
            raise TypeError("content_keys should be a ContentKeyList")

    @property
    def drm_systems(self):
        return self._drm_systems

    @drm_systems.setter
    def drm_systems(self, drm_systems):
        if isinstance(drm_systems, DRMSystemList):
            self._drm_systems = drm_systems
        else:
            raise TypeError("drm_systems should be a DRMSystemList")

    @property
    def usage_rules(self):
        return self._usage_rules

    @usage_rules.setter
    def usage_rules(self, usage_rules):
        if isinstance(usage_rules, UsageRuleList):
            self._usage_rules = usage_rules
        else:
            raise TypeError("usage_rules should be a UsageRuleList")

    def element(self):
        el = etree.Element("CPIX", nsmap=NSMAP)
        el.set("{{{xsi}}}schemaLocation".format(
            xsi=XSI), "urn:dashif:org:cpix cpix.xsd")
        if self.content_keys is not None and isinstance(self.content_keys,
                                                        ContentKeyList):
            el.append(self.content_keys.element())
        if self.drm_systems is not None and isinstance(self.drm_systems,
                                                       DRMSystemList):
            el.append(self.drm_systems.element())
        if self.usage_rules is not None and isinstance(self.usage_rules,
                                                       UsageRuleList):
            el.append(self.usage_rules.element())
        return el

    @staticmethod
    def parse(xml, validate=False):
        """
        Parse a CPIX xml
        """
        if validate:
            valid = validate(xml)

            if not valid:
                raise Exception("XML failed validation")

        new_cpix = CPIX()
        parsed_xml = etree.fromstring(xml)
        new_cpix.parsed_xml = parsed_xml

        for element in parsed_xml.getchildren():
            tag = etree.QName(element.tag).localname

            if tag == "ContentKeyList":
                new_cpix.content_keys = ContentKeyList.parse(element)
            if tag == "DRMSystemList":
                new_cpix.drm_systems = DRMSystemList.parse(element)
            if tag == "ContentKeyUsageRuleList":
                new_cpix.usage_rules = UsageRuleList.parse(element)

        return new_cpix

    @staticmethod
    def validate(xml):
        """
        Validate a CPIX XML against the schema

        Returns a tuple of valid true/false and if false the error(s)
        """
        parsed_xml = etree.fromstring(xml)
        try:
            CPIX_SCHEMA.assertValid(parsed_xml)
        except etree.DocumentInvalid as e:
            return (False, e)
        return (True, "")
