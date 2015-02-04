from apscheduler.schedulers.blocking import BlockingScheduler
from spiders import rfs


sched = BlockingScheduler()

@sched.scheduled_job('interval', seconds=20)
def timed_job():
    print "Running RFS"
    rfs()

sched.start()