"""
Root CPIX class
"""
from . import etree, ContentKeyList, DRMSystemList, UsageRuleList, PeriodList,\
    KeyPeriodFilter, XSI, NSMAP
from .base import CPIXComparableBase


class CPIX(CPIXComparableBase):
    def __init__(self,
                 content_keys=None,
                 drm_systems=None,
                 usage_rules=None,
                 periods=None):
        self._content_keys = ContentKeyList()
        self._drm_systems = DRMSystemList()
        self._usage_rules = UsageRuleList()
        self._periods = PeriodList()

        if content_keys is not None:
            self.content_keys = content_keys
        if drm_systems is not None:
            self.drm_systems = drm_systems
        if usage_rules is not None:
            self.usage_rules = usage_rules
        if periods is not None:
            self.periods = periods

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

    def element(self):
        el = etree.Element("CPIX", nsmap=NSMAP)
        el.set("{{{xsi}}}schemaLocation".format(
            xsi=XSI), "urn:dashif:org:cpix cpix.xsd")
        if (self.content_keys is not None and
                isinstance(self.content_keys, ContentKeyList) and
                len(self.content_keys) > 0):
            el.append(self.content_keys.element())
        if (self.drm_systems is not None and
                isinstance(self.drm_systems, DRMSystemList) and
                len(self.drm_systems) > 0):
            el.append(self.drm_systems.element())
        if (self.usage_rules is not None and
                isinstance(self.usage_rules, UsageRuleList) and
                len(self.usage_rules) > 0):
            el.append(self.usage_rules.element())
        if (self.periods is not None and
                isinstance(self.periods, PeriodList) and
                len(self.periods) > 0):
            el.append(self.periods.element())
        return el

    @staticmethod
    def parse(xml):
        """
        Parse a CPIX xml
        """
        if isinstance(xml, (str, bytes)):
            xml = etree.fromstring(xml)

        new_cpix = CPIX()

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
