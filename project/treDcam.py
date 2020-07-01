import threading   
import pyrealsense2 as rs
import numpy as np
import Save
import time
import synchronizer


def Photo(e,tred,token,flag):
    try:        
        pipe = rs.pipeline()
        color=rs.colorizer()
        ctx=rs.context()
        dev=ctx.query_devices() 
        i=0
        while True:
            if dev[i].get_info(rs.camera_info.ip_address)==tred["IP"]:
                break
            i=i+1
            if i==len(dev):
                raise Exception('This camera is not avaiable')
        cfg=rs.config()
        cfg.enable_stream(rs.stream.depth, 640, 480,rs.format.z16,30)
        cfg.enable_device(dev[i].get_info(rs.camera_info.serial_number))
        print("3D cam started.")
        #Getting the depth sensor's depth scale (see rs-align example for explanation)
        while e.is_set():
            if(synchronizer.Synchro(token)==1):
                try:
                    pipe.start(cfg)
                    # This call waits until a new coherent set of frames is available on a device
                    # Calls to get_frame_data(...) and get_frame_timestamp(...) on a device will return stable values until wait_for_frames(...) is called
                    for j in range (0,15):    
                        frames = pipe.wait_for_frames()
                    depth_frame = frames.get_depth_frame()
                    filename="3D_%d" % (int(time.time()))
                    if(flag==1):
                        depth_col=color.colorize(depth_frame)
                        depth_data = np.asanyarray(depth_col.get_data(),dtype=np.uint16)
                        Save.Save(filename, depth_data)
                    else:
                        depth_data = np.asanyarray(depth_frame.get_data(),dtype=np.uint16)
                        Save.Savebw(filename, depth_data) 
                    print("immagine 3d")
                    tred["acquiredImages"]=tred["acquiredImages"]+1
                    tred["timestamp"]=str(time.gmtime().tm_year)+"-"+str(time.gmtime().tm_mon)+"-"+str(time.gmtime().tm_mday)+"T"+str(time.gmtime().tm_hour)+":"+str(time.gmtime().tm_min)+":"+str(time.gmtime().tm_sec)
                    pipe.stop()
                    synchronizer.Update()
                except Exception as exc:
                    tred["error"]=str(exc) 
                    synchronizer.Update()                
                    break
    except Exception as err:
        tred["error"]=str(err)
        tred["status"]="error"
        synchronizer.removefromQueue(token)
        e.clear()
