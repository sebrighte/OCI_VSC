
from funcs import *
    
clearConsole()

min= 0x10000
max = 0xFFFFF

def printProgressBar(i,max,postText):
    n_bar =10 #size of progress bar
    j= i/max
    sys.stdout.write('\r')
    sys.stdout.write(f"[{'=' * int(n_bar * j):{n_bar}s}] {int(100 * j)}%  {postText}")
    sys.stdout.flush()

def GetCellKeyfromCellPermit(HW_ID,PermitLine,ECK1 = True):
    ECK = PermitLine[16:32]
    if not ECK1: ECK = PermitLine[32:48]
    cipher = blowfish.Cipher(bytearray.fromhex(HW_ID + HW_ID[0:2]))
    #return depad(b"".join(cipher.decrypt_ecb(bytes.fromhex(ECK))).hex())
    return depad(cipher.decrypt_block(bytes.fromhex(ECK)).hex())

#print(GetCellKeyfromCellPermit('0e51052ec2','GB3077022022033153BD6E442592FB8F53BD6E442592FB8F24B304172E423536',False), 'RFA FORT VICTORIA')
#print(GetCellKeyfromCellPermit('21c21e0f88','GB30770220220331523BD9B97FBB3A8A523BD9B97FBB3A8A8C1EAC8F89FD1451',True), 'HMS DEFENDER')
#print(GetCellKeyfromCellPermit('5ff5ff23d3','GB307702202203313DF8286B98B4B2953DF8286B98B4B295486472656D0B0C11',True), 'RFA TIDESPRING')

def getCellKey(eck, text = 'Nothing...', pmin = 0x10000):
    min = pmin
    print('-----------------------------------\nStart Scan ' + eck + ' (' + text + ')')
    printProgressBar(0, max, '')
    #Write("S63/OutputValues.txt",'-----------------------------------\nStart Scan ' + str(eck) + ' (' + text + ')')
    for n in range(min, max):

        HW_ID = hex(n).lstrip('0x').upper()
        HW_ID6b = (HW_ID + HW_ID[:1]).encode()
        #HW_ID6b = HW_ID.encode()
        eckb = bytes.fromhex(eck)

        cipher = blowfish.Cipher(HW_ID6b)
        val = b"".join(cipher.decrypt_ecb(eckb)).hex()

        if val[-6:] == '030303':
            print('\nHW_ID:', HW_ID6b.decode(), 'CK1:', depad(val))
            #Write("S63/OutputValues.txt",'HW_ID:' + str(HW_ID6b.decode()) + ' HW_ID:' + str(depad(val)))
            return HW_ID6b.decode()
        if n%1000 == 0: 
            #printProgressBar(n, max, str(n) + '(' + hex(n).lstrip('0x').upper() + '-' +  num + ')/' + str(max))
            printProgressBar(n, max, HW_ID6b.decode() + '                                 ')

    printProgressBar(max, max, 'Complete                                                         ')
    if n == max: 
        #Write("S63/OutputValues.txt","No valid keys found")
        #print("No valid keys found")
        return 0
    print('')

# HW_ID 3132333438 (12348) 5 bytes in hexadecimal
# CK1 C1CB518E9C 5 bytes in hexadecimal
# CK2 421571CC66 5 bytes in hexadecimal
# Cell Name NO4D0613.000 Valid S-57 cell name including file extension
# Expiry Date 20000830 Format YYYYMMDD
#NO4D0613 20000830 BEB9BFE3C7C6CE68 B16411FD09F9698 2795C77B204F54D48
CellPrtmit = 'NO4D061320000830BEB9BFE3C7C6CE68B16411FD09F96982795C77B204F54D48' 

#CellPrtmit = 'GB40162A20181231F81AC653B0AB63B0F81AC653B0AB63B09DE31FB609E17492,0,1,GB,Comment'
#GB40162A 20181231 F81AC653B0AB63B0 F81AC653B0AB63B0 9DE31FB609E17492,0,1,GB,'

#CellPrtmit = 'GB1000042018123164B51D24FB77ADB364B51D24FB77ADB390432733F4F4D403,0,1,GB,Comment'
#ID = '12345'

#QNLZ
#M_KEY: 201351 31287 (3331323837) HW_ID: 28701 (3238373031)
#GB307702 20220331 4209D1C0F1FEA71D 4209D1C0F1FEA71D 08CE6364D8F84166
#CellPrtmit = 'GB307702202203314209D1C0F1FEA71D4209D1C0F1FEA71D08CE6364D8F84166,0,2,GB,'
#CellPrtmit = 'NO4D061320000830BEB9BFE3C7C6CE68B16411FD09F96982795C77B204F54D48' 
#ID = '28701'
HW_ID = ''
#CK1 == E8A63CD6F2??

#DFDR
#GB307702 20220331 523BD9B97FBB3A8A 523BD9B97FBB3A8A8 C1EAC8F89FD1451,0,2,GB,
#M_KEY: 
#CellPrtmit = 'GB30770220220331523BD9B97FBB3A8A523BD9B97FBB3A8A8C1EAC8F89FD1451,0,2,GB,'
#ID = ''
#CK1 == E8A63CD6F2??

# Manufacturer ID: (M_ID) = 10 (or 3130 hexadecimal)Manufacturer 
# Key: (M_KEY) = 10121 (or 3130313231 hexadecimal)Hardware 
# ID: (HW_ID) = 12345 (or 3132333435 hexadecimal)
# USERPERMIT = 66B5CBFDF7E4139D5B6086C23130

# HW_ID = hexToASCiiPair(ID) #'3132333435' #5 bytes in hexadecimal
x =  bytes.fromhex('21c21e0f88')

lines = []
with open('S63/Data/DFDR Permit.txt') as f:
    lines = f.readlines()

user = ''
pos = 0x10000
for line in lines:
    chr1 = line[:1]
    if chr1 == ':':continue
    if chr1 == '#':
        pos = int(line[1:], base=16)
        continue
    CellPrtmit = line
    #CellPrtmit = 'GB30770220220331523BD9B97FBB3A8A523BD9B97FBB3A8A8C1EAC8F89FD1451,0,2,GB,'
    Cell_Name = CellPrtmit[0:8]
    Expiry_Date = CellPrtmit[8:16]
    ECK1 = CellPrtmit[16:32]
    ECK2 = CellPrtmit[32:48]
    CRC = CellPrtmit[48:64]
    ServiceLevelIndicator = CellPrtmit[65:66]
    EditionNumber = CellPrtmit[67:68]
    DataServerID = CellPrtmit[69:71]
    Comment = CellPrtmit[72:]

    if HW_ID == '':
        HW_ID = getCellKey(ECK1,f.name,pos)
        if HW_ID == 0: 
            print("No valid keys found")
            break

    cipher = blowfish.Cipher(HW_ID.encode())
    CK1 = decryptCy(cipher, ECK1).upper()
    CK2 = decryptCy(cipher, ECK2).upper()

    print("CK1, CK2:",CK1, CK2)
