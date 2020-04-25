# -*- coding: utf-8 -*-

from flask_apscheduler import APScheduler
from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_ERROR, JobExecutionEvent
from apscheduler.schedulers.background import BackgroundScheduler

scheduler = APScheduler()


# @scheduler.task('cron', id='do_job_2', minute='*')
def job2():
    pass


def scheduler_listener(event: JobExecutionEvent):
    if event.code == EVENT_JOB_EXECUTED:
        print("任务开始执行... ...")
    if event.exception:
        print("The job crashed.")
    else:
        print("The job worked")


scheduler.add_listener(scheduler_listener, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR)
