import logging
import requests
from os import getenv
import keen
import base64
from sqlite_cache import SQLiteCache
from capparselib.parsers import CAPParser

ALERTED_USERPASS = getenv('ALERTED_USERPASS', 'admin:password')
RACK_ENV = getenv('RACK_ENV', 'development')
ALERTED_API = getenv('ALERTED_API', 'http://localhost:8000/api/v1/alerts/')

HEADERS = {'Content-Type': 'application/xml', 'Accept': 'application/xml',
           'Authorization': 'Basic %s' % base64.b64encode(str(ALERTED_USERPASS))}


def transmit(alerts):
    """
    A function to transmit XML to Alerted web service

    :param alerts: XML CAP1.2 alerts to transmit
    :return:
    """
    #
    # Determine if the alert can be parsed as valid CAP XML
    # This will be erased on each deploy to Heroku, but that's OK
    cache = SQLiteCache("/tmp/cache.db", capacity=5000)

    result = False

    for alert in alerts:
        alert = alert.replace('\n', '')

        name = "Unknown"

        try:
            alert_list = CAPParser(alert).as_dict()
            name = alert_list[0]['cap_sender']
            identifier = alert_list[0]['cap_id']
        except:
            identifier = ''
            logging.error("Potentially invalid alert")

        cache_key = '%s:id' % identifier
        active = cache.get(cache_key)
        if not active:
            cache.set(cache_key, "submitted")

            resp = requests.post(url=ALERTED_API, data=alert, headers=HEADERS)
            status_code = "%s" % resp.status_code

            if resp.status_code == 201:
                result = True

            transmit_to_keen("transmit", {"result": "%s" % str(result), "sender": "%s" % name,
                                          "status_code": "%s" % status_code, "identifier": "%s" % identifier})
    cache.close()
    return result


def transmit_to_keen(collection_name, msg):
    if RACK_ENV == "production":
        keen.add_event(collection_name, msg)

