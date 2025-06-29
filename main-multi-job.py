from os import wait
from time import sleep

from apscheduler.schedulers.background import BackgroundScheduler, BlockingScheduler, BaseScheduler
from apscheduler.job import Job


max_runs = 10


def display(
        message:str,                                # message to display
):
    global max_runs                                 # use a global counter
    max_runs -= 1                                   # decrement counter
    if max_runs < 0:
        raise KeyboardInterrupt                     # simulate CTRL-C
    print(f'display({message})')                    # print messsage


def run_job(fn, scheduler, *args):
    try:
        fn(*args)
    except KeyboardInterrupt:                       # manage CTRL-C
        print(f'{fn=} {scheduler=} {args=}')        # print details
        print('stopping scheduler')
        scheduler.shutdown(wait=False)              # this prevents the exception message loop
                                                    # we can use event listeners approach



def main():
    print("Hello from apscheduler-tutorials!")
    scheduler = BlockingScheduler()                 # create scheduler
    
    job1 = scheduler.add_job( run_job, 'interval', seconds=1, args=[display, scheduler, 'Job 1'] )
    job2 = scheduler.add_job( run_job, 'interval', seconds=2, args=[display, scheduler, 'Job 2'] )
    job3 = scheduler.add_job( run_job, 'interval', seconds=3, args=[display, scheduler, 'Job 3'] )
    
    print(f'starting scheduler for jobs')
    scheduler.start()
    print('this will never be printed or when the scheduler stops')
    

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print('this will never get caught')
