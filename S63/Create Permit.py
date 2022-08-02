import blowfish
import binascii
from datetime import datetime, timedelta
from funcs import *

clearConsole()

def createPermit(HW_ID, Cells):

    CK1 = 'C1CB518E9C' #5 bytes in hexadecimal
    CK2 = '421571CC66' #5 bytes in hexadecimal
    Expiry_Days = 30
    PermitVersion = 1

    Expiry_Date = (datetime.today() + timedelta(days=Expiry_Days)).strftime('%Y%m%d')
    Permit = ":DATE" + datetime.today().strftime('%Y%m%d') + "\n:VERSION " + str(PermitVersion) + "\n:ENC\n"

    for cell in Cells:
        # a + b
        # Remmove extension and add expiry to cell permit
        permitLine = cell[:-4] + Expiry_Date

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
        #print(header + permitLine + "\n")
        Permit = Permit + permitLine + "\n"

    return Permit[:-1] #remove last new line

strID = '3132333438' #5 bytes in hexadecimal
strArrCell = ['NO4D0613.000','NO4D0614.000','NO4D0615.000']

print(createPermit(Cells = strArrCell, HW_ID = strID))