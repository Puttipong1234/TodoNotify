from noti import get_noti_data
import time
import requests

def testing1():
    print ("testing1 - every 2 min...")

def testing2():
    msgs = get_noti_data()
    for msg in msgs:
        r = requests.post(url, headers=headers , data = {'message':msg})
    
if __name__ == '__main__':
    from apscheduler.schedulers.blocking import BlockingScheduler
    sched = BlockingScheduler()
    sched.add_job(testing1, 'cron', id='run_every_2_min', minute='*/2')
    sched.add_job(testing2, 'cron', id='run_at_7_pm', hour='8')
    sched.start()