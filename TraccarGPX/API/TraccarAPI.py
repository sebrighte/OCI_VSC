from flask import Flask, redirect, request, render_template, send_file, Response, jsonify
from flask_restful import Resource, Api, reqparse
from flask_cors import CORS, cross_origin
import datetime
from requests.auth import HTTPBasicAuth
import requests
import json
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import io
import binascii
from datetime import date, time, datetime, timedelta
import socket
import time
import datetime
import os
#from SendBatteryEmail import sendmail

def sendmail(subject, message):
    import smtplib, ssl

    smtp_server = "outlook.office365.com"#"smtp.gmail.com"
    port = 993#587  # For starttls
    sender_email = "ernie_sebright@hotmail.com"#"ernie.sebright@gmail.com"
    password = "Janu2019!"#"Janu2019!" #input("Type your password and press enter: ")
    message = f"""Subject: {subject}\n{message}"""

    # Create a secure SSL context
    context = ssl.create_default_context()

    # Try to log in to server and send email
    try:
        server = smtplib.SMTP(smtp_server,port)
        #server.ehlo() # Can be omitted
        server.starttls(context=context) # Secure the connection
        #server.ehlo() # Can be omitted
        server.login(sender_email, password)
        # TODO: Send email here
        server.sendmail(sender_email, sender_email, message)
    except Exception as e:
        # Print any error messages to stdout
        print(e)
    finally:
        server.quit() 

#sudo cp /config/workspace/TraccarGPX/  /var/www/html/ -r

#sudo /etc/init.d/apache2 restart
#WSGIScriptAlias /traccar /var/www/html/TraccarGPX/API/TraccarAPI.py
#sudo cp /config/workspace/API /var/www/html/ -r
#sudo rm /var/www/html/TraccarGPX -R && sudo cp /config/workspace/TraccarGPX /var/www/html/ -r

application = Flask(__name__)

#https://api.sebright.synology.me/

@application.route('/')
def home():
   return render_template('index.html')

cors = CORS(application)
application.config['CORS_HEADERS'] = 'Content-Type'
api = Api(application)

# class con:
#     def __init__(self):
#         pass

#http://129.151.89.195:8005/DayGraph
class DayGraphAll(Resource):
    def get(self):
        print(".............................Here...................................")
        period = 2
        # today = datetime.datetime.now()
        dpiVal = int(request.args.get('dpi','1000'))
        # end = today.strftime("%Y-%m-%dT%H:%M:%SZ")

        today = datetime.datetime.now()
        end = today.strftime("%Y-%m-%dT%H:%M:%SZ")
        start = (today - timedelta(days=period)).strftime("%Y-%m-%dT00:00:00Z")

        start = (today - timedelta(days=period)).strftime("%Y-%m-%dT00:00:00Z")
        traccrURL = f"https://traccar.sebright.synology.me/api/reports/route?deviceId=7&from={start}&to={end}"
        print(traccrURL)
        HTTPauth = HTTPBasicAuth('Ernie', 'Maplatlop2021!')
        headersList = {'Accept': 'application/json'}
        response = requests.get(traccrURL, auth = HTTPauth, headers = headersList)
        JSON = json.loads(response.content)
        print(traccrURL)

        date = []
        level = []
        lastday = 0
        day = 0
        pdt = ""

        for result in JSON:
            try: 
                result2 = result['attributes']
                bl = result2['batteryLevel']
                tm = result['fixTime']

                pdt = datetime.datetime.strptime(tm, '%Y-%m-%dT%H:%M:%S.000+00:00')
                day = pdt.day
                #if day != lastday:
                #date.append(f"{pdt.day}/{pdt.hour}:{pdt.minute}")
                date.append(pdt.strftime("%d/%H:%M"))
                #date.append()

                level.append(bl)
            except: pass

            lastday = day
            
        fig = plt.figure(figsize=(8,4), dpi=dpiVal, tight_layout=True)
        plt.plot(date, level, linewidth=0.5)
        #plt.plot(date, level, 'o', label='data')
        plt.title(f"WA10JHO 24h Vehicle Battery Charge State - Current: ")# + pdt.strftime("%H:%M") + f" ({bl}%)")
        plt.xlabel("Date [day/time]")
        plt.ylabel("Battery Charge [%]")
        plt.show()
        plt.xticks(rotation=45, fontsize=1)
        #plt.savefig("/config/workspace/TraccarGPX/battery.png")
        #return send_file("/config/workspace/TraccarGPX/battery.png", mimetype='image/png')
        output = io.BytesIO()
        FigureCanvas(fig).print_png(output)
        return Response(output.getvalue(), mimetype='image/png')

#https://oci.sebright.synology.me/traccar/getdata
#http://129.151.89.195:8005/getdata
class getdata(Resource):
    @api.representation('text/json')
    def get(self):
        period = int(request.args.get('days','30'))
        dpiVal = int(request.args.get('dpi','180'))
        today = datetime.datetime.now()
        end = today.strftime("%Y-%m-%dT%H:%M:%SZ")
        start = (today - timedelta(days=period)).strftime("%Y-%m-%dT00:00:00Z")
        traccrURL = f"https://traccar.sebright.synology.me/api/reports/route?deviceId=7&from={start}&to={end}"

        HTTPauth = HTTPBasicAuth('Ernie', 'Maplatlop2021!')
        headersList = {'Accept': 'application/json'}
        response = requests.get(traccrURL, auth = HTTPauth, headers = headersList)
        JSON = json.loads(response.content)

        return jsonify(JSON)

#http://129.151.89.195:8005/traccar/batterydata
class batterydata(Resource):
    def get(self):
        period = int(request.args.get('days','2'))
        today = datetime.datetime.now()
        dpiVal = int(request.args.get('dpi','1000'))
        end = today.strftime("%Y-%m-%dT%H:%M:%SZ")
        start = (today - timedelta(days=period)).strftime("%Y-%m-%dT00:00:00Z")
        traccrURL = f"https://traccar.sebright.synology.me/api/reports/route?deviceId=7&from={start}&to={end}"

        HTTPauth = HTTPBasicAuth('Ernie', 'Maplatlop2021!')
        headersList = {'Accept': 'application/json'}
        response = requests.get(traccrURL, auth = HTTPauth, headers = headersList)
        JSON = json.loads(response.content)

        joint = []
        lastday = 0
        day = 0
        lasttime = ""

        for result in JSON:
            try: 
                result2 = result['attributes']
                bl = result2['batteryLevel']
                dt = result['deviceTime']
                ft = result['fixTime']
                jointstr = dt + "\t" + ft + "\t" + str(bl)
                joint.append(jointstr)

            except: pass

            lastday = day

        return jsonify(joint)

#http://129.151.89.195:8005/daygraph
class DayGraph(Resource):
    def get(self):
        
        period = int(request.args.get('days','30'))
        dpiVal = int(request.args.get('dpi','180'))
        today = datetime.datetime.now()
        end = today.strftime("%Y-%m-%dT%H:%M:%SZ")
        start = (today - timedelta(days=period)).strftime("%Y-%m-%dT00:00:00Z")
        traccrURL = f"https://traccar.sebright.synology.me/api/reports/route?deviceId=7&from={start}&to={end}"

        #https://traccar.sebright.synology.me/api/reports/route?deviceId=7&from=2022-02-21T00:00:00Z&to=2022-03-23T12:53:50Z

        print(traccrURL)

        HTTPauth = HTTPBasicAuth('Ernie', 'Maplatlop2021!')
        #response = requests.get(traccrURL, auth = HTTPauth)
        headersList = {'Accept': 'application/json'}
        response = requests.get(traccrURL, auth = HTTPauth, headers = headersList)

        JSON = json.loads(response.content)

        date = []
        level = []
        lastday = 0
        day = 0

        for result in JSON:
            try: 
                result2 = result['attributes']
                bl = result2['batteryLevel']
                tm = result['fixTime']

                pdt = datetime.datetime.strptime(tm, '%Y-%m-%dT%H:%M:%S.000+00:00')
                day = pdt.day
                if day != lastday:
                    date.append(pdt.strftime("%d-%m-%y"))
                    level.append(bl)
            except: pass

            lastday = day
        
        fig = plt.figure(figsize=(8,4), dpi=dpiVal, tight_layout=True)
        plt.plot(date, level)
        plt.plot(date, level, 'o', label='data')
        plt.title(f"WA10JHO Battery Charge (Daily) State - {period} Days - Current: " + pdt.strftime("%d-%m-%Y") + f" ({bl}%)")
        plt.xlabel("Date [date time]")
        plt.ylabel("Battery Charge [%]")
        plt.show()
        plt.xticks(rotation=45)
        #plt.savefig("/config/workspace/TraccarGPX/battery.png")
        #return send_file("/config/workspace/TraccarGPX/battery.png", mimetype='image/png')
        output = io.BytesIO()
        FigureCanvas(fig).print_png(output)
        return Response(output.getvalue(), mimetype='image/png')

#http://129.151.89.195:8005/histgraph?days=10
class HistGraph(Resource):
    def get(self):
        period = int(request.args.get('days','30'))
        dpiVal = int(request.args.get('dpi','500'))
        today = datetime.datetime.now()
        end = today.strftime("%Y-%m-%dT%H:%M:%SZ")
        start = (today - timedelta(days=period)).strftime("%Y-%m-%dT%H:%M:%SZ")
        traccrURL = f"https://traccar.sebright.synology.me/api/reports/route?deviceId=7&from={start}&to={end}"

        HTTPauth = HTTPBasicAuth('Ernie', 'Maplatlop2021!')
        headersList = {'Accept': 'application/json'}
        response = requests.get(traccrURL, auth = HTTPauth, headers = headersList)
        JSON = json.loads(response.content)

        date = []
        level = []
        lastday = 0
        day = 0

        for result in JSON:
            try: 
                result2 = result['attributes']
                bl = result2['batteryLevel']
                tm = result['fixTime']

                pdt = datetime.datetime.strptime(tm, '%Y-%m-%dT%H:%M:%S.000+00:00')
                #day = pdt.hour
                if pdt.hour != lastday:
                    date.append(pdt.strftime("%d-%m-%Y %H:%M"))
                    level.append(bl)
                lastday = pdt.hour
            except: pass

        fig = plt.figure(figsize=(8,4), dpi=dpiVal, tight_layout=True)
        plt.plot(date, level)
        #plt.plot(date, level, 'o', label='data')
        plt.title(f"WA10JHO {period} day (hourly) Battery Charge State - {pdt} ({bl}%)")
        plt.xlabel("Date [date time]")
        plt.ylabel("Battery Charge [%]")
        plt.show()
        plt.xticks(rotation=45, fontsize=3)
        #plt.savefig("/config/workspace/TraccarGPX/battery.png")
        #return send_file("/config/workspace/TraccarGPX/battery.png", mimetype='image/png')
        output = io.BytesIO()
        FigureCanvas(fig).print_png(output)
        return Response(output.getvalue(), mimetype='image/png')

#http://129.151.89.195:8005/gpx
class GetGPX(Resource):
    @api.representation('application/xml')

    def get(self):

        if not os.path.exists("/config/workspace/TraccarGPX/vantrack.xml"):
            return Response("No Data, looks like a track file has not been created yet", mimetype='text')

        f = open("/config/workspace/TraccarGPX/vantrack.xml","r")
        lines = f.readlines()
        return Response(lines, mimetype='application/xml')

#http://129.151.89.195:8005/testsend
class MockGPS(Resource):
    def get(self):
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
        #tc.sendLoc()

        return Response("Disabled as legacy GPS Device - Update device [imei] in Terminal request if required", mimetype='text/html')

#http://129.151.89.195:8005/checkbat?test=True
class checkbat(Resource):
    def get(self):
        test = request.args.get('test')
        traccrURL = "https://traccar.sebright.synology.me/api/positions?deviceId=7"
        HTTPauth = HTTPBasicAuth('Ernie', 'Maplatlop2021!')
        headersList = {'Accept': 'application/json'}
        response = requests.get(traccrURL, auth = HTTPauth, headers = headersList)
        JSON = json.loads(response.content)

        bl = 100

        for result in JSON:
            try:
                result2 = result['attributes']
                bl = result2['batteryLevel']
            except : bl = 100

        if bl <= 80 or test=='True': 
            sendmail("WA10JHO Battery Alert",f"Warning - The vehicle battery is at {bl}%")
            return Response(f"<h2>Alert Sent - Battery Level Checked</h2>The vehicle battery is at {bl}%", mimetype='text/html')

        return Response(f"<h2>Battery Level Checked</h2>Battery currently at {bl}%, No alert required", mimetype='text/html')

#http://129.151.89.195:8005/link
class link(Resource):
    def get(self):
        traccrURL = "https://traccar.sebright.synology.me/api/positions?deviceId=7"
        HTTPauth = HTTPBasicAuth('Ernie', 'Maplatlop2021!')
        headersList = {'Accept': 'application/json'}
        response = requests.get(traccrURL, auth = HTTPauth, headers = headersList)
        JSON = json.loads(response.content)

        for result in JSON:
            lat = result['latitude']
            lng = result['longitude']

        return redirect(f'http://maps.google.com/maps?t=h&q={lat},{lng}')
        #return redirect(f'https://www.google.com/search?q={lat},{lng}')

api.add_resource(DayGraph, '/daygraph')  
api.add_resource(batterydata, '/batterydata')   
api.add_resource(DayGraphAll, '/daygraphall')   
api.add_resource(HistGraph, '/histgraph')   
api.add_resource(GetGPX, '/gpx')  
api.add_resource(MockGPS, '/testsend')   
api.add_resource(getdata, '/getdata')   
api.add_resource(checkbat, '/checkbat')  
api.add_resource(link, '/link')  

if __name__ == '__main__':
    application.run(host='172.17.0.3', port=8006)#, debug=True)