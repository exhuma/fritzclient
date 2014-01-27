import xml.dom.minidom as dom

import requests


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
        elems = self._element.getElementsByTagName(key)
        if len(elems) == 1:
            value = elems[0].firstChild.nodeValue
            if value:
                return _parse_xml_value(value)
            else:
                return elems[0].firstChild
        elif len(elems) > 1:
            raise KeyError('Multiple elements found for key {}'.format(key))
        else:
            raise KeyError('No such element: {}'.format(key))


def render_message(host, url, method):
    impl = dom.getDOMImplementation()
    ns = 'http://schemas.xmlsoap.org/soap/envelope/'
    doc = impl.createDocument(ns, 's:Envelope', None)
    root = doc.documentElement
    root.setAttribute('xmlns:s', ns)
    root.setAttribute('s:encodingStyle',
                      'http://schemas.xmlsoap.org/soap/encoding/')
    envelope = doc.createElementNS(ns, 's:Envelope')
    root.appendChild(envelope)
    body = doc.createElementNS(ns, 's:Body')
    method = doc.createElementNS('', 'u:' + method)
    method.setAttribute('xmlns:u', "urn:dslforumorg:service:DeviceInfo:1")
    body.appendChild(method)
    envelope.appendChild(body)
    root.appendChild(envelope)
    return doc.toxml()


def parse_response(response):
    doc = dom.parseString(response)
    root = doc.documentElement
    envelope = root.firstChild
    body = envelope.firstChild
    return Container(body)


def send(host, url, method):
    response = requests.post(
        'http://{}{}'.format(host, url),
        data=render_message(host, url, method))
    print requests
    print requests.post
    print response
    return parse_response(response)
