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
        identifier = ''
        active = False

        try:
            alert_list = CAPParser(alert).as_dict()
            name = alert_list[0]['cap_sender']
            identifier = str(alert_list[0]['cap_id'])
            active = cache.get(identifier)
        except:
            logging.error("Potentially invalid alert")

        if not active and identifier:


            resp = requests.post(url=ALERTED_API, data=alert, headers=HEADERS, verify=False)

            if resp.status_code == 201:
                print "Successfully submitted alert %s" % identifier
                cache.set(identifier, "submitted")
                result = True
            else:
                print "Unable to submit alert %s" % identifier

    cache.close()
    return result

