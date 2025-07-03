from datetime import datetime, timedelta
import dis
from logging import ERROR
from operator import ge
import sched
from time import sleep

from apscheduler.schedulers.background import BackgroundScheduler, BlockingScheduler, BaseScheduler
from apscheduler.job import Job
from apscheduler.events import EVENT_JOB_ERROR, JobExecutionEvent


def display(message:str):
    '''
    this is the function to be scheduled
    '''
    now = datetime.now().replace(microsecond=0)
    print(f'display({now  = !s})')
    print(f'display({message})')
    raise KeyboardInterrupt


def all_events_listener(event):
    print(f'{type(event)=}')


def error_listener(event:JobExecutionEvent):
    print(f'{event=}')
    # print(f'{vars(event)=}')
    if event.exception:
        print(f'ERROR_LISTENER| {event.exception=}')
        print(f'ERROR_LISTENER| rescheduling job')
        schedule_job()
    else:
        print('ERROR_LISTENER| no exception')


SCHEDULER:BaseScheduler = None
def get_scheduler():
    global SCHEDULER
    if not SCHEDULER:
        SCHEDULER = BackgroundScheduler()
    return SCHEDULER


def schedule_job():
    print(f'SCHEDULE_JOB| scheduling job')
    scheduler = get_scheduler()
    now = datetime.now().replace(microsecond=0)
    print(f'SCHEDULE_JOB| {now  = !s}')
    when = (datetime.now() + timedelta(seconds=5)).replace(microsecond=0)
    print(f'SCHEDULE_JOB| {when = !s}')
    
    scheduler.add_job( display, 'date', run_date=when, args=[str(when)])
    

def main():
    print('MAIN| getting scheduler')
    scheduler = get_scheduler()
    print('MAIN| adding listener')
    scheduler.add_listener(error_listener, EVENT_JOB_ERROR)
    
    schedule_job()
    
    print('MAIN| starting scheduler')
    scheduler.start()
    
    print('MAIN| waiting 30 seconds...')
    sleep(30)
    
    print(f'{scheduler.get_jobs() = }')
    print('MAIN| stopping scheduler...')
    scheduler.shutdown(wait=True)


if __name__ == '__main__':
    main()

