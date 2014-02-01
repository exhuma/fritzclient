from contextlib import nested
from os import urandom
from pkg_resources import resource_string
from unittest import TestCase

from mock import patch

import fritzclient.model as mdl


UNDEF = urandom(10)
"Random value to detect unfinished unit-tests."


class BaseTest(TestCase):

    def setUp(self):
        tr064desc = resource_string('fritzclient',
                                    'tests/data/tr64desc.xml')
        with nested(patch('fritzclient.model.tr064'),
                    patch('fritzclient.model.requests')) as (mock_tr064,
                                                             mock_req):
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
            self.igd = mdl.InternetGatewayDevice()


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


class TestInternetGatewayDevice(BaseTest):

    def test_l3fw(self):
        self.assertIsInstance(self.igd.layer3_forwarding,
                              mdl.Layer3Forwarding)

    def test_device_info(self):
        self.assertIsInstance(self.igd.device_info,
                              mdl.DeviceInfo)

    def test_device_config(self):
        self.assertIsInstance(self.igd.device_config,
                              mdl.DeviceConfig)

    def test_lan_config_security(self):
        self.assertIsInstance(self.igd.lan_config_security,
                              mdl.LANConfigSecurity)

    def test_management_server(self):
        self.assertIsInstance(self.igd.management_server,
                              mdl.ManagementServer)

    def test_time(self):
        self.assertIsInstance(self.igd.time,
                              mdl.Time)

    def test_user_interface(self):
        self.assertIsInstance(self.igd.user_interface,
                              mdl.UserInterface)

    def test_lan_device(self):
        self.assertIsInstance(self.igd.lan_device,
                              mdl.LANDevice)


class TestDeviceInfo(BaseTest):

    def setUp(self):
        super(TestDeviceInfo, self).setUp()
        self.info = self.igd.device_info

    def test_wan_device(self):
        self.assertIsInstance(self.info.wan_device,
                              mdl.WANDevice)

    def test_manufacturer_name(self):
        self.assertEqual(self.info.manufacturer_name, 'AVM')

    def test_manufacturer_oui(self):
        oui = self.info.manufacturer_oui
        self.assertEqual(len(oui), 6)
        self.assertEqual(oui, UNDEF)

    def test_model_name(self):
        self.assertEqual(self.info.model_name,
                         UNDEF)

    def test_description(self):
        self.assertEqual(self.info.description,
                         UNDEF)

    def test_product_class(self):
        self.assertEqual(self.info.product_class,
                         UNDEF)

    def test_serial_number(self):
        self.assertEqual(self.info.serial_number,
                         UNDEF)

    def test_software_version(self):
        self.assertEqual(self.info.software_version,
                         UNDEF)

    def test_additional_software_versions(self):
        self.assertEqual(self.info.additional_software_versions,
                         UNDEF)

    def test_modem_firmware_version(self):
        self.assertEqual(self.info.modem_firmware_version,
                         UNDEF)

    def test_enabled_options(self):
        self.assertEqual(self.info.enabled_options,
                         UNDEF)

    def test_hardware_version(self):
        self.assertEqual(self.info.hardware_version,
                         UNDEF)

    def test_additional_hardware_versions(self):
        self.assertEqual(self.info.additional_hardware_versions,
                         UNDEF)

    def test_spec_version(self):
        self.assertEqual(self.info.spec_version,
                         UNDEF)

    def test_provisioning_code(self):
        self.assertEqual(self.info.provisioning_code,
                         UNDEF)

    def test_uptime(self):
        self.assertEqual(self.info.uptime,
                         UNDEF)

    def test_first_use_date(self):
        self.assertEqual(self.info.first_use_date,
                         UNDEF)

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
