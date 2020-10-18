import time
import threading


# def loop():
#     print(f"Thread {threading.current_thread().name} is running")
#     n = 0
#     while n < 5:
#         n = n +1
#         print(f'Thread {threading.current_thread().name} >>> {n}')
#         time.sleep(1)
#     print(f"Thread {threading.current_thread().name} ended")


# print(f'thread {threading.current_thread().name} is running...')


def wait(n):
    time.sleep(n)
    print(f"{n} complete!")


def save_money(n):
    global balance

    # print(balance,'+',n)
    balance += n
    # print(balance,'-',n)
    balance -= n
    # print(balance)


def run_thread(n):
    for i in range(1000000):
        lock.acquire()
        try:
            save_money(n)
        except:
            lock.release()


if __name__ == '__main__':

    balance = 0
    lock = threading.Lock()

    t1 = threading.Thread(target=run_thread, args=(5,))
    t2 = threading.Thread(target=run_thread, args=(8,))

    t1.start()

    t2.start()

    t1.join()
    t2.join()

    print(balance)