  
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
token = 'eCmRDLwClKxu88KPMx7Qh5j5pc7aQCTPet2BXXwaKa9'
headers = {'content-type':'application/x-www-form-urlencoded','Authorization':'Bearer '+token}

app = Flask(__name__)


executors = {
    'default': ThreadPoolExecutor(16),
    'processpool': ProcessPoolExecutor(4)
}
sched = BackgroundScheduler(timezone='Asia/Singapore', executors=executors)


def job():
    msgs = get_noti_data()
    for msg in msgs:
        r = requests.post(url, headers=headers , data = {'message':msg})

# schedule.every().day.at("01:00").do(job)
sched.add_job(job, trigger="cron", hour='8',minute='30')

@app.route('/start')
def start():
    sched.start()
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