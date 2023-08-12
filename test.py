import threading
import time

# function which takes some time to process
def say(i):
    time.sleep(1)
    print(i)
    while 1:
        print(i)
        time.sleep(1)


threads = []

print('z')
thread = threading.Thread(target=say, args=('abc',))
thread.start()
threads.append(thread)
print('z')

print('z')
thread = threading.Thread(target=say, args=('bca',))
thread.start()
threads.append(thread)
print('z')

"""for i in range(10):
    thread = threading.Thread(target=say, args=(i,))
    print('a')
    thread.start()
    print('a')
    threads.append(thread)
    print('a')
"""
# wait for all threads to complete before main program exits
for thread in threads:
    thread.join()