from apscheduler.schedulers.blocking import BlockingScheduler


sched = BlockingScheduler()
print('1')


@sched.scheduled_job('interval', minutes=1)
def some_job():
    print('hello')


sched.start()
