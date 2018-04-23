import sys
import logging
import os
import json
from datetime import datetime

log = logging.getLogger()
log.setLevel(logging.DEBUG)

# get this file's directory independent of where it's run from
here = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(here, "vendored"))

from spiders import rfs, usgs, taiwan, noaa
from common import transmit


def app():
    print "Running NOAA Spider at %s" % datetime.now()
    alerts = noaa()
    transmit(alerts)


def handler(event, context):
    log.debug("Received event {}".format(json.dumps(event)))
    response = {}

    try:
        print "Running NOAA Spider at %s" % datetime.now()
        alerts = noaa()
        response['result'] = transmit(alerts)
    except Exception as e:
        response['result'] = str(e)

    return {
        'statusCode': 200,
        'body': json.dumps(response)
    }
