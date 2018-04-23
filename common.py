import logging
import os
import sys
from os import getenv
import base64

# get this file's directory independent of where it's run from
here = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(here, "vendored"))

import requests
from capparselib.parsers import CAPParser
from dogpile.cache import make_region


ALERTED_USERPASS = getenv('ALERTED_USERPASS', 'admin:password')
RACK_ENV = getenv('RACK_ENV', 'development')
ALERTED_API = getenv('ALERTED_API', 'http://localhost:8000/api/v1/alerts/')

HEADERS = {'Content-Type': 'application/xml',
           'Authorization': 'Basic %s' % base64.b64encode(str(ALERTED_USERPASS))}

REDIS_URL = getenv('REDIS_URL', 'redis://localhost:6379/0')


def get_cache():
    """
    A function to return a filesystem based cache object

    :return:
    """
    if RACK_ENV == "development":
        region = make_region().configure(
            'dogpile.cache.dbm',
            expiration_time=86400,
            arguments={
                "filename": "cache"
            }
        )
    elif RACK_ENV == "production":
        region = make_region().configure(
            'dogpile.cache.redis',
            arguments={
                'url': REDIS_URL,
                'redis_expiration_time': 60 * 60 * 2,  # 2 hours
                'distributed_lock': True
            }
        )

    return region


def transmit(alerts):
    """
    A function to transmit XML to Alerted web service

    :param alerts: XML CAP1.2 alerts to transmit
    :return:
    """
    #
    # Determine if the alert can be parsed as valid CAP XML
    # This will be erased on each deploy to Heroku, but that's OK
    cache = get_cache()
    result = False

    logging.info("Querying cache and attempting to transmit %s alerts" % len(alerts))
    for alert in alerts:
        alert = alert.replace('\n', '')

        identifier = ''
        active = False

        try:
            alert_list = CAPParser(alert).as_dict()
            identifier = str(alert_list[0]['cap_id'])
            active = cache.get(identifier)
        except:
            logging.error("Potentially invalid alert")

        if not active and identifier:

            resp = requests.post(url=ALERTED_API, data=alert, headers=HEADERS)

            if resp.status_code == 201:
                cache.set(identifier, "submitted")
                result = True
            elif resp.status_code == 400:
                print "Invalid query (duplicate?) %s" % identifier
                cache.set(identifier, "invalid")
            else:
                print "Unable to submit alert (%s) %s" % (str(resp.status_code), identifier)
    return result

