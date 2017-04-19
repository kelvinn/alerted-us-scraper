import logging

from google.appengine.api import taskqueue
from flask import Flask
from spiders import rfs, usgs, taiwan, noaa
from common import transmit
from flask import Flask

app = Flask(__name__)


@app.route('/tasks/scan/rfs')
def rfs_timed_job():
    print "Running RFS Spider"
    alerts = rfs()
    transmit(alerts)
    return 'OK', 200


@app.route('/tasks/scan/usgs')
def usgs_timed_job():
    print "Running USGS Spider"
    alerts = usgs()
    transmit(alerts)
    return 'OK', 200


@app.route('/tasks/scan/taiwan')
def taiwan_timed_job():
    print "Running Taiwan Spider"
    alerts = taiwan()
    transmit(alerts)
    return 'OK', 200


@app.route('/tasks/scan/noaa')
def noaa_timed_job():
    print "Running NOAA Spider"
    alerts = noaa()
    transmit(alerts)
    return 'OK', 200


@app.route('/tasks/scan')
def run_scan():
    taskqueue.add(method='GET', url='/tasks/scan/rfs')
    taskqueue.add(method='GET', url='/tasks/scan/noaa')
    taskqueue.add(method='GET', url='/tasks/scan/taiwan')
    taskqueue.add(method='GET', url='/tasks/scan/usgs')
    return 'Tasks started', 200


@app.route('/api/v1/alerts/', methods=['POST'])
def submitted_sample_data():
    return 'OK', 201


@app.errorhandler(500)
def server_error(e):
    # Log the error and stacktrace.
    logging.exception('An error occurred during a request.')
    return 'An internal error occurred.', 500
