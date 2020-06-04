import threading

current=0
connected=0
queue=[]

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

def Update():
    global current
    global connected
    if(current>connected-2):
        current=0
    else:
        current=current+1

    
def addtoQueue(i):
    global queue
    global connected
    
    queue.append(i)
    connected=connected+1

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

def clearQueue():
    global queue
    global connected
    global current
    queue.clear()
    connected=0
    current=0
    
