from noti import get_noti_data
import time
import requests
from apscheduler.schedulers.blocking import BlockingScheduler

def testing1():
    print ("testing1 - every 2 min...")

def testing2():
    msgs = get_noti_data()
    for msg in msgs:
        r = requests.post(url, headers=headers , data = {'message':msg})
    
if __name__ == '__main__':
    sched = BlockingScheduler()
    sched.add_job(testing1, 'interval', id='run_every_2_min', minutes=3)
    sched.add_job(testing2, 'cron', id='run_at_7_pm', hour='8')
    sched.start()