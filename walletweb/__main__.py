import multiprocessing
from app import run_app
from job import run_job

p1 = multiprocessing.Process(name='p1', target=run_app)
p = multiprocessing.Process(name='p', target=run_job)
p1.start()
p.start()

