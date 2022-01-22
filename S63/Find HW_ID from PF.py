
#https://iho.int/uploads/user/pubs/standards/s-63/S-63_2020_Ed1.2.1_EN_Draft_Clean.pdf

from funcs import *
import os, re

import time

t = time.process_time()
    
clearConsole()

#min = 0x12000
max = 0xFFFFFFFFFF
#max = 0x10000

def hexToASCiiPair(val,padv):
    hexv = ""
    val = val.lstrip('0x')
    for i in val:
        hexvt = str(hex(ord(str(i))).lstrip('0x'))
        hexv = hexv + hexvt
    hexv = pad(hexv,padv)
    return hexv

def ASCiiPairToHex(val, len = 5):
    import re
    import binascii
    try:
        # remove padding if last value less than 8
        l = findLen(val)
        b = int(val[-2:])
        if b <= l-2:
            val = val[:-b*2]
        i = ""
        l = findLen(val) # recalc on new val
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

def findM_ID(ECK1, start = 0x10000):
    print('-----------------------------------\nStart Scan ' + ECK1, 'Start:' + hex(start).lstrip('0x').upper())
    Write("S63/Data/DecryptPermit.txt", '-----------------------------------\nStart Scan ' + ECK1 + ' Start:' + hex(start).lstrip('0x').upper())
    printProgressBar(0, max, str(start) + '/' + str(max))
    for n in range(start, max):
        hexv = hex(n).lstrip('0x').upper()
        #hexv = hexv.zfill(5)
        hexv = hexv + hexv[:2]
        #h = hexToASCiiPair(hexv,4)
        #hb = bytes.fromhex(hexv)
        #hb = str.encode(hexv)
        ECK1b = bytes.fromhex(ECK1)
        #b = b'113333'
        #hexv = pad(hexv,5)
        #num = hexToASCiiPair(hexv)
        #hexv = hexv.zfill(4)
        #block = b'000000'
        #bfh = bytes.fromhex(num)
        #bfs = str.encode(hexv)
        #uh = bfs.decode("ascii")
        #cipher = blowfish.Cipher(str.encode(hexv))
        cipher = blowfish.Cipher(bytes.fromhex(hexv))
        #block = cipher.decrypt_block(bytearray.fromhex(h))
        #block = cipher.decrypt_block(ECK1b)
        block = b"".join(cipher.decrypt_ecb(ECK1b))
        #bh = block.hex()

        if block.hex()[-6:] == '030303':
            print('\nFound: HW_ID for ' + ':' + hexv[:len(hexv)-1] + ' CK:' + block.hex())
            Write("S63/Data/DecryptPermit.txt", 'Found: HW_ID for ' + hexv[:len(hexv)-1] + ' CK:' + block.hex())
            return n
        if n%1000 == 0: 
            tm = time.strftime('%d-%H:%M:%S', time.gmtime(time.process_time() - t))
            printProgressBar(n, max, hexv + '(' + hexv[:len(hexv)-1] + ')' + ' [' + str(n) + '/' + str(max) + '] ' + tm)

    Write("S63/Data/DecryptPermit.txt", 'NotFound:' + ECK1)
    print('\nHW_ID NotFound:' + ECK1)
    return 0

def decryptCK(CellPrtmit, start = 0x1):
    id = findM_ID(CellPrtmit[16:32],start)
    #findM_ID(CellPrtmit[32:48],id)

Write("S63/Data/DecryptPermit.txt", '', True)

#QNLZ
#M_KEY: 201351 31287 (3331323837) HW_ID: 28701 (3238373031)
#GB307702 20220331 4209D1C0F1FEA71D 4209D1C0F1FEA71D 08CE6364D8F84166
#decryptCK('GB307702202203314209D1C0F1FEA71D4209D1C0F1FEA71D08CE6364D8F84166,0,2,GB,',0x28701)

#Defender
#GB307702 20220331 523BD9B97FBB3A8A 523BD9B97FBB3A8A 8C1EAC8F89FD1451
decryptCK('GB30770220220331523BD9B97FBB3A8A523BD9B97FBB3A8A8C1EAC8F89FD1451,0,2,GB,',0x1000000000)

#2504843D47FFF77B
# cipher = blowfish.Cipher(str.encode('123481'))
# block = cipher.decrypt_block(bytes.fromhex('B16411FD09F96982'.lower()))
# print(block.hex(),'B16411FD09F96982'.lower(),'lower')

# block = cipher.decrypt_block(bytes.fromhex('B16411FD09F96982'.upper()))
# print(block.hex(),'B16411FD09F96982'.upper(),'upper')

# cipher = blowfish.Cipher(str.encode('123481'))
# block = cipher.encrypt_block(block)
# print(block.hex(),block.hex().upper())

# #NO4D0613 20000830 BEB9BFE3C7C6CE68 B16411FD09F96982 795C77B204F54D48 = 12348
# CellPrtmit = 'NO4D061320000830BEB9BFE3C7C6CE68B16411FD09F96982795C77B204F54D48' 
# id = findM_ID(CellPrtmit[16:32],0x12348)
# findM_ID(CellPrtmit[32:48],id)

#decryptCK('NO4D061320000830BEB9BFE3C7C6CE68B16411FD09F96982795C77B204F54D48',0x12348)

# #GB40162A 20181231 F81AC653B0AB63B0 F81AC653B0AB63B0 9DE31FB609E17492,0,1,GB,' = 12348
# CellPrtmit = 'GB40162A20181231F81AC653B0AB63B0F81AC653B0AB63B09DE31FB609E17492,0,1,GB,Comment'
# id = findM_ID(CellPrtmit[16:32],0x12345)
# findM_ID(CellPrtmit[32:48],id)

#decryptCK('GB40162A20181231F81AC653B0AB63B0F81AC653B0AB63B09DE31FB609E17492,0,1,GB,Comment',0x12345)

# #GB100004 20181231 64B51D24FB77ADB3 64B51D24FB77ADB3 90432733F4F4D403,0,1,GB,Comment = 12345
# CellPrtmit = 'GB1000042018123164B51D24FB77ADB364B51D24FB77ADB390432733F4F4D403,0,1,GB,Comment'
# id = findM_ID(CellPrtmit[16:32],0x12345)
# findM_ID(CellPrtmit[32:48],id)

#decryptCK('GB1000042018123164B51D24FB77ADB364B51D24FB77ADB390432733F4F4D403,0,1,GB,Comment',0x12345)

# #AU314145 20071231 CB091E0599028118 CB091E0599028118 1480B38500390FF3,0,4,0, = ?
# CellPrtmit = 'AU31414520071231CB091E0599028118CB091E05990281181480B38500390FF3,0,4,0,'         
# id = findM_ID(CellPrtmit[16:32])
# findM_ID(CellPrtmit[32:48],id)

#v1.1?
#decryptCK('AU31414520071231CB091E0599028118CB091E05990281181480B38500390FF3,0,4,0,',0x1)

#GB302045 20140731 2504843D47FFF77B 2504843D47FFF77B 723651FE5C68F9A3,0,3,GB,')
# CellPrtmit = 'GB302045201407312504843D47FFF77B2504843D47FFF77B723651FE5C68F9A3,0,3,GB,'        
# fid = findM_ID(CellPrtmit[16:32])
# findM_ID(CellPrtmit[32:48],id)

#GB800001 20140731 A83EECC01E6F886F A83EECC01E6F886F F9129E7913A8D062
#decryptCK('GB80000120140731A83EECC01E6F886FA83EECC01E6F886FF9129E7913A8D062,0,18,GB,',0x1) # Found: HW_ID for :31321 CK:80ca0b4b57030303
#decryptCK('GB302045201407312504843D47FFF77B2504843D47FFF77B723651FE5C68F9A3,0,3,GB,',0x1)
