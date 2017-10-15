from apscheduler.schedulers.blocking import BlockingScheduler
from spiders import rfs, usgs, taiwan, noaa
from common import transmit
from pytz import utc


sched = BlockingScheduler(timezone=utc)


@sched.scheduled_job('interval', minutes=3)
def rfs_timed_job():
    print "Running RFS Spider"
    alerts = rfs()
    transmit(alerts)


@sched.scheduled_job('interval', minutes=3)
def usgs_timed_job():
    print "Running USGS Spider"
    alerts = usgs()
    transmit(alerts)


@sched.scheduled_job('interval', minutes=10)
def taiwan_timed_job():
    print "Running Taiwan Spider"
    alerts = taiwan()
    transmit(alerts)


@sched.scheduled_job('interval', minutes=5)
def noaa_timed_job():
    print "Running NOAA Spider"
    alerts = noaa()
    transmit(alerts)

sched.start()