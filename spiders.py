import requests
import requests_toolbelt.adapters.appengine
from lxml import etree
from google.appengine.api import memcache
from google.appengine.api import urlfetch

import feedparser

urlfetch.set_default_fetch_deadline(550)

# Use the App Engine Requests adapter. This makes sure that Requests uses
# URLFetch.
requests_toolbelt.adapters.appengine.monkeypatch()


def rfs():
    r = requests.get('http://www.rfs.nsw.gov.au/feeds/majorIncidentsCAP.xml')

    r.encoding = 'utf-8'

    tree = etree.fromstring(r.content.replace('\n          ', ''))

    scraped = tree.xpath(
        '/edxlde:EDXLDistribution[1]/edxlde:contentObject/edxlde:xmlContent/edxlde:embeddedXMLContent/cap:alert',
        namespaces={
            'edxlde': 'urn:oasis:names:tc:emergency:EDXL:DE:1.0',
            'georss': 'http://www.georss.org/georss',
            'cap': 'urn:oasis:names:tc:emergency:cap:1.2'
        })

    return [etree.tostring(x) for x in scraped]


def usgs():
    # Use requests so we can mock it out while testing
    r = requests.get('http://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/4.5_day.atom')
    d = feedparser.parse(r.content)
    alerts = []

    for entry in d['entries']:
        links = entry['links']
        for link in links:
            if link['type'] == 'application/cap+xml':
                link_href = link['href']
                cache_key = '%s:id' % link_href
                active = memcache.get(cache_key)
                if not active:
                    memcache.add(key=cache_key, value="submitted", time=3600)
                    resp = requests.get(link_href)
                    alerts.append(resp.content)
    return alerts


def taiwan():
    # Use requests so we can mock it out while testing
    r = requests.get('https://alerts.ncdr.nat.gov.tw/RssAtomFeed.ashx')
    d = feedparser.parse(r.content)
    alerts = []

    for entry in d['entries']:
        links = entry['links']
        for link in links:
            link_href = link['href']
            cache_key = '%s:id' % link_href
            active = memcache.get(cache_key)
            if not active:
                memcache.add(key=cache_key, value="submitted", time=3600)
                resp = requests.get(link_href)
                alerts.append(resp.content)
    return alerts


def allny():
    # Use requests so we can mock it out while testing
    r = requests.get('http://rss.nyalert.gov/CAP/Indices/_ALLNYCAP.xml')
    d = feedparser.parse(r.content)
    alerts = []

    for entry in d['entries']:
        link_href = entry['href']
        cache_key = '%s:id' % link_href
        active = memcache.get(cache_key)
        if not active:
            memcache.add(key=cache_key, value="submitted", time=3600)
            resp = requests.get(link_href)
            alerts.append(resp.content)
    return alerts


def noaa():
    # Use requests so we can mock it out while testing
    r = requests.get("https://alerts.weather.gov/cap/us.php?x=1")
    d = feedparser.parse(r.content)
    alerts = []

    for entry in d['entries']:
        links = entry['links']
        for link in links:
            link_href = link['href']
            cache_key = '%s:id' % link_href
            active = memcache.get(cache_key)
            if not active:
                memcache.add(key=cache_key, value="submitted", time=3600)
                resp = requests.get(link_href)
                alerts.append(resp.content)
    return alerts
