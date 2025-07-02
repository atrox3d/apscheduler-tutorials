from time import sleep

from apscheduler.schedulers.background import BackgroundScheduler, BlockingScheduler, BaseScheduler
from apscheduler.job import Job


class SimpleCounter:
    ''' 
    simple counter class, can be used instead of global counter
    or function attribute
    '''
    
    def __init__(self, start=0):
        self.value = start

    def increment(self) -> int:
        self.value += 1
        return self.value

    def __int__(self):
        return self.value


def display(
        message:str,                                # message to display
        counter:SimpleCounter,                      # counter instance
        max_runs:int,                               # max runs
        job_id=None,                                # job id instance guard
        scheduler:BaseScheduler=None                # scheduler instance guard
):
    '''
    this is the function to be scheduled
    i added some fancy counter, scheduler and job
    parameters just to explore them
    and expoloit them to shut down the scheduler
    '''
    print(f'display({message})')                    # print messsage
    
    runs = counter.increment()                      # increment counter
    print(f'{runs = }')
    
    if scheduler and job_id:                        # check we have objects
        job: Job = scheduler.get_job(job_id)        # get this job
        if job:
            print(f'  Inside job: My ID is {job.id}')
            print(f'  Inside job: Next run time is {job.next_run_time}')
            
    if runs >= max_runs:                                   # check for max runs
        print(f'removing job {job.id}')
        job.remove()                                # remove job
        print(f'shutting down scheduler')
        scheduler.shutdown(wait=False)              # shutdown scheduler


def main():
    '''
    basic example, creates the basic objs,
    schedules the job, modifies it and 
    starts the scheduler
    '''
    print("Hello from apscheduler-tutorials!")
    scheduler = BlockingScheduler()                 # create scheduler
    counter = SimpleCounter()                       # create counter
    
    job = scheduler.add_job(                        # add job to scheduler
        display,                                    # function to call
        'interval',                                 # trigger type
        seconds=2,                                  # interval
        args=[                                      # function positional args
                'every 2 seconds',                  # message
                counter,                            # counter instance
                5
        ],
    )
    
    # Now that the job is created, we modify it to pass its own ID and the scheduler
    scheduler.modify_job(
        job.id,                                     # job to modify
        kwargs={                                    # keyword args for function
            'job_id': job.id, 
            'scheduler': scheduler
        }
    )
    
    print(f'starting scheduler for job {job.id}')
    scheduler.start()
    print('this will never be printed or when the scheduler stops')
    

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
