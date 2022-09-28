"""
Root CPIX class
"""
from . import etree, ContentKeyList, DRMSystemList, UsageRuleList, PeriodList,\
    KeyPeriodFilter, DeliveryDataList, XSI, NSMAP
from .base import CPIXComparableBase


class CPIX(CPIXComparableBase):
    def __init__(self,
                 content_keys=None,
                 drm_systems=None,
                 usage_rules=None,
                 periods=None,
                 content_id=None,
                 version=None,
                 delivery_datas=None):
        self._content_keys = ContentKeyList()
        self._drm_systems = DRMSystemList()
        self._usage_rules = UsageRuleList()
        self._periods = PeriodList()
        self._delivery_datas = DeliveryDataList()
        self._content_id = None
        self._version = None

        if content_keys is not None:
            self.content_keys = content_keys
        if drm_systems is not None:
            self.drm_systems = drm_systems
        if usage_rules is not None:
            self.usage_rules = usage_rules
        if periods is not None:
            self.periods = periods
        if content_id is not None:
            self.content_id = content_id
        if delivery_datas is not None:
            self.delivery_datas = delivery_datas

        self.version = version

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

    @property
    def periods(self):
        return self._periods

    @periods.setter
    def periods(self, periods):
        if isinstance(periods, PeriodList):
            self._periods = periods
        else:
            raise TypeError("periods should be a PeriodList")

    @property
    def content_id(self):
        return self._content_id

    @content_id.setter
    def content_id(self, content_id):
        if isinstance(content_id, str):
            self._content_id = content_id
        elif content_id is None:
            self._content_id = None
        else:
            raise TypeError("content_id should be a string")

    @property
    def version(self):
        return self._version

    @version.setter
    def version(self, version):
        if isinstance(version, str):
            self._version = version
        elif version is None:
            self._version = None
        else:
            raise TypeError("version should be a string")

    @property
    def delivery_datas(self):
        return self._delivery_datas

    @delivery_datas.setter
    def delivery_datas(self, delivery_datas):
        if isinstance(delivery_datas, DeliveryDataList):
            self._delivery_datas = delivery_datas
        else:
            raise TypeError("delivery_datas should be a DeliveryDataList")

    def element(self):
        el = etree.Element("CPIX", nsmap=NSMAP)
        el.set("{{{xsi}}}schemaLocation".format(
            xsi=XSI), "urn:dashif:org:cpix cpix.xsd")
        if (self.content_id is not None and
                isinstance(self.content_id, str)):
            el.set("contentId", self.content_id)
        if (self.version is not None and
                isinstance(self.version, str)):
            el.set("version", self.version)
        if (self.delivery_datas is not None and
                isinstance(self.delivery_datas, DeliveryDataList) and
                len(self.delivery_datas) > 0):
            el.append(self.delivery_datas.element())
        if (self.content_keys is not None and
                isinstance(self.content_keys, ContentKeyList) and
                len(self.content_keys) > 0):
            el.append(self.content_keys.element())
        if (self.drm_systems is not None and
                isinstance(self.drm_systems, DRMSystemList) and
                len(self.drm_systems) > 0):
            el.append(self.drm_systems.element())
        if (self.periods is not None and
                isinstance(self.periods, PeriodList) and
                len(self.periods) > 0):
            el.append(self.periods.element())
        if (self.usage_rules is not None and
                isinstance(self.usage_rules, UsageRuleList) and
                len(self.usage_rules) > 0):
            el.append(self.usage_rules.element())
        return el

    @staticmethod
    def parse(xml):
        """
        Parse a CPIX xml
        """
        if isinstance(xml, (str, bytes)):
            xml = etree.fromstring(xml)

        new_cpix = CPIX()

        if "contentId" in xml.attrib:
            new_cpix.content_id = xml.attrib["contentId"]

        if "version" in xml.attrib:
            new_cpix.version = xml.attrib["version"]

        for element in xml.getchildren():
            tag = etree.QName(element.tag).localname

            if tag == "ContentKeyList":
                new_cpix.content_keys = ContentKeyList.parse(element)
            if tag == "DRMSystemList":
                new_cpix.drm_systems = DRMSystemList.parse(element)
            if tag == "ContentKeyUsageRuleList":
                new_cpix.usage_rules = UsageRuleList.parse(element)
            if tag == "ContentKeyPeriodList":
                new_cpix.periods = PeriodList.parse(element)
            if tag == "DeliveryDataList":
                new_cpix.delivery_datas = DeliveryDataList.parse(element)

        return new_cpix

    # content check functions
    def check_usage_rules(self):
        """
        Checks each usage rule references a valid content key
        """
        keys = [key.kid for key in self.content_keys]
        errors = []

        for usage_rule in self.usage_rules:
            if usage_rule.kid not in keys:
                errors.append(
                    "usage rule references missing kid: {kid}".format(
                        kid=usage_rule.kid))
        if len(errors) == 0:
            return (True, errors)
        else:
            return (False, errors)

    def check_drm_systems(self):
        """
        Checks each drm system references a valid content key
        """
        keys = [key.kid for key in self.content_keys]
        errors = []

        for drm_system in self.drm_systems:
            if drm_system.kid not in keys:
                errors.append(
                    "DRM system references missing kid: {kid}".format(
                        kid=drm_system.kid))
        if len(errors) == 0:
            return (True, errors)
        else:
            return (False, errors)

    def check_period_filters(self):
        """
        Checks each period filter references a valid period
        """
        periods = [period.id for period in self.periods]
        errors = []

        for usage_rule in self.usage_rules:
            for filter in usage_rule:
                if (isinstance(filter, KeyPeriodFilter) and
                        filter.period_id not in periods):
                    errors.append(
                        "period filter references missing period: {id}".format(
                            id=filter.period_id))
        if len(errors) == 0:
            return (True, errors)
        else:
            return (False, errors)

    def validate_content(self):
        """
        Confirms content is valid:
            usage rules must reference a valid content key
            drm systems must reference a valid content key
            period filters in usage rules must reference a valid period
        """
        errors = []
        errors += self.check_usage_rules()[1]
        errors += self.check_drm_systems()[1]
        errors += self.check_period_filters()[1]

        if len(errors) == 0:
            return (True, errors)
        else:
            return (False, errors)
