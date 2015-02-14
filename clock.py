from apscheduler.schedulers.blocking import BlockingScheduler
from spiders import rfs
from common import transmit


sched = BlockingScheduler()

@sched.scheduled_job('interval', minutes=3)
def timed_job():
    print "Running RFS"
    alerts = rfs()
    transmit(alerts)

sched.start()