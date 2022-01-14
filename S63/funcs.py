
import blowfish, sys, os

def clearConsole():
    import os
    clear = lambda: os.system('clear')
    clear()

def bytes_to_int(bytesIn):
    #try:
        bytesIn2 = bytearray(bytesIn)
        if int.from_bytes(bytesIn,"big") == 0: return 0
        l = len(bytesIn2) - 1
        b = bytesIn2[l]
        while bytesIn2[l] == 0:
            del bytesIn2[l]
            l = l-1
        byteObject = bytes(bytesIn2)
        return int.from_bytes(byteObject,"big")
    #except: return 0

def clearDir(path):
    import glob
    files = glob.glob(path)
    for f in files:
        os.remove(f)

def IntToTime(intVal):
    import time
    x = intVal 
    return time.strftime('%H:%M:%S', time.localtime(x))

def IntToDate(intVal):
    import datetime
    timestamp = datetime.datetime.fromtimestamp(intVal)
    return timestamp.strftime('%Y-%m-%d %H:%M:%S')

def WriteBinary(filename,binaryVal,append = False):
    #if os.path.exists(filename) or not append:
    #    os.remove(filename)
    file = open(filename, "wb")
    file.write(binaryVal)
    file.close()        

def pad(val):
    """This function pads a hex value to be 8 bytes in length"""
    val = val.lstrip('0x')
    a = int((16-len(val))/2)
    for i in range(a): val += hex(a).lstrip('0x').rjust(2,'0')
    return val

def depad(block):
    b = int(block[-2:])
    if b <= 16: block = block[:-b*2]
    return block

def decryptId(id, val, padVal = True, depadResult = True):
    try:
        if padVal: val = pad(val)
        cipher = blowfish.Cipher(bytes.fromhex(id)) 
        block = cipher.decrypt_block(bytes.fromhex(val)).hex()
        if depadResult: block = depad(block)
        return block
    except:
        return (-1)
        
def decryptCy(cipher, val, padVal = True, depadResult = True):
    try:
        if padVal: val = pad(val)
        block = cipher.decrypt_block(bytes.fromhex(val)).hex()
        if depadResult: block = depad(block)
        return block
    except:
        return (-1)

def hexToASCiiPair(val):
    hexv = ""
    val = val.lstrip('0x').upper()
    for i in val:
        hexv = hexv + str(hex(ord(str(i))).lstrip('0x'))
    #hexv = hexv + hexv [:2]
    return hexv

def printProgressBar(i,max,postText):
    n_bar =10 #size of progress bar
    j= i/max
    sys.stdout.write('\r')
    sys.stdout.write(f"[{'=' * int(n_bar * j):{n_bar}s}] {int(100 * j)}%  {postText}")
    sys.stdout.flush()