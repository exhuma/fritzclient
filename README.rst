Python FritzBox Client
======================

Loosely based on the `TR-064 standard`_.

AVM Notes on the standard:

* `First Steps`_
* `Technical Notes`_


.. _First Steps: http://www.avm.de/de/Extern/files/tr-064/AVM_Technical_Note_-_Konfiguration_ueber_TR-064.pdf
.. _Technical Notes: http://www.avm.de/de/Extern/files/tr-064/AVM_TR-064_first_steps.pdf
.. _TR-064 standard: http://www.broadband-forum.org/techincal/download/TR-064.pdf


Optional Implementation Ideas
=============================

Implement SSDP
--------------

The application should trigger a discovery by sending out a "SEARCH" packet to
UDP multicast 239.255.255.250 port 1900. This should trigger the CPE device to
send out a NOTIFY packet, containing all required info.

It seems that the FritzBox does not comply to the standard at 100%.

Example Search Request::

    M-SEARCH * HTTP/1.1
    Host: 239.255.255.250:1900
    ST: urn:dslforum.org:device:InternetGatewayDevice:1
    Man: "ssdp:discover"
    MX: 10

Alternative ST (observed on the net)::

    ST: urn:schemas-upnp-org:device:InternetGatewayDevice:1


Example NOTIFY message (as observed on the net. May be FritzBox specific!)::

    NOTIFY * HTTP/1.1
    HOST: 239.255.255.250:1900
    LOCATION: http://192.168.1.138:49000/igddesc.xml
    SERVER: FRITZ!Box Fon WLAN 7390 UPnP/1.0 AVM FRITZ!Box Fon WLAN7390 84.05.52
    CACHE-CONTROL: max-age=1800
    NT: uuid:75802409-bccb-40e7-8e6b-0896D74C6BF8
    NTS: ssdp:alive
    USN: uuid:75802409-bccb-40e7-8e6b-0896D74C6BF8
