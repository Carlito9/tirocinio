from PIL import Image

metadata={}
def Save(filename,data):
    SaveMetadata(filename)
    Image.fromarray(data, 'RGB').save(filename+".png",'PNG')

def Savebw(filename,data):
    SaveMetadata(filename)
    Image.fromarray(data).save(filename+".png",'PNG')

def SaveMetadata(filename):
    f=open(filename+".txt",'w')
    f.write(str(metadata))

def SetMetadata(meta,axis):
    global metadata
    metadata[axis]=meta
    
    