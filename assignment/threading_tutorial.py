import logging
from multiprocessing import Pool
import os, time, random

logging.basicConfig(level=logging.DEBUG, format='(%(threadName)-9s) %(message)s', )


def long_time_task(name):
    logging.debug('Run task %s (%s)...' % (name, os.getpid()))
    start = time.time()
    time.sleep(random.random() * 3)
    end = time.time()
    logging.debug('Task %s runs %0.2f seconds.' % (name, (end - start)))


if __name__ == '__main__':
    logging.debug('Parent process %s.' % os.getpid())
    p = Pool(4)
    for i in range(5):
        p.apply_async(long_time_task, args=(i,))
    logging.debug('Waiting for all subprocesses done...')
    p.close()
    p.join()
    logging.debug('All subprocesses done.')
