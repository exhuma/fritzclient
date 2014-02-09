from contextlib import nested
from os import urandom
from pkg_resources import resource_string
from unittest import TestCase, skip

from mock import patch

import fritzclient.model as mdl


UNDEF = urandom(10)
"Random value to detect unfinished unit-tests."


class BaseTest(TestCase):

    def setUp(self):
        tr064desc = resource_string('fritzclient',
                                    'tests/data/tr64desc.xml')
        with nested(patch('fritzclient.model.tr064'),
                    patch('fritzclient.model.minisoap')) as (mock_tr064,
                                                             mock_soap):
            mock_tr064.get_tr064desc.return_value = tr064desc
            mock_tr064.discover.return_value = {
                'status_code': 200,
                'location': 'http://192.168.179.1:49000/tr64desc.xml',
                'server': ('FRITZBOX UPnP/1.0 AVM FRITZ!Box Fon WLAN 7270 v3 '
                           '74.04.85'),
                'cache-control': 'max-age=1800',
                'ext': '',
                'st': 'urn:dslforum-org:device:InternetGatewayDevice:1',
                'usn': ('uuid:739f2409-bccb-40e7-8e6c-0024FE6E00C3::'
                        'urn:dslforum-org:device:InternetGatewayDevice:1'),
            }
            self.dev = mdl.InternetGatewayDevice()


class TestInternetGatewayDeviceDiscovery(BaseTest):

    @patch('fritzclient.model.tr064')
    def test_explicit_ip(self, mock_tr064):
        tr064desc = resource_string('fritzclient',
                                    'tests/data/tr64desc.xml')
        mock_tr064.get_tr064desc.return_value = tr064desc
        igd = mdl.InternetGatewayDevice(
            'http://192.168.179.1:49000/tr64desc.xml')
        self.assertFalse(mock_tr064.discover.called,
                         'SSDP discovery executed when it was not needed!')
        self.assertEqual(igd.spec_version, '1.0')

    @patch('fritzclient.model.tr064')
    def test_auto_disco(self, mock_tr064):
        tr064desc = resource_string('fritzclient',
                                    'tests/data/tr64desc.xml')
        mock_tr064.get_tr064desc.return_value = tr064desc
        igd = mdl.InternetGatewayDevice()
        self.assertTrue(mock_tr064.discover.called,
                        'SSDP discovery was not executed!')
        self.assertEqual(igd.spec_version, '1.0')


class TestDevice(BaseTest):

    def test_services(self):
        expected = set([
            {
                'service_type': 'urn:dslforum-org:service:DeviceInfo:1',
                'service_id': 'urn:DeviceInfo-com:serviceId:DeviceInfo1',
                'control_url': '/upnp/control/deviceinfo',
                'event_sub_url': '/upnp/control/deviceinfo',
                'scpd_url': '/deviceinfoSCPD.xml',
            },
            {
                'service_type': 'urn:dslforum-org:service:DeviceConfig:1',
                'service_id': 'urn:DeviceConfig-com:serviceId:DeviceConfig1',
                'control_url': '/upnp/control/deviceconfig',
                'event_sub_url': '/upnp/control/deviceconfig',
                'scpd_url': '/deviceconfigSCPD.xml'
            },
            {
                'service_type': 'urn:dslforum-org:service:Layer3Forwarding:1',
                'service_id': ('urn:Layer3Forwarding-com:serviceId:'
                               'Layer3Forwarding1'),
                'control_url': '/upnp/control/layer3forwarding',
                'event_sub_url': '/upnp/control/layer3forwarding',
                'scpd_url': '/layer3forwardingSCPD.xml'
            },
            {
                'service_type': 'urn:dslforum-org:service:LANConfigSecurity:1',
                'service_id': ('urn:LANConfigSecurity-com:serviceId:'
                               'LANConfigSecurity1'),
                'control_url': '/upnp/control/lanconfigsecurity',
                'event_sub_url': '/upnp/control/lanconfigsecurity',
                'scpd_url': '/lanconfigsecuritySCPD.xml'
            },
            {
                'service_type': 'urn:dslforum-org:service:ManagementServer:1',
                'service_id': ('urn:ManagementServer-com:serviceId:'
                               'ManagementServer1'),
                'control_url': '/upnp/control/mgmsrv',
                'event_sub_url': '/upnp/control/mgmsrv',
                'scpd_url': '/mgmsrvSCPD.xml'
            },
            {
                'service_type': 'urn:dslforum-org:service:Time:1',
                'service_id': 'urn:Time-com:serviceId:Time1',
                'control_url': '/upnp/control/time',
                'event_sub_url': '/upnp/control/time',
                'scpd_url': '/timeSCPD.xml'
            },
            {
                'service_type': 'urn:dslforum-org:service:UserInterface:1',
                'service_id': 'urn:UserInterface-com:serviceId:UserInterface1',
                'control_url': '/upnp/control/userif',
                'event_sub_url': '/upnp/control/userif',
                'scpd_url': '/userifSCPD.xml'
            },
            {
                'service_type': 'urn:dslforum-org:service:X_VoIP:1',
                'service_id': 'urn:X_VoIP-com:serviceId:X_VoIP1',
                'control_url': '/upnp/control/x_voip',
                'event_sub_url': '/upnp/control/x_voip',
                'scpd_url': '/x_voipSCPD.xml'
            },
            {
                'service_type': 'urn:dslforum-org:service:X_AVM-DE_Storage:1',
                'service_id': ('urn:X_AVM-DE_Storage-com:serviceId:'
                               'X_AVM-DE_Storage1'),
                'control_url': '/upnp/control/x_storage',
                'event_sub_url': '/upnp/control/x_storage',
                'scpd_url': '/x_storageSCPD.xml'
            },
            {
                'service_type': 'urn:dslforum-org:service:X_AVM-DE_OnTel:1',
                'service_id': ('urn:X_AVM-DE_OnTel-com:serviceId:'
                               'X_AVM-DE_OnTel1'),
                'control_url': '/upnp/control/x_contact',
                'event_sub_url': '/upnp/control/x_contact',
                'scpd_url': '/x_contactSCPD.xml'
            },
            {
                'service_type': ('urn:dslforum-org:service:'
                                 'X_AVM-DE_WebDAVClient:1'),
                'service_id': ('urn:X_AVM-DE_WebDAV-com:serviceId:'
                               'X_AVM-DE_WebDAVClient1'),
                'control_url': '/upnp/control/x_webdav',
                'event_sub_url': '/upnp/control/x_webdav',
                'scpd_url': '/x_webdavSCPD.xml'
            },
            {
                'service_type': 'urn:dslforum-org:service:X_AVM-DE_UPnP:1',
                'service_id': 'urn:X_AVM-DE_UPnP-com:serviceId:X_AVM-DE_UPnP1',
                'control_url': '/upnp/control/x_upnp',
                'event_sub_url': '/upnp/control/x_upnp',
                'scpd_url': '/x_upnpSCPD.xml'
            },
            {
                'service_type': ('urn:dslforum-org:service:'
                                 'X_AVM-DE_RemoteAccess:1'),
                'service_id': ('urn:X_AVM-DE_RemoteAccess-com:serviceId:'
                               'X_AVM-DE_RemoteAccess1'),
                'control_url': '/upnp/control/x_remote',
                'event_sub_url': '/upnp/control/x_remote',
                'scpd_url': '/x_remoteSCPD.xml'
            },
            {
                'service_type': 'urn:dslforum-org:service:X_AVM-DE_MyFritz:1',
                'service_id': ('urn:X_AVM-DE_MyFritz-com:serviceId:'
                               'X_AVM-DE_MyFritz1'),
                'control_url': '/upnp/control/x_myfritz',
                'event_sub_url': '/upnp/control/x_myfritz',
                'scpd_url': '/x_myfritzSCPD.xml'
            },
            {
                'service_type': 'urn:dslforum-org:service:X_AVM-DE_TAM:1',
                'service_id': 'urn:X_AVM-DE_TAM-com:serviceId:X_AVM-DE_TAM1',
                'control_url': '/upnp/control/x_tam',
                'event_sub_url': '/upnp/control/x_tam',
                'scpd_url': '/x_tamSCPD.xml'
            }])

        result = [{
            'service_type': _._service_type,
            'service_id': _._service_id,
            'control_url': _._control_url,
            'event_sub_url': _._event_sub_url,
            'scpd_url': _._scpd_url
        } for _ in self.dev.services]

        self.assertEqual(result, expected)

    def test_devices(self):
        pass

    def test_l3fw(self):
        self.assertIsInstance(self.dev.layer3_forwarding,
                              mdl.Layer3Forwarding)

    def test_device_info(self):
        self.assertIsInstance(self.dev.device_info,
                              mdl.DeviceInfo)

    def test_device_config(self):
        self.assertIsInstance(self.dev.device_config,
                              mdl.DeviceConfig)

    def test_lan_config_security(self):
        self.assertIsInstance(self.dev.lan_config_security,
                              mdl.LANConfigSecurity)

    def test_management_server(self):
        self.assertIsInstance(self.dev.management_server,
                              mdl.ManagementServer)

    def test_time(self):
        self.assertIsInstance(self.dev.time,
                              mdl.Time)

    def test_user_interface(self):
        self.assertIsInstance(self.dev.user_interface,
                              mdl.UserInterface)

    def test_lan_device(self):
        self.assertIsInstance(self.dev.lan_device,
                              mdl.LANDevice)

    def test_wan_device(self):
        self.assertIsInstance(self.dev.lan_device,
                              mdl.WANDevice)

    @skip('AVM Extensions are not yet implemented')
    def test_X_VoIP(self):
        self.fail('not yet implemented')

    @skip('AVM Extensions are not yet implemented')
    def test_X_AVM_DE_Storage(self):
        self.fail('not yet implemented')

    @skip('AVM Extensions are not yet implemented')
    def test_X_AVM_DE_OnTel(self):
        self.fail('not yet implemented')

    @skip('AVM Extensions are not yet implemented')
    def test_X_AVM_DE_WebDAVClient(self):
        self.fail('not yet implemented')

    @skip('AVM Extensions are not yet implemented')
    def test_X_AVM_DE_UPnP(self):
        self.fail('not yet implemented')

    @skip('AVM Extensions are not yet implemented')
    def test_X_AVM_DE_RemoteAccess(self):
        self.fail('not yet implemented')

    @skip('AVM Extensions are not yet implemented')
    def test_X_AVM_DE_MyFritz(self):
        self.fail('not yet implemented')

    @skip('AVM Extensions are not yet implemented')
    def test_X_AVM_DE_TAM(self):
        self.fail('not yet implemented')


class TestDeviceInfo(BaseTest):

    def setUp(self):
        super(TestDeviceInfo, self).setUp()
        self.info = self.dev.device_info

    def test_wan_device(self):
        self.assertIsInstance(self.info.wan_device,
                              mdl.WANDevice)

    def test_manufacturer_name(self):
        self.assertEqual(self.info.manufacturer_name, 'AVM')

    def test_manufacturer_oui(self):
        oui = self.info.manufacturer_oui
        self.assertEqual(len(oui), 6)
        self.assertEqual(oui, '00040E')

    def test_model_name(self):
        self.assertEqual(self.info.model_name,
                         'FRITZ!Box Fon WLAN 7390')

    def test_description(self):
        self.assertEqual(self.info.description,
                         'FRITZ!Box Fon WLAN 7390 84.05.52')

    def test_product_class(self):
        self.assertEqual(self.info.product_class,
                         'FRITZ!Box')

    def test_serial_number(self):
        self.assertEqual(self.info.serial_number,
                         '0896D74C6BF8')

    def test_software_version(self):
        self.assertEqual(self.info.software_version,
                         '84.05.52')

    def test_additional_software_versions(self):
        self.assertIsNone(self.info.additional_software_versions)

    def test_modem_firmware_version(self):
        self.assertIsNone(self.info.modem_firmware_version)

    def test_enabled_options(self):
        self.assertIsNone(self.info.enabled_options)

    def test_hardware_version(self):
        self.assertEqual(self.info.hardware_version,
                         'FRITZ!Box Fon WLAN 7390')

    def test_additional_hardware_versions(self):
        self.assertIsNone(self.info.additional_hardware_versions)

    def test_spec_version(self):
        self.assertEqual(self.info.spec_version,
                         '1.0')

    def test_provisioning_code(self):
        self.assertEqual(self.info.provisioning_code,
                         '7390V2012.09.19')

    def test_uptime(self):
        self.assertEqual(self.info.uptime,
                         '794051')

    def test_first_use_date(self):
        self.assertIsNone(self.info.first_use_date)

    def test_device_log(self):
        self.assertEqual(self.info.device_log,
                         UNDEF)

    def test_get_info(self):
        res = self.info.get_info()
        expected = {
            'manufacturer_name': 'AVM',
            'manufacturer_oui': UNDEF,
            'model_name': UNDEF,
            'description': UNDEF,
            'product_class': UNDEF,
            'serial_number': UNDEF,
            'software_version': UNDEF,
            'additional_software_versions': UNDEF,
            'modem_firmware_version': UNDEF,
            'enabled_options': UNDEF,
            'hardware_version': UNDEF,
            'additional_hardware_versions': UNDEF,
            'spec_version': UNDEF,
            'provisioning_code': UNDEF,
            'uptime': UNDEF,
            'first_use_date': UNDEF,
        }
        self.assertEqual(res, expected)

    @patch('fritzclient.model.minisoap')
    def test_set_provisioning_code(self, mock_soap):
        self.info.set_provisioning_code('newcode')
        mock_soap.send.assert_called_with('SetProvisioningCode',
                                          {'ProvisioningCode': 'newcode'})

    def test_get_device_log(self):
        result = self.info.get_device_log()
        expected = {
            'device_log': UNDEF
        }
        self.assertEqual(result, expected)


# vim: set path+=fritzclient :
