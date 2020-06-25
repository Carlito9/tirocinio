"""creazione del dictionary contenente info sulla camera"""
def createDic(dic,type,name,connection,timestamp,status="none",IP="N/A",acquiredImages=0,error="none"):
    if(IP=="N/A" and connection=="PoE"):
        status="stopped"
    elif connection=="PoE":
        status="running"
    dic["cameras"].append({

            "status": status,

            "type": type,

            "name": name,

            "IP": IP,

            "connection": connection,

            "timestamp": timestamp,

            "acquiredImages": acquiredImages,

            "error": error

        })
           
    return dic