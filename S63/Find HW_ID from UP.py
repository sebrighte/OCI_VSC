
import binascii
import blowfish
import sys
import re
import os

from funcs import *

min = 0x10000
max = 0xFFFFF  

filename = "S63/OutputValues.txt"
if os.path.exists(filename):
    os.remove(filename)

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

def hexToASCiiPair(val):
    hexv = ""
    val = val.lstrip('0x')#.upper()
    for i in val:
        s = str(hex(ord(str(i))).lstrip('0x'))
        hexv = hexv + s
    #hexv = hexv + hexv [:2]
    return hexv

def psFromFile(filename):
    lines = []
    with open('S63/Data/User Permits2.txt') as f:
        lines = f.readlines()

    user = ''
    for line in lines:
        if line == '\n': continue
        if line[:1] == '#':
            user = line  
            continue
        findM_ID(line,user[1:-1],0x1000)

def printProgressBar(i,max,postText):
    n_bar =10 #size of progress bar
    j= i/max
    sys.stdout.write('\r')
    sys.stdout.write(f"[{'=' * int(n_bar * j):{n_bar}s}] {int(100 * j)}%  {postText}")
    sys.stdout.flush()

def findM_ID(encryID, text, pmin = 0x1000):
    min = pmin
    encryID = encryID[0:16]
    print('-----------------------------------\nStart Scan ' + encryID + ' (' + text + ')')
    printProgressBar(0, max, '0/' + str(max))
    Write("S63/OutputValues.txt",'-----------------------------------\nStart Scan ' + encryID + ' (' + text + ')')
    for n in range(min, max):

        hexvb = hex(n).lstrip('0x').upper().encode()
        encryIDb = bytes.fromhex(encryID)

        cipher = blowfish.Cipher(hexvb)
        val = b"".join(cipher.decrypt_ecb(encryIDb)).hex()

        if val[-6:] == '030303':
            print('\nM_KEY:', hexvb.decode(), 'HW_ID:', depad(val))
            Write("S63/OutputValues.txt",'M_KEY:' + str(hexvb.decode()) + ' HW_ID:' + str(depad(val)))
            break
        if n%1000 == 0: 
            #printProgressBar(n, max, str(n) + '(' + hex(n).lstrip('0x').upper() + '-' +  num + ')/' + str(max))
            printProgressBar(n, max, hexvb.decode() + '                                 ')

    printProgressBar(max, max, 'Complete                                                         ')
    if n == max: 
        Write("S63/OutputValues.txt","No valid keys found")
        print("No valid keys found")
    print('')

def CreateUserPermit(M_KEY,HW_ID,M_ID):
    ehw_id = encrypt(M_KEY,HW_ID)[0]
    hex_string = ehw_id
    hex_value = hex(binascii.crc32(hex_string.encode('utf8')))
    return (ehw_id + hex_value.lstrip('0x') + M_ID).upper()
    
def unitTest(): #unit tests - encrypt 
    if encrypt('10121', '12345')[0] != '66B5CBFDF7E4139D': print("Test 1 Failed", encrypt('10121', '12345'))
    if encrypt('3130313231', '3132333435')[0] != '66B5CBFDF7E4139D': print("Test 1 Failed", encrypt('3130313231', '3132333435')[0]) 

    if encrypt('123AB', 'FE321')[0] != 'A89D5B77F731DF86': print("Test 2 Failed", encrypt('123AB', 'FE321'))
    if encrypt('3132334142', '4645333231')[0] != 'A89D5B77F731DF86': print("Test 3b Failed", encrypt('3132334142', '4645333231'))

    if encrypt('ABCDE', 'EDCBA')[0] != 'C0AD0FF2ACE832EB': print("Test 3 Failed", encrypt('abcde', 'EDCBA'))
    if encrypt('4142434445', '4544434241')[0] != 'C0AD0FF2ACE832EB': print("Test 3d Failed", encrypt('4142434445', '4544434241'))

    if encrypt('98765', '12348')[0] != '73871727080876A0': print("Test 3b Failed", encrypt('98765', '12348'))
    if encrypt('3938373635', '3132333438')[0] != '73871727080876A0': print("Test 3e Failed", encrypt('3938373635', '3132333438'))

    #unit tests - decrypt 
    if decrypt('3130313231', '66B5CBFDF7E4139D')[0] != '3132333435': print("Test 4 Failed") 
    if decrypt('10121', '66B5CBFDF7E4139D')[0] != '3132333435': print("Test 5 Failed",decrypt('10121', '66B5CBFDF7E4139D'))
    if decrypt('123AB', 'A89D5B77F731DF86')[0] != '4645333231': print("Test 6 Failed",decrypt('123AB', 'A89D5B77F731DF86'))
    if decrypt('21c21e0f8821', '523BD9B97FBB3A8A')[1] != 'e8a63cd6f2030303': print("Test 5 Failed",decrypt('21c21e0f8821', '523BD9B97FBB3A8A'))

    #unit test - hexToASCiiPair
    # if hexToASCiiPair('123AB') != '3132334142': print("Test 7 Failed",hexToASCiiPair('123AB'))  
    # if hexToASCiiPair('0x123AB') != '3132334142': print("Test 8 Failed",hexToASCiiPair('0x123AB')) 
    # if hexToASCiiPair('10121') != '3130313231': print("Test 9 Failed",hexToASCiiPair('10121')) 
    # if hexToASCiiPair('0x10121') != '3130313231': print("Test 9a Failed",hexToASCiiPair('0x10121')) 
    # if hexToASCiiPair('0x254de') != '3235346465': print("Test 9b Failed",hexToASCiiPair('0x254de')) 
    # if hexToASCiiPair('0x254DE') != '3235344445': print("Test 9c Failed",hexToASCiiPair('3235344445')) 
    # if hexToASCiiPair('123') != '313233': print("Test 10 Failed",hexToASCiiPair('0x123')) 

    #unit test - ASCiiPairToHex
    # if ASCiiPairToHex('3130313231') != '10121': print("Test 11 Failed",ASCiiPairToHex('3130313231')) 
    # if ASCiiPairToHex('3130310202') != '101': print("Test 12 Failed",ASCiiPairToHex('3130310202')) 
    # if ASCiiPairToHex('4646464646') != 'FFFFF': print("Test 13 Failed",ASCiiPairToHex('4646464646')) 
    # if ASCiiPairToHex('3104040404') != '1': print("Test 14 Failed",ASCiiPairToHex('3104040404')) 

    #unit test - CreateUserPermit
    if str(CreateUserPermit('10121','12345','3130')) != '66B5CBFDF7E4139D5B6086C23130': print("Test Failed" , CreateUserPermit('10121','12345','3130'))
    if str(CreateUserPermit('3130313231','3132333435','3130')) != '66B5CBFDF7E4139D5B6086C23130': print("Test Failed" , CreateUserPermit('3130313231','3132333435','3130'))

    print("Tests Complete")

def unitUpTest():
    # From S=63 docs
    #M_KEY: 65825 10121 (3130313231) HW_ID: 12345 (3132333435)
    findM_ID('66B5CBFDF7E4139D','From S63 docs',0x10121)

    # From S=63 docs
    #M_KEY: 624485 98765 (3938373635) HW_ID: 12348 (3132333438)
    findM_ID('73871727080876A07E450C043031','From S63 docs',0x98765)

    #M_KEY: 703710 0xabcde (373033373130) HW_ID: EDCBA (4544434241)
    findM_ID('C0AD0FF2ACE832EB','Derived',0xABCDE)

    #SAM ChartPilot 1100 Version 6.14 Build 69
    #E7A63F22C8B0B9CD CAF68D32 3134
    #M_KEY: 84953 HW_ID: ae31411501
    findM_ID('E7A63F22C8B0B9CDCAF68D323134','SAM ChartPilot 1100',0x84953)

    #encry_HW_ID = '057DA7ADC227C0D0'
    #M_KEY: 45109 HW_ID: b953ceb5ee
    findM_ID('057DA7ADC227C0D0','Derived',0x45109)

    #encry_HW_ID = '7D88AC20B915A587'
    #M_KEY: 83011 HW_ID: 0130584096
    findM_ID('7D88AC20B915A587','Derived',0x83011)

    # Test from doc (might not be real...)
    # M_KEY: 0x98765 (363234343835) HW_ID: 74568 (3132333438)
    findM_ID('73871727080876A0','Test from doc (might not be real...)',0x98765)# A79AB

    #
    findM_ID('51ABA63B31D3BD5B','Derived',0x24317)

    #
    findM_ID('EB3C7E109D3A6064','Derived',0x16410)

    #HMS QUEEN ELIZABETH
    #D6CE30E1B2E876229DEA86BC3234
    #M_KEY: 201351 31287 (3331323837) HW_ID: 28701 (3238373031)
    findM_ID('D6CE30E1B2E87622','QNLZ',0x31287)

    #HMS DEFENDER
    #M_KEY: 21c21e0f88
    #981A73CCF40AFFB7B432B3413837
    findM_ID('981A73CCF40AFFB7','HMS DEFENDER',0x10273)

    #HMS TAMAR
    #M_KEY: b5e38e80ac
    #7B5B008E5F7A7A8816C2B3B63837
    findM_ID('7B5B008E5F7A7A88','HMS TAMAR',0x10273)

clearConsole()

unitTest()
unitUpTest()

#findM_ID('981A73CCF40AFFB7','HMS DEFENDER',0x10273)



