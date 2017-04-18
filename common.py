import logging
import requests
import requests_toolbelt.adapters.appengine
import base64
from capparselib.parsers import CAPParser
from google.appengine.api import memcache
from google.appengine.api import urlfetch
from models import Settings

urlfetch.set_default_fetch_deadline(300)

# Use the App Engine Requests adapter. This makes sure that Requests uses
# URLFetch.
requests_toolbelt.adapters.appengine.monkeypatch()


def transmit(alerts):
    """
    A function to transmit XML to Alerted web service

    :param alerts: XML CAP1.2 alerts to transmit
    :return:
    """
    #
    # Determine if the alert can be parsed as valid CAP XML
    # This will be erased on each deploy to Heroku, but that's OK

    RACK_ENV = Settings.get('RACK_ENV', "development")
    ALERTED_USERPASS = Settings.get('ALERTED_USERPASS', "admin:password")
    ALERTED_API = Settings.get('ALERTED_API', "http://localhost:8080/api/v1/alerts/")

    HEADERS = {'Content-Type': 'application/xml', 'Accept': 'application/xml',
               'Authorization': 'Basic %s' % base64.b64encode(str(ALERTED_USERPASS))}

    result = False

    for alert in alerts:
        alert = alert.replace('\n', '')

        identifier = ''
        active = False

        try:
            alert_list = CAPParser(alert).as_dict()
            identifier = str(alert_list[0]['cap_id'])
            logging.info(identifier)
            active = memcache.get(identifier)

        except:
            logging.error("Potentially invalid alert")

        if not active and identifier:

            resp = requests.post(url=ALERTED_API, data=alert, headers=HEADERS, verify=False)

            if resp.status_code == 201:
                memcache.add(key=identifier, value="submitted", time=3600)
                result = True
            elif resp.status_code == 400:
                print "Invalid query (duplicate?) %s" % identifier
                memcache.add(key=identifier, value="submitted", time=3600)
            else:
                print "Unable to submit alert (%s) %s" % (str(resp.status_code), identifier)
    return result
