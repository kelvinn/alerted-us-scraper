import requests
from lxml import etree


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