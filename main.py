from spiders import rfs, usgs, taiwan, noaa
from common import transmit


def rfs_timed_job():
    print "Running RFS Spider"
    alerts = rfs()
    transmit(alerts)

def usgs_timed_job():
    print "Running USGS Spider"
    alerts = usgs()
    transmit(alerts)

def taiwan_timed_job():
    print "Running Taiwan Spider"
    alerts = taiwan()
    transmit(alerts)

def noaa_timed_job():
    print "Running NOAA Spider"
    alerts = noaa()
    transmit(alerts)

if __name__ == "__main__":
    rfs_timed_job()
    usgs_timed_job()
    taiwan_timed_job()
    noaa_timed_job()