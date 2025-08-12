from datetime import datetime, timedelta
from logging import ERROR
from time import sleep

from apscheduler.schedulers.background import BackgroundScheduler, BlockingScheduler, BaseScheduler
from apscheduler.events import EVENT_JOB_ERROR, JobExecutionEvent
from apscheduler.job import Job


SCHEDULER:BaseScheduler = None
def get_scheduler():
    global SCHEDULER
    if not SCHEDULER:
        # Using a timezone-aware scheduler is a good practice.
        SCHEDULER = BackgroundScheduler(timezone="UTC")
    return SCHEDULER


# --- Define a constant ID for the job ---
DECORATOR_JOB_ID = 'my_decorated_job'

# The decorator runs when this module is loaded.
# We add an 'id' to be able to find and modify it later.
@get_scheduler().scheduled_job(
        'date',
        id=DECORATOR_JOB_ID, # <-- This ID is crucial
        run_date=(datetime.now() + timedelta(seconds=5)),
        args=[f"Initial run scheduled for {(datetime.now() + timedelta(seconds=5)).replace(microsecond=0)}"]
)


def display(message:str):
    '''
    this is the function to be scheduled
    '''
    now = datetime.now().replace(microsecond=0)
    print(f'\n--- Job Executing ---')
    print(f'display({now  = !s})')
    print(f'display({message})')
    # Let's raise a more standard error for demonstration
    print(f'This run will fail to trigger the listener.')
    print(f'---------------------\n')
    raise ValueError("Simulating a job failure to trigger rescheduling.")


def all_events_listener(event):
    print(f'{type(event)=}')


# This listener will now MODIFY the job that failed.
def error_listener(event:JobExecutionEvent):
    print(f'\n--- Event Listener Triggered ---')
    print(f'Job {event.job_id} raised an exception: {event.exception!r}')

    # Check if the failed job is the one we want to reschedule
    if event.job_id == DECORATOR_JOB_ID:
        print(f'Caught error from job "{DECORATOR_JOB_ID}". Modifying it to run again.')
        scheduler = get_scheduler()
        new_run_time = datetime.now() + timedelta(seconds=10)

        # In v3, use modify_job and provide a new run_date
        scheduler.modify_job(
            job_id=DECORATOR_JOB_ID,
            run_date=new_run_time,
            args=[f"Rescheduled by listener to run at {new_run_time.replace(microsecond=0)}"]
        )
        print(f'Job "{DECORATOR_JOB_ID}" has been modified. New run time: {new_run_time}')
    else:
        print(f'Error was from a different job ({event.job_id}), not modifying.')
    print(f'------------------------------\n')


def main():
    print('MAIN| getting scheduler')
    scheduler = get_scheduler()


    print('MAIN| adding listener')
    scheduler.add_listener(error_listener, EVENT_JOB_ERROR)

    # We no longer need to call schedule_job().
    # The decorator has already added the job.

    print('MAIN| starting scheduler')
    scheduler.start()
    # In v3, we get a "Job" object
    job: Job = scheduler.get_job(DECORATOR_JOB_ID)
    if job:
        print(f'MAIN| Job "{job.id}" was created by the decorator, scheduled for: {job.next_run_time}')
    else:
        print(f'MAIN| ERROR: Could not find the decorated job.')

    print('MAIN| waiting 30 seconds to see the job fail and get rescheduled...')
    try:
        sleep(30)
    except (KeyboardInterrupt, SystemExit):
        print('MAIN| Interrupted.')
    finally:
        print(f'MAIN| Final jobs list: {scheduler.get_jobs()}')
        print('MAIN| stopping scheduler...')
        scheduler.shutdown(wait=True)


if __name__ == '__main__':
    main()
