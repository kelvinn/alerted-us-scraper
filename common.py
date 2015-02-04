import logging
import requests
from os import getenv
import base64
from capparselib.parsers import CAPParser

if getenv('ALERTED_USERPASS'):
    ALERTED_API = 'https://alerted.us/api/v1/alerts/'
    ALERTED_USERPASS = str(getenv('ALERTED_USERPASS'))
    RACK_ENV = "production"
else:
    ALERTED_API = 'http://localhost:8000/api/v1/alerts/'
    ALERTED_USERPASS = 'admin:password'  # This is the same default password used in the dev alerted website
    RACK_ENV = "development"

HEADERS = {'Content-Type': 'application/xml', 'Accept': 'application/xml',
            'Authorization': 'Basic %s' % base64.b64encode(ALERTED_USERPASS)}


def transmit(alert):
    """
    A function to transmit XML to Alerted web service

    :param alert: XML CAP1.2 alert to transmit
    :return:
    """
    alert = alert.replace('\n', '')
    # Determine if the alert can be parsed as valid CAP XML
    result = False
    name = "Unknown"
    try:
        alert_list = CAPParser(alert).as_dict()
        name = alert_list[0]['cap_sender']
    except:
        logging.error("Potentially invalid alert")

    resp = requests.post(url=ALERTED_API, data=alert, headers=HEADERS)
    status_code = "%s" % resp.status_code

    if resp.status_code == 201:
        result = True

    return result