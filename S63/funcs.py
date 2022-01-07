
import blowfish, sys

def pad(val):
    """
    This function greets to
    the person passed in as
    a parameter
    """
    val = val.lstrip('0x')
    a = int((16-len(val))/2)
    for i in range(a): val += hex(a).lstrip('0x').rjust(2,'0')
    return val

def depad(block):
    b = int(block[-2:])
    if b <= 16: block = block[:-b*2]
    return block

#Stuff
def decryptId(id, val, padVal = True, depadResult = True):
    try:
        if padVal: val = pad(val)
        cipher = blowfish.Cipher(bytes.fromhex(id)) 
        block = cipher.decrypt_block(bytes.fromhex(val)).hex()
        if depadResult: block = depad(block)
        return block
    except:
        return (-1)

#Stuff
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