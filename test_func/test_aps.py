from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime


def job():
    print("hello apscheduler!")


Scheduler = BackgroundScheduler()
# Scheduler.add_job(job, "interval", seconds=2, start_date=datetime(2019,1,2,14,25,30))
# Scheduler.add_job(job, "date", run_date=datetime(2019, 1, 2, 15, 43, 40))
# 每年的1-2月，9-12月每周六，日每天8:16:10:15
Scheduler.add_job(job, "cron", month="1-2, 9-12", day_of_week="5-6", hour="8", minute=16, second="45,50")
Scheduler.start()




while True:
    pass