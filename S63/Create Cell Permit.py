import blowfish
import binascii
from funcs import *

clearConsole()

HW_ID = '3132333438' #5 bytes in hexadecimal
CK1 = 'C1CB518E9C' #5 bytes in hexadecimal
CK2 = '421571CC66' #5 bytes in hexadecimal
Cell_Name = 'NO4D0613.000' #Valid S-57 cell name including file extension
Expiry_Date = '20000830' #Format YYYYMMDD

# a + b
# Remmove extension and add expiry to cell permit
permitLine = Cell_Name[:-4] + Expiry_Date

# c
# Add first byte of hardware id to the end
HW_ID6 = HW_ID + HW_ID[:2]

# d + e + f
# Encrypt cell key and add to Cell permit
cipher = blowfish.Cipher(bytes.fromhex(HW_ID6)) 
permitLine += cipher.encrypt_block(bytes.fromhex(pad(CK1))).hex().upper()

# g + h + i
# Encrypt cell key and add to Cell permit
permitLine += cipher.encrypt_block(bytes.fromhex(pad(CK2))).hex().upper()

# j
# Get CRC for the Cell Permit
CRC = hex(binascii.crc32(permitLine.encode('utf8')))

# k + l
# Get Encrypted CRC and add to Cell Permit
permitLine += cipher.encrypt_block(bytes.fromhex(pad(CRC))).hex().upper()

# Cell Permit
#print(permitLine)
# Test permit
# Cell    Expiry  Cell 1 key      Cell 2 key      CRC
# NO4D061320000830BEB9BFE3C7C6CE68B16411FD09F96982795C77B204F54D48
print("Valid Cell permit created?", permitLine == 'NO4D061320000830BEB9BFE3C7C6CE68B16411FD09F96982795C77B204F54D48', permitLine)
