  
from threading import Thread
import time
import requests
from flask import Flask
from noti import get_noti_data
from datetime import datetime
import schedule
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor

url = 'https://notify-api.line.me/api/notify'
token = 'TiaiYEoFnQIghXI8GXz3311xspBdHwEWNsFc3KLSyYi'
headers = {'content-type':'application/x-www-form-urlencoded','Authorization':'Bearer '+token}

app = Flask(__name__)


executors = {
    'default': ThreadPoolExecutor(16),
    'processpool': ProcessPoolExecutor(4)
}
sched = BackgroundScheduler(timezone='Asia/Singapore', executors=executors)

def testing1():
    print ("testing1 - every 2 min...")


def job():
    msgs = get_noti_data()
    for msg in msgs:
        r = requests.post(url, headers=headers , data = {'message':msg})

sched.add_job(testing1, 'cron', id='run_every_2_min', minute='*/2')
sched.add_job(job, trigger="cron", hour='8',minute='30')

@app.route("/")
def noti():
    job()
    return "200"

@app.route('/resume')
def resume():
    sched.resume()
    return "200"

@app.route('/stop')
def stop():
    sched.pause()
    return "200"

@app.route('/renew_token/<new_token>')
def new_token(new_token):
    sched.pause()
    token = new_token
    sched.resume()
    return "200"

if __name__ == '__main__':
    app.run(port=200,use_reloader=False)