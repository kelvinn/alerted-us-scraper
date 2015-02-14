import requests
from lxml import etree
import feedparser
import redis
from os import getenv


REDIS_URL = getenv('REDISCLOUD_URL', 'redis://localhost:6379')
conn = redis.from_url(REDIS_URL)


def rfs():
    r = requests.get('http://www.rfs.nsw.gov.au/feeds/majorIncidentsCAP.xml')

    r.encoding = 'utf-8'

    tree = etree.fromstring(r.content.replace('\n          ', ''))

    scraped = tree.xpath('/edxlde:EDXLDistribution[1]/edxlde:contentObject/edxlde:xmlContent/edxlde:embeddedXMLContent/cap:alert',
            namespaces = {
            'edxlde': 'urn:oasis:names:tc:emergency:EDXL:DE:1.0',
            'georss': 'http://www.georss.org/georss',
            'cap': 'urn:oasis:names:tc:emergency:cap:1.2'
        })

    return [etree.tostring(x) for x in scraped]


def usgs():

    # Use requetss so we can mock it out while testing
    r = requests.get('http://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/4.5_day.atom')
    d = feedparser.parse(r.content)
    alerts = []

    for entry in d['entries']:
        links = entry['links']
        for link in links:
            if link['type'] == 'application/cap+xml':
                link_href = link['href']
                cache_key = '%s:id' % link_href
                active = conn.get(cache_key)
                if not active:
                    conn.setex(cache_key, "submitted", 100000)
                    resp = requests.get(link_href)
                    alerts.append(resp.content)
    return alerts