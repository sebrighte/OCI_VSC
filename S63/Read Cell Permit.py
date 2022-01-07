
import blowfish
from datetime import datetime
from funcs import *

#CellPrtmit = 'NO4D061320000830BEB9BFE3C7C6CE68B16411FD09F96982795C77B204F54D48' 
#NO4D0613 20000830 BEB9BFE3C7C6CE68 B16411FD09F9698 2795C77B204F54D48
CellPrtmit = 'GB40162A20181231F81AC653B0AB63B0F81AC653B0AB63B09DE31FB609E17492,0,1,GB,Comment'
#GB40162A 20181231 F81AC653B0AB63B0 F81AC653B0AB63B0 9DE31FB609E17492,0,1,GB,'

CellPrtmit = 'GB1000042018123164B51D24FB77ADB364B51D24FB77ADB390432733F4F4D403,0,1,GB,Comment'
#"\\SynologyNAS\docker\vsc\config\workspace\S63\Test 4b\V01X01\ENC_ROOT\GB\GB100004\7\0\GB100004.000"

# Manufacturer ID: (M_ID) = 10 (or 3130 hexadecimal)Manufacturer 
# Key: (M_KEY) = 10121 (or 3130313231 hexadecimal)Hardware 
# ID: (HW_ID) = 12345 (or 3132333435 hexadecimal)
# USERPERMIT = 66B5CBFDF7E4139D5B6086C23130

HW_ID = hexToASCiiPair('12345') #'3132333435' #5 bytes in hexadecimal
HW_ID6 = HW_ID + HW_ID[:2]

Cell_Name = CellPrtmit[0:8]
Expiry_Date = CellPrtmit[8:16]
ECK1 = CellPrtmit[16:32]
ECK2 = CellPrtmit[32:48]
CRC = CellPrtmit[48:64]
ServiceLevelIndicator = CellPrtmit[65:66]
EditionNumber = CellPrtmit[67:68]
DataServerID = CellPrtmit[69:71]
Comment = CellPrtmit[72:]

cipher = blowfish.Cipher(bytes.fromhex(HW_ID6))
CK1 = decryptCy(cipher, ECK1)
CK2 = decryptCy(cipher, ECK2)

print("CK1, CK2:",CK1, CK2)

#file = open("S63/Test 6d/V01X01/ENC_ROOT/GB/GB40162A/9/0/GB40162A.000", "rb")
#file = open("S63/Test 6d/V01X01/ENC_ROOT/GB/GB40162A/9/1/GB40162A.001", "rb")
file = open("S63/Test 4b/V01X01/ENC_ROOT/GB/GB100004/7/0/GB100004.000", "rb")
#file = open("S63/Test 4b/V01X01/ENC_ROOT/GB/GB100004/7/1/GB100004.001", "rb") #'592cecd934'
bytesRead = file.read(8)

#cipher = blowfish.Cipher(bytes.fromhex(CK2))
#ENC = cipher.decrypt_block(bytesRead)[:2]

now = datetime.now()

#cipher = blowfish.Cipher(bytes.fromhex('1000000000'))
# for n in range(0x1000000000,0xFFFFFFFFFF):
#     n2 = hex(n).lstrip('0x')
#     cipher = blowfish.Cipher(bytes.fromhex(n2))
#     if n%1000 == 0: 
#         printProgressBar(n, 0xFFFFFFFFFF, str(n) + ' ' + hex(n) + ' ' + str(datetime.now() - now))

#for n in range(0x592cecd134,0xFFFFFFFFFF):
for n in range(0x1000000000,0xFFFFFFFFFF):
    n2 = hex(n).lstrip('0x')
    cipher = blowfish.Cipher(bytes.fromhex(n2))
    block = cipher.decrypt_block(bytesRead)
    ENC = block[:4]
    #h = block[:4].hex()
    #p= chr(ENC[0]) + chr(ENC[1])
    if ENC == b'PK\x03\x04': 
        print(' ')
        h = block.hex()
        # 504b0304
        print('Found:', n2, 'Expected:' , CK1, 'Bytes:',block, 'Hex:', block.hex())
        #break
    if n%1000 == 0: 
        printProgressBar(n, 0xFFFFFFFFFF, str(n) + ' ' + hex(n) + ' ' + str(datetime.now() - now))