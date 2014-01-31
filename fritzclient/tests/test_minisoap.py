from unittest import TestCase
import xml.etree.ElementTree as etree

import fritzclient.minisoap as soap


class TestMiniSoap(TestCase):
    """
    Test a simplified SOAP implementation.
    """

    def test_render_message(self):
        result = soap.render_message('context', 'GetSecurityPort')
        envelope = etree.fromstring(result)
        body = envelope[0]
        self.assertEqual(body[0].tag, '{context}GetSecurityPort')

    def test_render_message_with_args(self):
        result = soap.render_message('urn:dslforum-org:service:DeviceConfig',
                                     'ConfigurationStarted',
                                     args={
                                         'NewSessionID': 'foo',
                                         'SillySecondArg': 20
                                     })
        envelope = etree.fromstring(result)
        body = envelope[0]
        expected = {
            'NewSessionID': 'foo',
            'SillySecondArg': '20'
        }
        result = {_.tag: _.text for _ in body[0]}
        self.assertEqual(result, expected)

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


# vim: set path+=fritzclient :
