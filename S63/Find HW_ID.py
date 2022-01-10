
import binascii
import blowfish
import sys
import re
import os

min = 0x10000
max = 0xFFFFF  

filename = "S63/OutputValues"
if os.path.exists(filename):
    os.remove(filename)

def Write(strVal):
    with open(filename, "a") as file_object:
        file_object.write(strVal + '\n')

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
        cipher = blowfish.Cipher(bytes.fromhex(str(id)))
        block = cipher.decrypt_block(bytes.fromhex(val)).hex()
        # remove padding if last value less than 8
        b = int(block[-2:])
        if b <= 8:
            block2 = block[:-b*2]
        if block2 == '': return (0, block)
        return (block2, block)
    except:
        return (0, block)

def findLen(str):
    counter = 0    
    for i in str:
        counter += 1
    return counter

def printProgressBar(i,max,postText):
    n_bar =10 #size of progress bar
    j= i/max
    sys.stdout.write('\r')
    sys.stdout.write(f"[{'=' * int(n_bar * j):{n_bar}s}] {int(100 * j)}%  {postText}")
    sys.stdout.flush()

def hexToASCiiPair(val):
    hexv = ""
    len = 5
    val = val.lstrip('0x').upper()
    for i in val:
        hexv = hexv + str(hex(ord(str(i))).lstrip('0x'))
    l = findLen(hexv)
    l2 = ((2*len) - l)/2
    k = int((10 - l)/2)
    for n in range(0, k):
        ch = str(k)
        hexv += '0' + ch
    return hexv

def findLen(str):
    counter = 0    
    for i in str:
        counter += 1
    return counter

def ASCiiPairToHex(val, len = 5):
    try:
        # remove padding if last value less than 8
        l = findLen(val)
        b = int(val[-2:])
        if b <= l-2:
            val = val[:-b*2]
        i = ""
        l = findLen(val) # recalc on new val
        #if l < 10: return hex(int(0))
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

def findM_ID(encryID, text):
    print('-----------------------------------\nStart Scan ' + encryID + ' (' + text + ')')
    Write(encryID)
    printProgressBar(0, max, '0/' + str(max))
    encryID = encryID[0:16]
    for n in range(min, max):
        hexv = hex(n).lstrip('0x').upper()
        num = hexToASCiiPair(hexv)
        val = decrypt(num,encryID)[0]
        if len(str(val)) == 10: 
            a = ASCiiPairToHex(val)
            a = int(a, 16)
            if a <= 0xFFFFF and a > 0:
                if findLen(hexv) == 5 and findLen(ASCiiPairToHex(val)) > 3: 
                    print(' ')
                    print('M_KEY:', n, hexv, '(' + hexToASCiiPair(str(hex(n))) + ') HW_ID:', ASCiiPairToHex(val), '('+val+')')
                    Write('M_KEY: ' + hexv.upper() + ' (' + hexToASCiiPair(str(hex(n))) + ') HW_ID: ' + ASCiiPairToHex(val).upper() + ' ('+val+')')
                    break

            #elif  a > 0:
            #    print(' ')
            #    print('?M_KEY:'+ hexv, '(' + hexToASCiiPair(str(hex(n))) + ') HW_ID:', ASCiiPairToHex(val), '('+val+')')

        if n%1000 == 0: 
            printProgressBar(n, max, str(n) + '(' + hex(n).lstrip('0x').upper() + '-' +  num + ')/' + str(max))

    printProgressBar(max, max, 'Complete                                                         ')
    if min == max: Write("No valid keys found")
    print('')

def CreateUserPermit(M_KEY,HW_ID,M_ID):
    ehw_id = encrypt(M_KEY,HW_ID)[0]
    hex_string = ehw_id
    hex_value = hex(binascii.crc32(hex_string.encode('utf8')))
    return (ehw_id + hex_value.lstrip('0x') + M_ID).upper()
    
#---------------------------------------------------------------------------------------------------------------

def unitTest(): #unit tests - encrypt 
    if encrypt('10121', '12345')[0] != '66B5CBFDF7E4139D': print("Test 1 Failed", encrypt('10121', '12345'))
    if encrypt('3130313231', '3132333435')[0] != '66B5CBFDF7E4139D': print("Test 1 Failed", encrypt('3130313231', '3132333435')[0]) 

    if encrypt('123AB', 'FE321')[0] != 'A89D5B77F731DF86': print("Test 2 Failed", encrypt('123AB', 'FE321'))
    if encrypt('3132334142', '4645333231')[0] != 'A89D5B77F731DF86': print("Test 3b Failed", encrypt('3132334142', '4645333231'))

    if encrypt('abcde', 'EDCBA')[0] != 'C0AD0FF2ACE832EB': print("Test 3 Failed", encrypt('abcde', 'EDCBA'))
    if encrypt('4142434445', '4544434241')[0] != 'C0AD0FF2ACE832EB': print("Test 3d Failed", encrypt('4142434445', '4544434241'))

    if encrypt('98765', '12348')[0] != '73871727080876A0': print("Test 3b Failed", encrypt('98765', '12348'))
    if encrypt('3938373635', '3132333438')[0] != '73871727080876A0': print("Test 3e Failed", encrypt('3938373635', '3132333438'))

    #unit tests - decrypt 
    if decrypt('3130313231', '66B5CBFDF7E4139D')[0] != '3132333435': print("Test 4 Failed") 
    if decrypt('10121', '66B5CBFDF7E4139D')[0] != '3132333435': print("Test 5 Failed",decrypt('10121', '66B5CBFDF7E4139D'))
    if decrypt('123AB', 'A89D5B77F731DF86')[0] != '4645333231': print("Test 6 Failed",decrypt('123AB', 'A89D5B77F731DF86'))

    #unit test - hexToASCiiPair
    if hexToASCiiPair('123AB') != '3132334142': print("Test 7 Failed",hexToASCiiPair('123AB'))  
    if hexToASCiiPair('0x123AB') != '3132334142': print("Test 8 Failed",hexToASCiiPair('0x123AB')) 
    if hexToASCiiPair('10121') != '3130313231': print("Test 9 Failed",hexToASCiiPair('10121')) 
    if hexToASCiiPair('0x10121') != '3130313231': print("Test 9a Failed",hexToASCiiPair('0x10121')) 
    if hexToASCiiPair('0x254de') != '3235344445': print("Test 9b Failed",hexToASCiiPair('0x254de')) 
    if hexToASCiiPair('0x254DE') != '3235344445': print("Test 9c Failed",hexToASCiiPair('3235344445')) 
    if hexToASCiiPair('123') != '3132330202': print("Test 10 Failed",hexToASCiiPair('0x123')) 

    #unit test - ASCiiPairToHex
    if ASCiiPairToHex('3130313231') != '10121': print("Test 11 Failed",ASCiiPairToHex('3130313231')) 
    if ASCiiPairToHex('3130310202') != '101': print("Test 12 Failed",ASCiiPairToHex('3130310202')) 
    if ASCiiPairToHex('4646464646') != 'FFFFF': print("Test 13 Failed",ASCiiPairToHex('4646464646')) 
    if ASCiiPairToHex('3104040404') != '1': print("Test 14 Failed",ASCiiPairToHex('3104040404')) 

    #unit test - CreateUserPermit
    if str(CreateUserPermit('10121','12345','3130')) != '66B5CBFDF7E4139D5B6086C23130': print("Test Failed" , CreateUserPermit('10121','12345','3130'))
    if str(CreateUserPermit('3130313231','3132333435','3130')) != '66B5CBFDF7E4139D5B6086C23130': print("Test Failed" , CreateUserPermit('3130313231','3132333435','3130'))

    print("Tests Complete")

#---------------------------------------------------------------------------------------------------------------

unitTest()

# From S=63 docs
#M_KEY: 65825 10121 (3130313231) HW_ID: 12345 (3132333435)
findM_ID('66B5CBFDF7E4139D','From S=63 docs')

# From S=63 docs
#M_KEY: 624485 98765 (3938373635) HW_ID: 12348 (3132333438)
findM_ID('73871727080876A07E450C043031','From S=63 docs')

#M_KEY: 703710 0xabcde (373033373130) HW_ID: EDCBA (4544434241)
#findM_ID('C0AD0FF2ACE832EB','Derived')

#SAM ChartPilot 1100 Version 6.14 Build 69
#E7A63F22C8B0B9CD CAF68D32 3134
findM_ID('E7A63F22C8B0B9CDCAF68D323134','SAM ChartPilot 1100')

#encry_HW_ID = '057DA7ADC227C0D0'
#findM_ID('057DA7ADC227C0D0','Derived')

#encry_HW_ID = '7D88AC20B915A587'
#findM_ID('7D88AC20B915A587','Derived')

# Test from doc (might not be real...)
# M_KEY: 0x98765 (363234343835) HW_ID: 74568 (3132333438)
findM_ID('73871727080876A0','Test from doc (might not be real...)')# A79AB

#findM_ID('51ABA63B31D3BD5B','Derived')
#findM_ID('EB3C7E109D3A6064','Derived')

