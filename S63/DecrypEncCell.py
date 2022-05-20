from funcs import *

import blowfish
import os
import sys

clearConsole()

# Manufacturer ID: (M_ID) = 10 (or 3130 hexadecimal)Manufacturer 
# Key: (M_KEY) = 10121 (or 3130313231 hexadecimal)Hardware 
# ID: (HW_ID) = 12345 (or 3132333435 hexadecimal)
# USERPERMIT = 66B5CBFDF7E4139D5B6086C23130

base_file_path = "/config/workspace/S63/"
CellPrtmit = 'GB1000042018123164B51D24FB77ADB364B51D24FB77ADB390432733F4F4D403,0,1,GB,Comment'
HW_ID = '3132333435' #5 bytes in hexadecimal hexToASCiiPair('12345') #
CK1 = GetCellKeyfromCellPermit(HW_ID,CellPrtmit)
cellFile = CellPrtmit[0:8]
enc_path = base_file_path + f"Test 4b/V01X01/ENC_ROOT/GB/GB100004/7/0/{cellFile}.000"

result = decryptENC(enc_path,CK1, base_file_path + "TempData/", True)
print('File Decryption Status:', result[0], '\nDecrypted File Location:', result[1])
#clearDir(base_file_path + "TempData/*")