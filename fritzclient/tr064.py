import logging
import socket

import requests

LOG = logging.getLogger(__name__)

SSDP_GRP = '239.255.255.250'
SSDP_PORT = 1900

DISCO_MESSAGE = (
    b'M-SEARCH * HTTP/1.1\n'
    b'Host: 239.255.255.250:1900\n'
    b'Man: "ssdp:discover"\n'
    b'MX: 5\n'
    b'ST: urn:dslforum-org:device:InternetGatewayDevice:1\n'
)


class SSDPError(Exception):
    pass


def discover():
    sock = socket.socket(socket.AF_INET,
                         socket.SOCK_DGRAM,
                         socket.IPPROTO_UDP)
    sock.settimeout(1.0)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)
    sock.sendto(DISCO_MESSAGE, (SSDP_GRP, SSDP_PORT))
    LOG.debug('Listening on {}'.format(sock))
    try:
        response = sock.recv(4096)
    except socket.error as exc:
        raise SSDPError(str(exc))
    else:

        output = {}
        for line in response.splitlines():
            if not line.strip():
                continue
            if line.startswith('HTTP/1.1'):
                _, status, _ = line.split()
                status = int(status)
                output['status_code'] = status
                continue

            name, value = line.split(':', 1)
            name = name.lower().strip()
            output[name] = value.strip()

        return output


def get_tr064desc(location):
    desc = requests.get(location)
    return desc.text
