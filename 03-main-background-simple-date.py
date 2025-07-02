from datetime import datetime, timedelta
import dis
from time import sleep

from apscheduler.schedulers.background import BackgroundScheduler, BlockingScheduler, BaseScheduler
from apscheduler.job import Job


def display(message:str):
    '''
    this is the function to be scheduled
    '''
    now = datetime.now().replace(microsecond=0)
    print(f'display({now  = !s})')
    print(f'display({message})')


def main():
    scheduler = BackgroundScheduler()
    
    # this is a simpler but bad practice
    # it does not take in account edge cases
    # for seconds > 60
    when = datetime(
            datetime.now().year,
            datetime.now().month,
            datetime.now().day,
            datetime.now().hour,
            datetime.now().minute,
            datetime.now().second + 5
        )

    # best practice
    when = ((
                datetime.now()          # get current time
                + timedelta(seconds=5)  # add safely 5 seconds
            )
            .replace(microsecond=0)     # remove decimals for seconds
    )
    
    now = datetime.now().replace(microsecond=0)
    print(f'{now  = !s}')
    print(f'{when = !s}')
    
    scheduler.add_job(
        display,
        'date',
        run_date=when,
        args=[str(when)]
    )
    
    print('starting scheduler')
    scheduler.start()
    
    print('waiting 10 seconds...')
    sleep(10)
    
    print(f'{scheduler.get_jobs() = }')
    print('stopping scheduler...')
    scheduler.shutdown(wait=True)



if __name__ == '__main__':
    main()

