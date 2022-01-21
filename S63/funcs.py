
import blowfish, sys, os

def clearConsole():
    """This function clears all text from the console"""
    import os
    clear = lambda: os.system('clear')
    clear()

def GetCellKeyfromCellPermit(HW_ID,PermitLine,ECK1 = True):
    ECK = PermitLine[16:32]
    if not ECK1: ECK = PermitLine[32:48]
    cipher = blowfish.Cipher(bytearray.fromhex(HW_ID + HW_ID[0:2]))
    #return depad(b"".join(cipher.decrypt_ecb(bytes.fromhex(ECK))).hex())
    return depad(cipher.decrypt_block(bytes.fromhex(ECK)).hex())

def decryptENC(enc_path, cypher, dest_path, delAllFiles = False):
    "Returns True if decrypted file is created"

    try:
        file = open(enc_path, "rb")
        bytesRead = file.read()

        cipher = blowfish.Cipher(bytes.fromhex(cypher))
        dbr = b"".join(cipher.decrypt_ecb(bytesRead))

        if delAllFiles: clearDir(dest_path + '*')

        WriteBinary(dest_path + "tmp.zip", dbr)

        from zipfile import ZipFile
        with ZipFile(dest_path + "tmp.zip", 'r') as zip:
            #zip.printdir()
            zip.extractall(dest_path)

        os.remove(dest_path + "tmp.zip")
        return os.path.exists(dest_path + os.path.basename(enc_path))
    except: return False

def encrypt(id,val):
    if len(id) == 5: id = hexToASCiiPair(id)
    if len(val) == 5: val = hexToASCiiPair(val)
    a = int((16-len(val))/2)
    for i in range(a): val += hex(a).lstrip('0x').rjust(2,'0')
    cipher = blowfish.Cipher(bytes.fromhex(str(id)))
    block = bytes.fromhex(str(val))
    retBlock = (cipher.encrypt_block(block).hex()).upper()
    return (retBlock, id, block)

def decrypt(id,val):
    try:
        if len(id) == 5: id = hexToASCiiPair(id)
        if len(val) == 5: val = hexToASCiiPair(val)
        b = bytes.fromhex(str(id))
        cipher = blowfish.Cipher(bytes.fromhex(str(id)))
        block = cipher.decrypt_block(bytes.fromhex(val))
        block = block.hex()
        # remove padding if last value less than 8
        b = int(block[-2:])
        if b <= 8:
            block2 = block[:-b*2]
        if block2 == '': return (0, block)
        return (block2, block)
    except:
        return (0, block)
        
def ASCiiPairToHex(val, len = 5):
    try:
        # remove padding if last value less than 8
        l = findLen(val)
        b = int(val[-2:])
        if b <= l-2:
            val = val[:-b*2]
        i = ""
        l = findLen(val) # recalc on new val
        #if l < 10: return hex(int(0))
        for n in range(0, l, 2):
            h = val[n:n+2]
            x = re.search("[3][0-9]|[46][1-6]", h)  
            if not x: 
                #print(h)
                return hex(int(0))
            b = binascii.unhexlify(h)
            c = str(b, 'utf-8')
            i = i + c
        return hex(int(i, 16)).lstrip('0x').upper()
    except:
        return hex(int(0))

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

def Write(filename,strVal,cls=False):
    if os.path.exists(filename) and cls==True:
        os.remove(filename)
    with open(filename, "a") as file_object:
        file_object.write(strVal + '\n')

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

def findLen(str):
    counter = 0    
    for i in str:
        counter += 1
    return counter      

def pad(val,pad = 8):
    "This function pads a hex value to be 8 bytes in length"
    val = val.lstrip('0x')
    a = int(( (pad*2) -len(val))/2)
    for i in range(a): val += hex(a).lstrip('0x').rjust(2,'0')
    return val

def depad(block):
    "This function removes padding"
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
    val = val.lstrip('0x')#.upper()
    for i in val:
        s = str(hex(ord(str(i))).lstrip('0x'))
        hexv = hexv + s
    #hexv = hexv + hexv [:2]
    return hexv

def printProgressBar(i,max,postText):
    n_bar =10 #size of progress bar
    j= i/max
    sys.stdout.write('\r')
    sys.stdout.write(f"[{'=' * int(n_bar * j):{n_bar}s}] {int(100 * j)}%  {postText}")
    sys.stdout.flush()