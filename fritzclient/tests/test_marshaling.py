from unittest import TestCase
from pkg_resources import resource_string

import fritzclient.marshal as codec
import fritzclient.model as mdl


class TestMarshalingDeviceDesc(TestCase):
    """
    Test decoding of the document returned from the Fritz device description.
    """

    def setUp(self):
        self.data = resource_string('fritzclient',
                                    'tests/data/device-meta.xml')

    def test_return_type(self):
        result = codec.decode(self.data)
        self.assertIsInstance(result, mdl.Device)

    def test_device_type(self):
        result = codec.decode(self.data)
        self.assertEqual(
            result.device_type,
            'urn:schemas-upnp-org:device:InternetGatewayDevice:1')

    def test_friendly_name(self):
        result = codec.decode(self.data)
        self.assertEqual(
            result.friendly_name,
            'FRITZ!Box Fon WLAN 7390')

    def test_manufacturer(self):
        result = codec.decode(self.data)
        self.assertEqual(
            result.manufacturer,
            'AVM Berlin')

    def test_manufacturer_url(self):
        result = codec.decode(self.data)
        self.assertEqual(
            result.manufacturer_url,
            'http://www.avm.de')

    def test_model_description(self):
        result = codec.decode(self.data)
        self.assertEqual(
            result.model_description,
            'FRITZ!Box Fon WLAN 7390')

    def test_model_name(self):
        result = codec.decode(self.data)
        self.assertEqual(
            result.model_name,
            'FRITZ!Box Fon WLAN 7390')

    def test_model_number(self):
        result = codec.decode(self.data)
        self.assertEqual(
            result.model_number,
            'avme')

    def test_model_url(self):
        result = codec.decode(self.data)
        self.assertEqual(
            result.model_url,
            'http://www.avm.de')

    def test_udn(self):
        result = codec.decode(self.data)
        self.assertEqual(
            result.udn,
            'uuid:75802409-bccb-40e7-8e6c-0896D74C6BF8')

    def test_icons_type(self):
        result = codec.decode(self.data)
        self.assertIsInstance(result.icons, list)

    def test_icons(self):
        result = codec.decode(self.data)
        self.assertEqual(
            result.icons[0],
            {
                'mimetype': 'image/gif',
                'width': '118',
                'height': '119',
                'depth': '8',
                'url': '/ligd.gif',
            })

    def test_services_type(self):
        result = codec.decode(self.data)
        self.assertIsInstance(result.services, list)

    def test_services(self):
        result = codec.decode(self.data)
        service = result.services[0]
        self.assertEqual(service.service_type,
                         'urn:schemas-any-com:service:Any:1')
        self.assertEqual(service.service_id, 'urn:any-com:serviceId:any1')
        self.assertEqual(service.control_url, '/upnp/control/any')
        self.assertEqual(service.event_suburl, '/upnp/control/any')
        self.assertEqual(service.scpdurl, '/any.xml')

    def test_devices_type(self):
        result = codec.decode(self.data)
        self.assertIsInstance(result.devices, list)

    def test_devices_elementtype(self):
        result = codec.decode(self.data)
        self.assertIsInstance(result.devices[0], mdl.Device)


class TestMarshalingTr064Desc(TestCase):
    """
    Test decoding of the document returned from the TR-064 device description.
    """

    def setUp(self):
        self.data = resource_string('fritzclient',
                                    'tests/data/tr64desc.xml')

    def test_return_type(self):
        result = codec.decode(self.data)
        self.assertIsInstance(result, mdl.Device)

    def test_device_type(self):
        result = codec.decode(self.data)
        self.assertEqual(
            result.device_type,
            'urn:dslforum-org:device:InternetGatewayDevice:1')

    def test_friendly_name(self):
        result = codec.decode(self.data)
        self.assertEqual(
            result.friendly_name,
            'FRITZ!Box Fon WLAN 7390')

    def test_manufacturer(self):
        result = codec.decode(self.data)
        self.assertEqual(
            result.manufacturer,
            'AVM')

    def test_manufacturer_url(self):
        result = codec.decode(self.data)
        self.assertEqual(
            result.manufacturer_url,
            'www.avm.de')

    def test_model_description(self):
        result = codec.decode(self.data)
        self.assertEqual(
            result.model_description,
            'FRITZ!Box Fon WLAN 7390')

    def test_model_name(self):
        result = codec.decode(self.data)
        self.assertEqual(
            result.model_name,
            'FRITZ!Box Fon WLAN 7390')

    def test_model_number(self):
        result = codec.decode(self.data)
        self.assertEqual(
            result.model_number,
            '- avme')

    def test_model_url(self):
        result = codec.decode(self.data)
        self.assertEqual(result.model_url, 'www.avm.de')

    def test_udn(self):
        result = codec.decode(self.data)
        self.assertEqual(
            result.udn,
            'uuid:739f2409-bccb-40e7-8e6c-0896D74C6BF8')

    def test_icons_type(self):
        result = codec.decode(self.data)
        self.assertIsInstance(result.icons, list)

    def test_icons(self):
        result = codec.decode(self.data)
        self.assertEqual(
            result.icons[0],
            {
                'mimetype': 'image/gif',
                'width': '118',
                'height': '119',
                'depth': '8',
                'url': '/ligd.gif',
            })

    def test_services_type(self):
        result = codec.decode(self.data)
        self.assertIsInstance(result.services, list)

    def test_services(self):
        result = codec.decode(self.data)
        self.assertEqual(len(result.services), 15)
        service = result.services[0]
        self.assertEqual(service.service_type,
                         'urn:dslforum-org:service:DeviceInfo:1')
        self.assertEqual(service.service_id,
                         'urn:DeviceInfo-com:serviceId:DeviceInfo1')
        self.assertEqual(service.control_url, '/upnp/control/deviceinfo')
        self.assertEqual(service.event_suburl, '/upnp/control/deviceinfo')
        self.assertEqual(service.scpdurl, '/deviceinfoSCPD.xml')

    def test_devices_type(self):
        result = codec.decode(self.data)
        self.assertIsInstance(result.devices, list)

    def test_devices_length(self):
        result = codec.decode(self.data)
        self.assertEqual(len(result.devices), 2)

    def test_devices_elementtype(self):
        result = codec.decode(self.data)
        self.assertIsInstance(result.devices[0], mdl.Device)


# vim: set path+=fritzclient :
