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


# vim: set path+=fritzclient :
