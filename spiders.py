import requests
from os import getenv
import base64
import redis
from lxml import etree
from common import transmit


redis_url = getenv('REDISCLOUD_URL', 'redis://localhost:6379')

conn = redis.from_url(redis_url)


def rfs():
    r = requests.get('http://www.rfs.nsw.gov.au/feeds/majorIncidentsCAP.xml')
    r.encoding = 'utf-8'

    tree = etree.fromstring(r.text.replace('\n          ', ''))

    scraped = tree.xpath('/edxlde:EDXLDistribution[1]/edxlde:contentObject/edxlde:xmlContent/edxlde:embeddedXMLContent/cap:alert',
            namespaces = {
            'edxlde': 'urn:oasis:names:tc:emergency:EDXL:DE:1.0',
            'georss': 'http://www.georss.org/georss',
            'cap': 'urn:oasis:names:tc:emergency:cap:1.2'
        })

    for item in scraped:
        cap_id = item.xpath('.//cap:identifier/text()',
                            namespaces = {
                            'edxlde': 'urn:oasis:names:tc:emergency:EDXL:DE:1.0',
                            'georss': 'http://www.georss.org/georss',
                            'cap': 'urn:oasis:names:tc:emergency:cap:1.2'
                            })

        cache_key = '%s:id' % str(cap_id[0])
        active = conn.get(cache_key)
        if not active:
            conn.setex(cache_key, "submitted", 100000)
            transmit(etree.tostring(item))