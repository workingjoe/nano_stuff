from threading import Thread 
import time

def BigBox(color):
    while True:
        print(f'{color} Bigbox is open for 5 seconds')
        time.sleep(5)
        print(f'{color} Bigbox is closed for 5 seconds')
        time.sleep(5)


def SmallBox(color):
    while True:
        print(f'{color} smallbox is open for 1 second')
        time.sleep(1)
        print(f'{color} smallbox is closed for 1 second')
        time.sleep(1)

# target = assign function to execute in thread
# args() is a LIST so either () or ('item',)
bigBoxThread = Thread(target=BigBox,args=(['Red']))
smallBoxThread = Thread(target=SmallBox, args=(['Blue']))

# keep track of background thread as a daemon -- why???
bigBoxThread.daemon = True
smallBoxThread.daemon = True

# start the threads
bigBoxThread.start()
smallBoxThread.start()

start = time.time()
current = time.time()
timeout = 20

# let this main task just run for a while and let threads output
# then when main exists the background threads will die
print(f'This program will run for {timeout} seconds')
while (current - start) < timeout:
    current = time.time()
    
