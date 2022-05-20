import binascii
from datetime import date, time, datetime
import socket
import time

# def hextocoord(coord):
#     b = bytes(coord, 'utf-8')
#     ba = binascii.a2b_hex(b)
#     x = int.from_bytes(ba, byteorder='big', signed=True)
#     y = ((int.from_bytes(ba, byteorder='big', signed=True)/30000)/60)
#     if (x & 0x8000) == 0x8000: y = y * -1
#     return str( "{:.5f}".format(y))

# def hexToDateTime(dt):
#     year = int(dt[0:2], 16)
#     month = int(dt[2:4], 16)
#     day = int(dt[4:6], 16)
#     hour = int(dt[6:8], 16)
#     min = int(dt[8:10], 16)
#     sec = int(dt[10:12], 16)
#     return str(day).rjust(2, '0') + '/' + str(month).rjust(2, '0') + '/' + str(year).rjust(2, '0') + ' ' + str(hour).rjust(2, '0') + ':' + str(min).rjust(2, '0') + ':' + str(sec).rjust(2, '0')

# def datetimeToHex(tdstr = ''):
#     td = datetime.now()
#     if tdstr != '': td = datetime.strptime(tdstr, '%d%m%Y %H:%M:%S')
#     year = int(str(td.year)[2:4])
#     month = td.month
#     day = td.day
#     hour = td.hour
#     min = td.minute
#     sec = td.second;
#     return hex(year).lstrip('0x').rjust(2, '0') + hex(month).lstrip('0x').rjust(2, '0') + hex(day).lstrip('0x').rjust(2, '0') + hex(hour).lstrip('0x').rjust(2, '0') + hex(min).lstrip('0x').rjust(2, '0') + hex(sec).lstrip('0x').rjust(2, '0')

# def gpsStreamNow(): #Home location with current time
#     #origGps = '78781f12160214000605c9057865140055bfab001c0000ea0a53b4005420004714890d0a'
#     origGps = '78781f12160214000605c9057865140055c1ab001c0000ea0a53b4005420004714890d0a'
#     gps2 = origGps[0:8] + datetimeToHex() + origGps[20:]
#     return gps2

class traccar:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server = ("traccar.sebright.synology.me",5023)
    Terminal = '78780d01035288707540256400018cdd0d0a'
    HeartBeat = '78780a1344060300000048e7750d0a'

    def connect(self):
        try:
            self.s.connect(("traccar.sebright.synology.me", 5023))
            print("Socket Connected Successfully", self.server)
        except: print("SocketAlready Connected")

    def close(self):
        self.s.close()
        print("Socket Connection Closed")

    def sendLoc(self):
        self.s.send(binascii.unhexlify(self.Terminal))
        self.s.send(binascii.unhexlify(self.gpsStreamNow()))
        self.s.send(binascii.unhexlify(self.HeartBeat))
        print("Location Fix and Heartbeat Sent")

    def gpsStreamNow(self): #Home location with current time
        #origGps = '78781f12160214000605c9057865140055bfab001c0000ea0a53b4005420004714890d0a'
        origGps = '78781f12160214000605c9057865140055c1ab001c0000ea0a53b4005420004714890d0a'
        return origGps[0:8] + self.datetimeToHex() + origGps[20:]

    def datetimeToHex(self, tdstr = ''):
        td = datetime.now()
        if tdstr != '': td = datetime.strptime(tdstr, '%d%m%Y %H:%M:%S')
        year = int(str(td.year)[2:4])
        month = td.month
        day = td.day
        hour = td.hour
        min = td.minute
        sec = td.second
        return hex(year).lstrip('0x').rjust(2, '0') + hex(month).lstrip('0x').rjust(2, '0') + hex(day).lstrip('0x').rjust(2, '0') + hex(hour).lstrip('0x').rjust(2, '0') + hex(min).lstrip('0x').rjust(2, '0') + hex(sec).lstrip('0x').rjust(2, '0')

tc = traccar()
tc.connect()
tc.sendLoc()

start_time = time.time()
seconds = 10#5 * 60
ctr = 0
ctrMax = 12

start_time = time.time()

print("Sending fix every",seconds, "seconds", "for" , int((seconds*ctrMax)/60), "minutes" )

while True and ctr <= ctrMax:
    current_time = time.time()
    elapsed_time = current_time - start_time
    if elapsed_time % seconds == 0:
        tc.sendLoc()
        ctr = ctr + 1

tc.close()