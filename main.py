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

from aws_xray_sdk.core import xray_recorder



from spiders import rfs, usgs, taiwan, noaa
from common import transmit


# Get the current active segment or subsegment from the main thread.
current_entity = xray_recorder.get_trace_entity()
functions = [rfs, usgs, taiwan, noaa]


def app():
    print "Running spiders at %s" % datetime.now()
    for fn in functions:
        alerts = fn()
        transmit(alerts, current_entity)


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
