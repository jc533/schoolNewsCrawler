from apscheduler.schedulers.blocking import BlockingScheduler

sched = BlockingScheduler()


# @sched.scheduled_job('interval', hours=1)
# def timed_job():
#     print('This job is run every three minutes.')


@sched.scheduled_job('cron', day_of_week='mon-sun', hour=21,minute=10)
def scheduled_job():
    print('This job is run every weekday at 5pm.')


sched.start()
