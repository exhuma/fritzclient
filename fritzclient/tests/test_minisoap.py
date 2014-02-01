from unittest import TestCase
import xml.etree.ElementTree as etree

from mock import patch, create_autospec
from requests import Response

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

    @patch('fritzclient.minisoap.requests')
    def test_execute_faulty_content_type(self, mock_requests):

        mock_response = create_autospec(Response)
        mock_response.headers = {
            'content-type': 'bar'
        }
        mock_requests.post.return_value = mock_response
        with self.assertRaises(ValueError):
            soap.execute('/foo', 'ns', 'action')

    @patch('fritzclient.minisoap.requests')
    def test_execute_fault(self, mock_requests):

        mock_response = create_autospec(Response)
        mock_response.headers = {
            'content-type': 'text/xml'
        }
        mock_response.status_code = 500
        mock_response.text = """
        <s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/"
                s:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">
            <s:Body>
                <s:Fault>
                    <faultcode>s:Client</faultcode>
                    <faultstring>UPnPError</faultstring>
                    <detail>
                        <UPnPError xmlns="urn:dslforum-org:control-1-0">
                            <errorCode>401</errorCode>
                            <errorDescription>Invalid Action</errorDescription>
                        </UPnPError>
                    </detail>
                </s:Fault>
            </s:Body>
        </s:Envelope>
        """

        mock_requests.post.return_value = mock_response
        with self.assertRaises(soap.SOAPError):
            soap.execute('/foo', 'ns', 'action')

        try:
            soap.execute('/foo', 'ns', 'action')
        except soap.SOAPError as exc:
            result = {
                'faultcode': exc.faultcode,
                'faultstring': exc.faultstring,
            }
            expected = {
                'faultcode': 's:Client',
                'faultstring': 'UPnPError',
            }
            self.assertEqual(result, expected)
            self.assertIn('401', exc.detail)
            self.assertIn('Invalid Action', exc.detail)

# vim: set path+=fritzclient :
