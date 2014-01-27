from unittest import TestCase
from pkg_resources import resource_string

from mock import patch

from fritzclient.ssdp import discover


class TestDiscovery(TestCase):

    @patch('fritzclient.ssdp.socket.socket')
    def test_disco(self, socket):
        self.maxDiff = 1000
        example_response = resource_string('fritzclient',
                                           'tests/data/ssdp_response.txt')
        sock = socket()
        sock.recv.return_value = example_response
        response = discover()

        disco_message = (
            b'M-SEARCH * HTTP/1.1\n'
            b'Host: 239.255.255.250:1900\n'
            b'Man: "ssdp:discover"\n'
            b'MX: 5\n'
            b'ST: urn:dslforum-org:device:InternetGatewayDevice:1\n'
        )

        sock.sendto(disco_message, ('239.255.255.250', 1900))

        expected = {
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
        self.assertEqual(response, expected)
