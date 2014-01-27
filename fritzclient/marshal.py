import xml.etree.ElementTree as etree

from fritzclient.model import XMLObject


def decode(data):
    document = etree.fromstring(data)
    tag = document.tag

    if not tag.endswith('root'):
        raise ValueError('Unsupported data')

    for cls in XMLObject.__subclasses__():
        for ns in cls.NS:
            if ns in tag:
                main_element = document.find(ns + cls.TAGNAME)
                return cls.decode(main_element, ns)

    raise ValueError('Unsupported element: {!r}'.format(tag))
