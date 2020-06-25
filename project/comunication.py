import paho.mqtt.client as paho
import time
import threading
import json
import dicCamera
import Salva
import hdcam
import usbcam
import treDcam
import synchronizer

"""funzione che crea ed invia i json contenenti lo stato delle camere"""
def send():
    i=0
    while i<5:
        create=json.dumps(dicamera["cameras"][i])
        if(dicamera["cameras"][i]["type"]=="HD"):
            client.publish(pub_topic+dicamera["cameras"][i]["name"],create)
        else:
            client.publish(pub_topic+dicamera["cameras"][i]["type"],create)   
        i=i+1

"""arresta tutti i thread in esecuzione"""
def clearAll():
    e0.clear()
    e1.clear()
    e2.clear()
    e3.clear()
    e4.clear()

"""ricezione del messaggio in ingresso via mqtt e aggiornamento delle strutture dati delle camere,
  se il messaggio arriva dal topic "Vision/"+config["topic"]+"/Cameras/shutdown" con valore 1,
  il sistema si arresta"""
def on_message(client, userdata, msg) :
    global shutdown
    m_decode=str(msg.payload.decode("utf-8","ignore"))
    if msg.topic=="Vision/"+config["topic"]+"/Cameras/shutdown":
        shutdown=int(m_decode)
    else:
        Salva.SetMetadata(json.loads(m_decode),str(msg.topic)) 
    

    
def on_connect(client, userdata, flags, rc) :
    print("connessione mqtt riuscita")

e0=threading.Event()
e1=threading.Event()
e2=threading.Event()
e3=threading.Event()
e4=threading.Event()

shutdown=0

Broker = "hmi.polcevera.ubisive.it"

f=open("configuration.txt","r")

config=json.loads(f.read())

"""creazione dictonary contenente info su ogni camera"""
dicamera={"cameras":[]}
dicamera=dicCamera.createDic(dicamera,"MSI","VIS4X4","USB",0,status=config["usb"]["IP"])
dicamera=dicCamera.createDic(dicamera,"HD","HD1","PoE",0,IP=config["hd1"]["IP"])
dicamera=dicCamera.createDic(dicamera,"HD","HD2","PoE",0,IP=config["hd2"]["IP"])
dicamera=dicCamera.createDic(dicamera,"HD","HD3","PoE",0,IP=config["hd3"]["IP"])
dicamera=dicCamera.createDic(dicamera,"3D","D435","PoE",0,IP=config["3d"]["IP"])


pub_topic = "Vision/"+config["topic"]+"/Cameras/"
sub_topic = config["topic"]+"/+/ActualPosition"

devices={"HD1": config["hd1"]["IP"], "HD2": config["hd2"]["IP"], "HD3":config["hd3"]["IP"]}

client = paho.Client()

client.on_message = on_message
client.on_connect = on_connect

client.tls_set()
client.username_pw_set("client01",password="1oReANqFsMTWLRl8crcS4n4OO1fD83cdqrse13pogVSuhlcWZlZp2YTbC5RJ754")
client.connect(Broker,8883, 60)

client.subscribe(sub_topic)

client.loop_start()
clearAll()

"""main loop del programma nel quale i thread vengono lanciati e dentro il quale vengono inviati
   dei json di aggiornamento sullo stato delle camere. Con qualche modifica alla struttura del 
   programma può supportare un assegnazione dinamica delle camere"""
tempo=time.time()
while(shutdown==0):
    if(dicamera["cameras"][1]["status"]=="GenError" or dicamera["cameras"][2]["status"]=="GenError" or dicamera["cameras"][3]["status"]=="GenError"):
        clearAll()
        synchronizer.clearQueue()
        if(dicamera["cameras"][1]["status"]=="GenError"):
            dicamera["cameras"][1]["status"]="running"
        if(dicamera["cameras"][2]["status"]=="GenError"):
            dicamera["cameras"][2]["status"]="running"
        if(dicamera["cameras"][3]["status"]=="GenError"):
            dicamera["cameras"][3]["status"]="running"
        print("System Reboot")
        time.sleep(5)
    
    if (dicamera["cameras"][0]["status"]=="running" and not e0.is_set()):
        e0.set()
        synchronizer.addtoQueue(1)
        dicamera["cameras"][0]["error"]=="none"
        thread_usb=threading.Thread(target=usbcam.Photo, args=(e0,dicamera["cameras"][0],1,config["usb"]["exposure"]))
        thread_usb.start() 
    elif(dicamera["cameras"][0]["status"]=="stopped" and e0.is_set()):
        synchronizer.removefromQueue(1)
        e0.clear()  
    if (dicamera["cameras"][1]["status"]=="running" and not e1.is_set()):
        e1.set()
        synchronizer.addtoQueue(2)
        dicamera["cameras"][1]["error"]=="none"
        thread_hd=threading.Thread(target=hdcam.Photo, args=(e1,dicamera["cameras"][1],devices["HD1"],2,config["hd1"]["exposure"]))
        thread_hd.start()   
    elif(dicamera["cameras"][1]["status"]=="stopped" and e1.is_set()):
        synchronizer.removefromQueue(2)
        e1.clear()
    if (dicamera["cameras"][2]["status"]=="running" and not e2.is_set()):
        e2.set()
        synchronizer.addtoQueue(3)
        dicamera["cameras"][2]["error"]=="none"
        thread_hd2=threading.Thread(target=hdcam.Photo, args=(e2,dicamera["cameras"][2],devices["HD2"],3,config["hd2"]["exposure"]))
        thread_hd2.start() 
    elif(dicamera["cameras"][2]["status"]=="stopped" and e2.is_set()):
        synchronizer.removefromQueue(3)
        e2.clear()
    if (dicamera["cameras"][3]["status"]=="running" and not e3.is_set()):
        e3.set()
        synchronizer.addtoQueue(4)
        dicamera["cameras"][3]["error"]=="none"
        thread_hd3=threading.Thread(target=hdcam.Photo, args=(e3,dicamera["cameras"][3],devices["HD3"],4,config["hd3"]["exposure"]))
        thread_hd3.start() 
    elif(dicamera["cameras"][3]["status"]=="stopped" and e3.is_set()):
        synchronizer.removefromQueue(4)
        e3.clear()
    if (dicamera["cameras"][4]["status"]=="running" and not e4.is_set()):
        e4.set()
        synchronizer.addtoQueue(5)
        dicamera["cameras"][4]["error"]=="none"
        thread_tred=threading.Thread(target=treDcam.Photo, args=(e4,dicamera["cameras"][4],5,config["3d"]["colorize"]))
        thread_tred.start()
    elif(dicamera["cameras"][4]["status"]=="stopped" and e4.is_set()):
        synchronizer.removefromQueue(5)
        e4.clear()
    #tempo distanziamento invio json
    if((tempo+30)<time.time() and dicamera["cameras"][0]["status"]!="none"):
        send()
        tempo=time.time()

clearAll()
send()
client.loop_stop()
client.disconnect()


