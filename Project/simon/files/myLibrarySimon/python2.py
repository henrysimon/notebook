import time

vNew_Line_Linux = '\n'

def sString_Find(vText, *arrFind):
    vReturn = False
    for vFind in arrFind:
        if(vText.find(vFind) > 0):
            vReturn = True
            break    
    return vReturn

def sFile_Read(vPath):
    """Read file
    """
    f=open(vPath, "r")
    return(f.read())

def sFile_Write(vPath, vText):
    """write file
    """
    f = open(vPath, "w+")
    f.write(vText)
    return()

def sWait(iSeconds):
    time.sleep(iSeconds)
    return

def sHostname_Get():
    import socket
    return socket.gethostname()