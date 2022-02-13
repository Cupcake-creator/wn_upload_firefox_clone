from apscheduler.schedulers.background import BackgroundScheduler
from .schedule import schedule_adds_on


def start():
    # Created background task
    scheduler = BackgroundScheduler()
    scheduler.add_job(schedule_adds_on, 'interval', minutes=90)
    scheduler.start()