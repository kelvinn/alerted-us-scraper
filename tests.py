import unittest

import os
import sys

# get this file's directory independent of where it's run from
here = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(here, "vendored"))

import responses
from capparselib.parsers import CAPParser
from common import transmit
from spiders import rfs, usgs, taiwan, sweden, noaa


def cleanup():
    to_remove_list = ["cache", "cache.db", "cache.rw.lock"]
    [os.remove(item) for item in to_remove_list if os.path.exists(item)]


class AppTestCase(unittest.TestCase):

    def setUp(self):
        cleanup()

    def tearDown(self):
        cleanup()

    @responses.activate
    def test_rfs_get(self):

        sample = open(r'data/bushfire.cap', 'r').read()
        responses.add(responses.GET, 'http://www.rfs.nsw.gov.au/feeds/majorIncidentsCAP.xml',
              body=sample, status=200,
              content_type='application/xml')
        result = rfs()
        self.assertEqual(59, len(result))

    @responses.activate
    def test_rfs_post(self):
        result = ['<cap:alert xmlns:cap="urn:oasis:names:tc:emergency:cap:1.2" xmlns:edxlde="urn:oasis:names:tc:emergency:EDXL:DE:1.0" xmlns:georss="http://www.georss.org/georss">\n<cap:identifier>2015-02-13T04:51:00-00:00:186162</cap:identifier>\n<cap:sender>webmaster@rfs.nsw.gov.au</cap:sender>\n<cap:sent>2015-02-13T04:51:00-00:00</cap:sent>\n<cap:status>Actual</cap:status>\n<cap:msgType>Alert</cap:msgType>\n<cap:scope>Public</cap:scope>\n<cap:code>urn:oasis:names:tc:emergency:cap:1.2:profile:CAP-AU:1.0</cap:code>\n<cap:incidents>186162</cap:incidents>\n<cap:info>\n  <cap:language>en-AU</cap:language>\n  <cap:category>Fire</cap:category>\n  <cap:event>Bushfire</cap:event>\n  <cap:responseType>Monitor</cap:responseType>\n  <cap:urgency>Expected</cap:urgency>\n  <cap:severity>Moderate</cap:severity>\n  <cap:certainty>Observed</cap:certainty>\n  <cap:eventCode>\n    <cap:valueName>https://govshare.gov.au/xmlui/handle/10772/6495</cap:valueName>\n    <cap:value>bushFire</cap:value>\n  </cap:eventCode>\n  <cap:effective>2015-02-13T04:51:00-00:00</cap:effective>\n  <cap:expires>2015-02-14T04:51:00-00:00</cap:expires>\n  <cap:senderName>NSW Rural Fire Service</cap:senderName>\n  <cap:headline>Wakool Rd, Wakool</cap:headline>\n  <cap:description>ALERT LEVEL: Advice\nLOCATION: Wakool Rd, Wakool, NSW 2710\nCOUNCIL AREA: Wakool\nSTATUS: under control\nTYPE: Bush Fire\nSIZE: 45 \nRESPONSIBLE AGENCY: Rural Fire Service\nUPDATED: 13 Feb 2015 15:51\n</cap:description>\n  <cap:instruction>A fire has started. There is no immediate danger. Stay up to date in case the situation changes.</cap:instruction>\n  <cap:web>http://www.rfs.nsw.gov.au/fire-information/fires-near-me</cap:web>\n  <cap:contact>webmaster@rfs.nsw.gov.au</cap:contact>\n  <cap:parameter>\n    <cap:valueName>FuelType</cap:valueName>\n    <cap:value>Forest</cap:value>\n  </cap:parameter>\n  <cap:parameter>\n    <cap:valueName>Location</cap:valueName>\n    <cap:value>Wakool Rd, Wakool, NSW 2710</cap:value>\n  </cap:parameter>\n  <cap:parameter>\n    <cap:valueName>FireDangerClass</cap:valueName>\n    <cap:value>1</cap:value>\n  </cap:parameter>\n  <cap:parameter>\n    <cap:valueName>Status</cap:valueName>\n    <cap:value>under control</cap:value>\n  </cap:parameter>\n  <cap:parameter>\n    <cap:valueName>Fireground</cap:valueName>\n    <cap:value>45 ha</cap:value>\n  </cap:parameter>\n  <cap:parameter>\n    <cap:valueName>AllocatedResources</cap:valueName>\n    <cap:value/>\n  </cap:parameter>\n  <cap:parameter>\n    <cap:valueName>ControlAuthority</cap:valueName>\n    <cap:value>Rural Fire Service</cap:value>\n  </cap:parameter>\n  <cap:parameter>\n    <cap:valueName>AlertLevel</cap:valueName>\n    <cap:value>Advice</cap:value>\n  </cap:parameter>\n  <cap:parameter>\n    <cap:valueName>CouncilArea</cap:valueName>\n    <cap:value>Wakool</cap:value>\n  </cap:parameter>\n  <cap:parameter>\n    <cap:valueName>IncidentName</cap:valueName>\n    <cap:value>Wakool Rd, Wakool</cap:value>\n  </cap:parameter>\n  <cap:parameter>\n    <cap:valueName>Evacuation</cap:valueName>\n    <cap:value/>\n  </cap:parameter>\n  <cap:resource>\n    <cap:resourceDesc>map</cap:resourceDesc>\n    <cap:mimeType>text/html</cap:mimeType>\n    <cap:uri>http://www.rfs.nsw.gov.au/fire-information/fires-near-me</cap:uri>\n  </cap:resource>\n  <cap:area>\n    <cap:areaDesc>Wakool Rd, Wakool, NSW 2710, Wakool</cap:areaDesc>\n    <cap:polygon>-35.4978,144.4698 -35.4982,144.4697 -35.4986,144.4694 -35.4989,144.4684 -35.4989,144.4674 -35.4988,144.4664 -35.4985,144.4655 -35.4978,144.464 -35.4979,144.4642 -35.4978,144.4639 -35.497,144.4638 -35.4967,144.4637 -35.4962,144.4635 -35.4959,144.4633 -35.4956,144.4631 -35.495,144.4629 -35.4946,144.463 -35.4942,144.4637 -35.4939,144.464 -35.4932,144.464 -35.4926,144.4643 -35.4923,144.4644 -35.4921,144.4649 -35.492,144.4654 -35.4918,144.4659 -35.4916,144.4665 -35.4916,144.4669 -35.4916,144.4673 -35.4916,144.4676 -35.4917,144.4679 -35.4919,144.4682 -35.4921,144.4686 -35.4923,144.469 -35.4929,144.469 -35.4933,144.4692 -35.4934,144.4693 -35.4941,144.4695 -35.4945,144.4693 -35.4949,144.469 -35.4954,144.4688 -35.4957,144.4686 -35.496,144.4688 -35.4963,144.4693 -35.4966,144.4695 -35.4969,144.4697 -35.4973,144.4699 -35.4976,144.4699 -35.4978,144.4698</cap:polygon>\n    <cap:circle>-35.4959,144.4539 0.0</cap:circle>\n    <cap:geocode>\n      <cap:valueName>urn:oasis:names:tc:emergency:cap:1.2:profile:CAP-AU:1.0:ISO3166-2</cap:valueName>\n      <cap:value>AU-NSW</cap:value>\n    </cap:geocode>\n  </cap:area>\n</cap:info>\n        </cap:alert>\n      ']

        responses.add(responses.POST, 'http://localhost:8000/api/v1/alerts/',
              status=201, content_type='application/xml')
        result2 = transmit(result)
        self.assertTrue(result2)

    @responses.activate
    def test_usgs_get(self):

        sample = open(r'data/usgs.atom', 'r').read()
        responses.add(responses.GET, 'http://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/4.5_day.atom',
              body=sample, status=200,
              content_type='application/xml')

        usgs_sample_cap = open(r'data/usgs.cap', 'r').read()
        responses.add(responses.GET, 'http://earthquake.usgs.gov/earthquakes/feed/v1.0/detail/nn00482627.cap',
              body=usgs_sample_cap, status=200,
              content_type='application/xml')

        result = usgs()
        alert = CAPParser(result[0].decode()).as_dict()
        self.assertEqual('USGS-earthquakes-nn00482627.703198.482627.20150214T025331.156Z.3', alert[0]['cap_id'])

    @responses.activate
    def test_taiwan_get(self):

        sample = open(r'data/taiwan.atom', 'r').read()
        responses.add(responses.GET, 'https://alerts.ncdr.nat.gov.tw/RssAtomFeed.ashx',
              body=sample, status=200,
              content_type='application/xml')

        usgs_sample_cap = open(r'data/taiwan.cap', 'r').read()
        responses.add(responses.GET, 'https://alerts.ncdr.nat.gov.tw/Capstorage/THB/2015/roadClose/THB-Bobe2015021417044705281791366163.cap',
              body=usgs_sample_cap, status=200,
              content_type='application/xml')

        result = taiwan()
        alert = CAPParser(result[0].decode('utf-8')).as_dict()
        self.assertEqual('THB-Bobe2015021417044705281791366163', alert[0]['cap_id'])

    @responses.activate
    def test_noaa_get(self):

        sample = open(r'data/noaa.atom', 'r').read()
        responses.add(responses.GET, "https://alerts.weather.gov/cap/us.php",
              body=sample, status=200,
              content_type='application/xml')

        noaa_sample_cap = open(r'data/noaa.cap', 'r').read()
        responses.add(responses.GET, 'http://alerts.weather.gov/cap/wwacapget.php',
              body=noaa_sample_cap, status=200,
              content_type='application/xml')

        result = noaa()

        alert = CAPParser(result[0].decode()).as_dict()
        self.assertEqual('NOAA-NWS-ALERTS-AK12539CADCECC.WinterWeatherAdvisory.12539CBBD120AK.AFGWSWNSB.bda790b45bcda3f2c9f1d0a1bdec3ec3', alert[0]['cap_id'])


    # This is waiting on NY to clean up their CAP feeds
    """
    @responses.activate
    def test_allny_get(self):

        sample = open(r'data/allnycap.xml', 'r').read()
        responses.add(responses.GET, 'http://rss.nyalert.gov/CAP/Indices/_ALLNYCAP.xml',
              body=sample, status=200,
              content_type='application/xml')


        ny_sample_cap = open(r'data/ny.cap', 'r').read()
        responses.add(responses.GET, "http://www.nyalert.gov/Public/News/GetCapAlert.aspx",
              body=ny_sample_cap, status=200,
              content_type='application/xml')

        result = allny()
        alert = CAPParser(result[0]).as_dict()
        self.assertEqual('THB-Bobe2015021417044705281791366163', alert[0]['cap_id'])
    """


if __name__ == '__main__':

    unittest.main()

