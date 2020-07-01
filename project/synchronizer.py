import threading
import time

current=0
connected=0
queue=[]

"""the thread with the number that is in the current position of the queue is executed"""
def Synchro(request):
    global current
    if (current>connected-1):
        current=0
    try:
        if (request==queue[current]):
            return 1
        else:
            return 0
    except IndexError:
        return 0

"""after one acquisition of a camera the queue index move to the next position"""
def Update():
    global current
    global connected
    if(current>connected-2):
        current=0
        #if the index returns to the first position the program waits
        time.sleep(10)
    else:
        current=current+1

"""adding the number associated to a camera at the end of queue"""
def addtoQueue(i):
    global queue
    global connected
    queue.append(i)
    connected=connected+1

"""removing the number associated to a camera at the end of queue"""
def removefromQueue(i):
    global queue
    global connected
    global current
    current=0
    try:
        queue.remove(i)
    except ValueError:
        connected=connected+1
    connected=connected-1

"""removing all the elements of the queue (in case of reboot)"""
def clearQueue():
    global queue
    global connected
    global current
    queue.clear()
    connected=0
    current=0
    
