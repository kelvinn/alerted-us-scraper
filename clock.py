from apscheduler.schedulers.blocking import BlockingScheduler
from spiders import rfs


sched = BlockingScheduler()

@sched.scheduled_job('interval', minutes=3)
def timed_job():
    print "Running RFS"
    rfs()

sched.start()