
from queue import Queue
import threading
from threading import Thread
import time

data = []
# A thread that produces data
def producer(out_q, eve):
    # Produce some data
    for i in range(10):
        data.append(i)
    out_q.put(data)
    time.sleep(10)
    for i in range(20):
        data.append(i)
    out_q.put(data)
    eve.set()

# A thread that consumes data
def consumer(in_q, eve):
    while not eve.isSet():
        time.sleep(0.2)
        # Get some data
        data = in_q.get()
        # Process the data
        for i in data:
            print(i)

# Create the shared queue and launch both threads
q = Queue()
eve = threading.Event()
t1 = Thread(target = consumer, args =(q, eve,))
t2 = Thread(target = producer, args =(q, eve,))
t1.start()
t2.start()
t1.join()
t2.join()
