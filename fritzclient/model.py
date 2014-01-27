class XMLObject(object):
    pass


class Root(object):
    """
    TODO: unused!
    """

    @staticmethod
    def decode(document, nsp):
        elem = Root()
        spec = document.find(nsp + 'specVersion')
        major = spec.find(nsp + 'major').text.strip()
        minor = spec.find(nsp + 'minor').text.strip()
        elem.spec_version = '{}.{}'.format(major, minor)


class Service(XMLObject):

    NS = [
        "{urn:schemas-upnp-org:service-1-0}"
    ]
    TAGNAME = 'service'

    @staticmethod
    def decode(xmlserv, ns):
        service = Service()
        service.service_type = xmlserv.find(ns + 'serviceType').text.strip()
        service.service_id = xmlserv.find(ns + 'serviceId').text.strip()
        service.control_url = xmlserv.find(ns + 'controlURL').text.strip()
        service.event_suburl = xmlserv.find(ns + 'eventSubURL').text.strip()
        service.scpdurl = xmlserv.find(ns + 'SCPDURL').text.strip()
        return service


class Device(XMLObject):

    NS = [
        "{urn:schemas-upnp-org:device-1-0}",
        "{urn:dslforum-org:device-1-0}"
    ]
    TAGNAME = 'device'

    @staticmethod
    def decode(xmldev, ns):
        device = Device()
        device.model_url = xmldev.find(ns + 'modelURL').text.strip()
        device.device_type = xmldev.find(ns + 'deviceType').text.strip()
        device.friendly_name = xmldev.find(
            ns + 'friendlyName').text.strip()
        device.manufacturer = xmldev.find(
            ns + 'manufacturer').text.strip()
        device.manufacturer_url = xmldev.find(
            ns + 'manufacturerURL').text.strip()
        device.model_description = xmldev.find(
            ns + 'modelDescription').text.strip()
        device.model_name = xmldev.find(
            ns + 'modelName').text.strip()
        device.model_number = xmldev.find(
            ns + 'modelNumber').text.strip()
        device.model_url = xmldev.find(ns + 'modelURL').text.strip()
        device.udn = xmldev.find(ns + 'UDN').text.strip()

        device.devices = []
        subdevices = xmldev.find(ns + 'deviceList')
        if subdevices is not None:
            for dev in subdevices:
                subdevice = Device.decode(dev, ns)
                device.devices.append(subdevice)

        device.services = []
        services = xmldev.find(ns + 'serviceList')
        if services is not None:
            for srv in services:
                service = Service.decode(srv, ns)
                device.services.append(service)

        device.icons = []
        icons = xmldev.find(ns + 'iconList')
        if icons is not None:
            for ico in icons:
                device.icons.append({
                    'depth': ico.find(ns + 'depth').text.strip(),
                    'height': ico.find(ns + 'height').text.strip(),
                    'mimetype': ico.find(ns + 'mimetype').text.strip(),
                    'url': ico.find(ns + 'url').text.strip(),
                    'width': ico.find(ns + 'width').text.strip()
                })

        return device
