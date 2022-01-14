
import blowfish, zipfile
from funcs import *

clearConsole()

#CellPrtmit = 'NO4D061320000830BEB9BFE3C7C6CE68B16411FD09F96982795C77B204F54D48' 
#NO4D0613 20000830 BEB9BFE3C7C6CE68 B16411FD09F9698 2795C77B204F54D48
#CellPrtmit = 'GB40162A20181231F81AC653B0AB63B0F81AC653B0AB63B09DE31FB609E17492,0,1,GB,Comment'
#GB40162A 20181231 F81AC653B0AB63B0 F81AC653B0AB63B0 9DE31FB609E17492,0,1,GB,'
CellPrtmit = 'GB1000042018123164B51D24FB77ADB364B51D24FB77ADB390432733F4F4D403,0,1,GB,Comment'

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

#print("CK1, CK2:",CK1, CK2)

#enc_path = "S63/Test 6d/V01X01/ENC_ROOT/GB/GB40162A/9/0/GB40162A.000"
enc_path = "S63/Test 4b/V01X01/ENC_ROOT/GB/GB100004/7/0/GB100004.000"
# file = open("S63/Test 6d/V01X01/ENC_ROOT/GB/GB40162A/9/0/GB40162A.000", "rb")
# #file = open("S63/Test 6d/V01X01/ENC_ROOT/GB/GB40162A/9/1/GB40162A.001", "rb")
# #file = open("S63/Test 4b/V01X01/ENC_ROOT/GB/GB100004/7/0/GB100004.000", "rb")
# # #file = open("S63/Test 4b/V01X01/ENC_ROOT/GB/GB100004/7/1/GB100004.001", "rb") #'592cecd934'
# bytesRead = file.read()

# cipher = blowfish.Cipher(bytes.fromhex(CK1))
# dbr = b"".join(cipher.decrypt_ecb(bytesRead))

# clearDir('S63/TempData/*')

# WriteBinary("S63/TempData/ENCTest.zip", dbr)

# from zipfile import ZipFile
# with ZipFile("S63/TempData/ENCTest.zip", 'r') as zip:
#     zip.printdir()
#     zip.extractall("S63/TempData")

# os.remove("S63/TempData/ENCTest.zip")

def decryptENC(enc_path, cypher, dest_path):
    file = open(enc_path, "rb")
    #file = open("S63/Test 6d/V01X01/ENC_ROOT/GB/GB40162A/9/1/GB40162A.001", "rb")
    #file = open("S63/Test 4b/V01X01/ENC_ROOT/GB/GB100004/7/0/GB100004.000", "rb")
    # #file = open("S63/Test 4b/V01X01/ENC_ROOT/GB/GB100004/7/1/GB100004.001", "rb") #'592cecd934'
    bytesRead = file.read()

    cipher = blowfish.Cipher(bytes.fromhex(cypher))
    dbr = b"".join(cipher.decrypt_ecb(bytesRead))

    #clearDir(dest_path + '*')

    WriteBinary(dest_path + "tmp.zip", dbr)

    from zipfile import ZipFile
    with ZipFile(dest_path + "tmp.zip", 'r') as zip:
        zip.printdir()
        zip.extractall(dest_path)

    os.remove(dest_path + "tmp.zip")

decryptENC(enc_path,CK1,"S63/TempData/")


