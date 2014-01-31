import xml.etree.ElementTree as etree


etree.register_namespace('s', 'http://schemas.xmlsoap.org/soap/envelope/')


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
