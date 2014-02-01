import xml.etree.ElementTree as etree

import requests


etree.register_namespace('s', 'http://schemas.xmlsoap.org/soap/envelope/')


class SOAPError(Exception):
    """
    SOAP Fault Object. It has the following instance attributes:

        faultcode
            The SOAP fault code

        faultstring
            A descriptive error title

        detail
            Internal error details (XML string)

        http_url
            The URL which caused this error

        http_body
            The HTTP message sent to the remote URL which cause the error.

        http_headers
            The HTTP headers which were sent in the request that caused the
            error.
    """

    def __init__(self, msg, faultcode, faultstring, detail, http_url,
                 http_body, http_headers):
        super(SOAPError, self).__init__(msg)
        self.faultcode = faultcode
        self.faultstring = faultstring
        self.detail = detail
        self.http_url = http_url
        self.http_body = http_body
        self.http_headers = http_headers


def _parse_xml_value(value):
    if isinstance(value, basestring) and value.isdigit():
        return int(value)
    else:
        return value


class Container(object):
    """
    Simple container class for easy access to XML nodes.
    """

    def __init__(self, element):
        self._element = element

    def __getitem__(self, key):
        elems = self._element.findall('.//{}'.format(key))
        if len(elems) == 1:
            value = elems[0].text
            if value:
                return _parse_xml_value(value)
            else:
                return elems[0]
        elif len(elems) > 1:
            raise KeyError('Multiple elements found for key {}'.format(key))
        else:
            raise KeyError('No such element: {}'.format(key))

    def get(self, key, default=None):
        try:
            return self[key]
        except KeyError:
            return default


def render_message(context, method, args=None):
    """
    @param context: The namespace for the method element (a URN from the TR-064
                    standard).
    @param method: The method name (from the TR-064 standard)
    @param args: An optional dictionary of parameters.
    """
    if not args:
        args = {}

    etree.register_namespace('u', context)

    ns = 'http://schemas.xmlsoap.org/soap/envelope/'
    doc = etree.Element(etree.QName(ns, 'Envelope'))
    doc.set(etree.QName(ns, 'encodingStyle'),
            'http://schemas.xmlsoap.org/soap/encoding/')
    body = etree.Element(etree.QName(ns, 'Body'))
    method_el = etree.Element(etree.QName(context, method))
    for key, value in args.items():
        arg_el = etree.Element(key)
        arg_el.text = str(value)
        method_el.append(arg_el)
    body.append(method_el)
    doc.append(body)
    output = etree.tostring(doc)
    return output


def parse_response(response):
    root = etree.fromstring(response)
    envelope = root[0]
    body = envelope[0]
    return Container(body)


def execute(url, namespace, action, params=None):

    headers = {'soapaction': '#'.join((namespace, action)),
               'content-type': 'text/xml',
               'charset': 'utf-8'}

    payload = render_message(namespace, action, params)

    response = requests.post(url, data=payload, headers=headers)

    if not response.headers['content-type'].startswith('text/xml'):
        raise ValueError("Don't know how to handle content-type {}".format(
            response.headers['content-type']))

    if response.status_code != 200:
        try:
            ns = '{http://schemas.xmlsoap.org/soap/envelope/}'
            ns2 = '{urn:dslforum-org:control-1-0}'
            envelope = etree.fromstring(response.text)
            fault = envelope.find('./{0}Body/{0}Fault'.format(ns))
            detail = fault.find('./detail')
            error_code = detail.find(
                './{0}UPnPError/{0}errorCode'.format(ns2)).text.strip()
            error_desc = detail.find(
                './{0}UPnPError/{0}errorDescription'.format(ns2)).text.strip()
            error = SOAPError(
                '{}: {}'.format(error_code, error_desc),
                faultcode=fault.find('./faultcode').text.strip(),
                faultstring=fault.find('./faultstring').text.strip(),
                detail=etree.tostring(detail),
                http_url=url,
                http_body=payload,
                http_headers=headers
            )
        except Exception as exc:
            raise SOAPError(
                'Unparsable SOAP Error: {} from source {!r}'.format(
                    exc, response.text))
        else:
            raise error

    return parse_response(response.text)
