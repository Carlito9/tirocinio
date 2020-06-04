
from pypylon import pylon,genicam
import platform
import threading
import time
import Salva
import numpy as np
import traceback
import synchronizer


def Photo(e,hd,device,token,exp):
    
    try:
        if device=="N/A":
            raise Exception('This camera is not avaiable')
    
        tlf = pylon.TlFactory.GetInstance() 
        dev=tlf.EnumerateDevices()
        i=0
        while True:
            if(dev[i].GetIpAddress()==device):
                break
            i=i+1
            if(i==len(dev)):
                raise Exception('This camera is not avaiable')
        
        cam = pylon.InstantCamera(tlf.CreateDevice(dev[i]))
        cam.Open()
        img = pylon.PylonImage()
        print(hd["name"]+" camera started.")
        if(exp!="auto"):
            cam.ExposureTime.SetValue(int(exp))
        while e.is_set():
            if(synchronizer.Synchro(token)==1):
                try: 
                    if(not cam.IsGrabbing()):
                        cam.StartGrabbing()
                    result=cam.RetrieveResult(2000)
                    # Calling AttachGrabResultBuffer creates another reference to the
                    # grab result buffer. This prevents the buffer's reuse for grabbing.
                    #arr=result.Array
                    img.AttachGrabResultBuffer(result)  
                    if(img.IsGrabResultBufferAttached()):
                        filename = "saved_pypylon_"+hd["name"]+"_img_%d" % (hd["acquiredImages"]+1)
                        
                        img.Save(pylon.ImageFileFormat_Png, filename)
                        Salva.SaveMetadata(filename)
                        hd["timestamp"]=str(time.gmtime().tm_year)+"-"+str(time.gmtime().tm_mon)+"-"+str(time.gmtime().tm_mday)+"T"+str(time.gmtime().tm_hour)+":"+str(time.gmtime().tm_min)+":"+str(time.gmtime().tm_sec)
                        img.Release()  
                        cam.StopGrabbing()                  
                        print("New image "+hd["name"])                   
                        hd["acquiredImages"]=hd["acquiredImages"]+1
                        synchronizer.Update()
                        
                        
                except genicam.RuntimeException as exc:
                    hd["error"]=str(exc)
                    hd["status"]="GenError"                    
                    
                except genicam.LogicalErrorException as exc:
                    hd["error"]=str(exc)
                    hd["status"]="GenError"
                
                except Exception as exc:
                    hd["error"]=str(exc)
                    synchronizer.Update()        
        cam.Close()            
    except Exception as err:
        hd["error"]=str(err)
        hd["status"]="error"
        synchronizer.removefromQueue(token)
        e.clear()
    
    