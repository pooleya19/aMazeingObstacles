import time
from threading import Thread

def a():
    for i in range(0,100):
        time.sleep(1)
        print("a",i)

def b():
    for i in range(0,100):
        time.sleep(5)
        print("b",i)

aThread = Thread(target=a)
bThread = Thread(target=b)

aThread.start()
print("AThread Started")
bThread.start()
print("BThread Started")