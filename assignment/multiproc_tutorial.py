import logging
import os, time, random
import threading

logging.basicConfig(level=logging.DEBUG, format='(%(threadName)-9s) %(message)s', )


def long_time_task(name):
    logging.debug('Run task %s (%s)...' % (name, os.getpid()))
    start = time.time()
    time.sleep(random.random() * 3)
    end = time.time()
    logging.debug('Task %s runs %0.2f seconds.' % (name, (end - start)))


if __name__ == '__main__':
    logging.debug('Parent process %s.' % os.getpid())

    ts = list()
    for i in range(5):
        ts.append(threading.Thread(target=long_time_task, args=(i,)))

    for t in ts:
        t.start()

    logging.debug('Waiting for all subprocesses done...')
    for t in ts:
        t.join()

    logging.debug('All subprocesses done.')
