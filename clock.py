from apscheduler.schedulers.blocking import BlockingScheduler
from spiders import rfs, usgs, taiwan, noaa
from common import transmit


sched = BlockingScheduler()

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

@sched.scheduled_job('interval', minutes=3)
def taiwan_timed_job():
    print "Running Taiwan Spider"
    alerts = taiwan()
    transmit(alerts)

@sched.scheduled_job('interval', minutes=3)
def noaa_timed_job():
    print "Running NOAA Weather Spider"
    alerts = noaa()
    transmit(alerts)

sched.start()