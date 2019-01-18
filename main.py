import logging
import json
from datetime import datetime
from spiders import rfs, usgs, taiwan, noaa
from common import transmit

log = logging.getLogger()
log.setLevel(logging.DEBUG)

functions = [rfs, usgs, taiwan, noaa]


def app():
    print("Running spiders at %s" % datetime.now())
    for fn in functions:
        alerts = fn()
        transmit(alerts)


def handler(event, context):
    log.debug("Received event {}".format(json.dumps(event)))
    response = {}

    try:
        print("Running spiders at %s" % datetime.now())
        results = []
        for fn in functions:
            alerts = fn()
            results.append(transmit(alerts))

        response['result'] = results
    except Exception as e:
        response['result'] = str(e)

    return {
        'statusCode': 200,
        'body': json.dumps(response)
    }
