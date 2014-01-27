from unittest import TestCase
import xml.dom.minidom as dom

from mock import patch

import fritzclient.minisoap as soap


class TestMiniSoap(TestCase):
    """
    Test a simplified SOAP implementation.
    """

    def test_render_message(self):
        result = soap.render_message('1.2.3.4', '/url', 'GetSecurityPort')
        doc = dom.parseString(result)
        root = doc.documentElement
        envelope = root.firstChild
        body = envelope.firstChild
        self.assertEqual(body.firstChild.tagName, 'u:GetSecurityPort')

    def test_parse_response(self):
        response_data = (
            b'<?xml version="1.0"?>'
            b'<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/" '
            b's:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">'
            b'<s:Body>'
            b'<u:GetSecurityPortResponse xmlns:u="urn:dslforumorg:'
            b'service:DeviceInfo:1">'
            b'<NewSecurityPort>49443</NewSecurityPort>'
            b'</u:GetSecurityPortResponse>'
            b'</s:Body> </s:Envelope>'
        )
        output = soap.parse_response(response_data)
        self.assertEqual(output['NewSecurityPort'], 49443)

    @patch('fritzclient.minisoap.requests')
    @patch('fritzclient.minisoap.dom')
    def test_send_noparams(self, dom, requests):
        data = soap.render_message('1.2.3.4', '/url', 'GetSecurityPort')
        soap.send('1.2.3.4', '/url', 'GetSecurityPort')
        requests.post.assert_called_with(
            'http://1.2.3.4/url', data=data)

    @patch('fritzclient.minisoap.requests')
    def test_send_result(self, requests):
        response_data = (
            b'<?xml version="1.0"?>'
            b'<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/" '
            b's:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">'
            b'<s:Body>'
            b'<u:GetSecurityPortResponse xmlns:u="urn:dslforumorg:'
            b'service:DeviceInfo:1">'
            b'<NewSecurityPort>49443</NewSecurityPort>'
            b'</u:GetSecurityPortResponse>'
            b'</s:Body> </s:Envelope>'
        )
        requests.post.return_value = response_data
        result = soap.send('1.2.3.4', '/url', 'GetSecurityPort')
        self.assertEqual(result['NewSecurityPort'], 49443)
