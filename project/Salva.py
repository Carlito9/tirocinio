import PIL.PngImagePlugin
from PIL import Image
import cv2

metadata={}
def Salva(filename,data):
    """meta=PngInfo()
    meta.add_text("Xposition", str(pos[0]))
    meta.add_text("Yposition", str(pos[1]))
    meta.add_text("Zposition", str(pos[2]))"""
    SaveMetadata(filename)
    #Image.fromarray(data).save(filename,'PNG',pnginfo=meta)
    Image.fromarray(data, 'RGB').save(filename+".png",'PNG')

def Salvabn(filename,data):
    """meta=PngInfo()
    meta.add_text("Xposition", str(pos[0]))
    meta.add_text("Yposition", str(pos[1]))
    meta.add_text("Zposition", str(pos[2]))"""
    SaveMetadata(filename)
    Image.fromarray(data, 'I;16').save(filename+".png",'PNG')

def SaveMetadata(filename):
    f=open(filename+".txt",'w')
    f.write(str(metadata))

def SetMetadata(meta,axis):
    global metadata
    metadata[axis]=meta
    
    