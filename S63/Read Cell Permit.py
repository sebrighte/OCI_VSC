
from funcs import *
    
clearConsole()

min= 0x10000
max = 0xFFFFF
HW_ID = ''
lines = []

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

with open('S63/Data/QNLZ Permit.txt') as f:
    lines = f.readlines()

pos = 0x10000
for line in lines:
    if line[:1] == ':':
        print(f"MET_D: {line[1:-1]}")
        continue
    elif line[:1] == '#':
        HW_ID = line[1:]
        print(f"HW_ID: {line[1:-1]}")
        continue

    if HW_ID == '':
        HW_ID = getCellKey(line[16:32],f.name,pos)
        if HW_ID == 0: 
            print("No valid keys found")
            break

    CK1 = GetCellKeyfromCellPermit(HW_ID,line,True).upper()
    CK2 = GetCellKeyfromCellPermit(HW_ID,line,False).upper()

    print(f"Cell:{line[0:8]} Ed:{line[67:68]} CK1:{CK1} CK2:{CK2}")
