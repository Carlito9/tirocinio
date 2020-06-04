from ximea import xiapi
import threading
import Salva
import pyexiv2
import time
import synchronizer

#Check that /sys/module/usbcore/parameters/usbfs_memory_mb is set to 0

def Photo(e,usb,token,exp):
    try:
        cam = xiapi.Camera()
        #start communication    
        cam.open_device()
        img = xiapi.Image()
        #setting
        if(exp=="auto"):
            cam.enable_aeag() 
        else: 
            cam.set_exposure(int(exp)) 
        #start data acquisition
        print('Starting data acquisition...\n')
        cam.start_acquisition()
        cam.set_imgdataformat('XI_RGB24')
        
        while e.is_set():
            if(synchronizer.Synchro(token)==1):
                try:
                    cam.get_image(img)
                    data_num = img.get_image_data_numpy(invert_rgb_order=True)
                    
                    filename='USB_%d' % (int(time.time()))                  
                    Salva.Salva(filename,data_num)
                    print("New usb image...")
                    usb["timestamp"]=str(time.gmtime().tm_year)+"-"+str(time.gmtime().tm_mon)+"-"+str(time.gmtime().tm_mday)+"T"+str(time.gmtime().tm_hour)+":"+str(time.gmtime().tm_min)+":"+str(time.gmtime().tm_sec)
                    synchronizer.Update()
                    usb["acquiredImages"]=usb["acquiredImages"]+1
                    print("token: "+str(token))
                except Exception as exc:
                    usb["error"]=str(exc)
                    synchronizer.Update()
                    #stop data acquisition
        print('Usb Cam: Stopping acquisition...')
        cam.stop_acquisition()            
    except Exception as err:
        usb["error"]=str(err)
        usb["status"]="error"
        synchronizer.removefromQueue(token)
        e.clear()
    

    #stop communication

    cam.close_device()
