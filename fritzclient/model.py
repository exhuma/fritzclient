import xml.etree.ElementTree as ET
from urlparse import urlparse, urlunparse
import logging

from fritzclient import tr064, minisoap

LOG = logging.getLogger(__name__)
ET.register_namespace('s', 'http://schemas.xmlsoap.org/soap/envelope/')
NS = '{urn:dslforum-org:device-1-0}'


class ProxyObject(object):

    def __init__(self, control_urls, tr064root, host):
        self._control_urls = control_urls
        self._tr046root = tr064root
        self._host = host

    def _execute_action(self, action, params=None):
        LOG.info("Executing %r with params %r", action, params)

        control_url = self._control_urls[self.__class__.TYPE]
        url = urlunparse((self._host[0:2] + (control_url, '', '', '')))

        return minisoap.execute(url, self.__class__.TYPE, action, params)


class DeviceInfo(ProxyObject):

    TYPE = 'urn:dslforum-org:service:DeviceInfo:1'

    def __init__(self, *args, **kwargs):
        super(DeviceInfo, self).__init__(*args, **kwargs)
        info_result = self._execute_action('GetInfo')
        self.manufacturer_name = info_result.get('NewManufacturerName')
        self.manufacturer_oui = info_result.get('NewManufacturerOUI')
        self.model_name = info_result.get('NewModelName')
        self.description = info_result.get('NewDescription')
        self.product_class = info_result.get('NewProductClass')
        self.serial_number = info_result.get('NewSerialNumber')
        self.software_version = info_result.get('NewSoftwareVersion')
        self.additional_software_versions = info_result.get(
            'NewAdditionalSoftwareVersions')
        self.modem_firmware_version = info_result.get(
            'NewModemFirmwareVersion')
        self.enabled_options = info_result.get('NewEnabledOptions')
        self.hardware_version = info_result.get('NewHardwareVersion')
        self.additional_hardware_versions = info_result.get(
            'NewAdditionalHardwareVersions')
        self.spec_version = info_result.get('NewSpecVersion')
        self.provisioning_code = info_result.get('NewProvisioningCode')
        self.uptime = info_result.get('NewUpTime')
        self.firstuse_date = info_result.get('NewFirstUseDate')


def get_root_device(location=None):

    if not location:
        # No location given. Run an SSDP discovery.
        tr064_response = tr064.discover()
        location = tr064_response['location']

    tr064desc = tr064.get_tr064desc(location)
    root = ET.fromstring(tr064desc)
    if root.tag != '{ns}root'.format(ns=NS):
        raise ValueError('The document returned at {!r} is not a valid '
                         'TR-064 document!'.format(location))

    spec = root.find('./{}specVersion'.format(NS))
    spec_version = '.'.join([tag.text for tag in spec])

    if spec_version != '1.0':
        raise ValueError('This library only supports TR-064 documents of '
                         'spec version 1.0! You passed in a document of '
                         'version {!r}'.format(spec_version))

    control_urls = {}
    for srv in root.findall(
            './{0}device/{0}serviceList/{0}service'.format(NS)):
        service_type = srv.find('./{}serviceType'.format(NS)).text.strip()
        control_url = srv.find('./{}controlURL'.format(NS)).text.strip()
        control_urls[service_type] = control_url
