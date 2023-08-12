#!/usr/bin/python3

import threading
import time
import server


def run():
    time.sleep(1)
    while 1:
        print(1)
        time.sleep(1)


print('a')
t1 = threading.Thread(target=server.main.run, args=())
t2 = threading.Thread(target=server.main.run, args=())
t3 = threading.Thread(target=server.main.run, args=())

print('a')
t1.start()
print('a')
t2.start()
print('a')
t3.start()
print('a')
t1.join()
t2.join()
t3.join()