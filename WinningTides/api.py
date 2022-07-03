
import sys, os


from flask import Flask, request, redirect, render_template, send_file, send_from_directory, jsonify, make_response, url_for, Response
from flask_restful import Resource, Api, reqparse
from flask_cors import CORS, cross_origin

import sys
#if "/var/www/html/" in os.path.abspath(os.getcwd()):
if "/" == os.path.abspath(os.getcwd()):
    sys.path.insert(0,"/var/www/html/WinningTides/")

from tides import *
from gpxtojson import * 
from date import * 

from json2html import *
import json

application = Flask(__name__)

#https://www.tidetimes.org.uk/portsmouth-tide-times-20220529
#http://129.151.89.195:8005
#http://129.151.89.195:8005.url_for(endpoint)
#http://129.151.89.195:8005/pdf
#http://129.151.89.195:8005/pdf/2022-05-30T11:22:00

# ps -fa
# UID          PID    PPID  C STIME TTY          TIME CMD
# abc        95397   95389  0 Jun05 pts/8    00:00:10 /bin/python3 /config/workspace/WinningTides/api.py
# abc        96269   95933  0 11:02 pts/9    00:00:00 ps -fa
# kill 95397

@application.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(application.root_path, 'static'),
                          'favicon.ico',mimetype='image/vnd.microsoft.icon')

@application.route('/getcwd')
def getcwd():
    return os.path.abspath(os.getcwd())

@application.route('/')
def Index():
    return render_template('index.html')

@application.route('/ecdis')
def ecdis():
    return render_template('ecdis.html')

@application.route('/chart')
def show_static_pdf():
    return redirect("static/3026.pdf")

@application.route('/tides')
def GetTides():
    from datetime import datetime
    response = requests.get("https://easytide.admiralty.co.uk/Home/GetPredictionData?stationId=0065")
    JSONOrig = json.loads(response.content)
    JSONOrig = JSONOrig['tidalHeightOccurrenceList']
    JSON = response.content.decode("utf-8")
    JSON = JSON.replace((":0,"), ":\"High Tide Event\",")
    JSON = JSON.replace((":1,"), ":\"Low Tide Event\",")
    JSON = JSON.replace(("eventType"), "Tidal Event")
    JSON = JSON.replace(("dateTime"), "DateTime")
    JSON = JSON.replace(("height"), "Height")
    JSON = json.loads(JSON)
    JSON = JSON['tidalEventList']
    for a in JSON: 
        del a["date"]
        del a['isApproximateHeight']
        del a['isApproximateTime']
        a['Height'] = str(round(a['Height'],2)) + "m"
        dt = datetime.strptime(a['DateTime'], '%Y-%m-%dT%H:%M:%S')
        #2022-07-01 05:54:00
        a['DateTime'] = is_dst(dt)
    tableAttrib = "class=\"center\""
    tableData = json2html.convert(json = JSON, table_attributes=tableAttrib)
    return render_template("tides.html", data=JSONOrig, tdata=tableData)

@application.route('/marks')
def GetMarks():

    gpxURL = "https://www.scra.org.uk/assets/documents/solentmarks-1.gpx"
    return requests.get(gpxURL).content

    # gpxURL = application.config.root_path + "/static/solentmarks-1.gpx"
    # f = open(gpxURL, "r") 
    # return f.read()

@application.route('/route')
def CourseWebPage():
    return render_template('route3.html')

@application.route('/streams')
def Create_html_tidetimes():
    f = open(application.config.root_path + "/static/html.txt", "r")
    txt = f.read()
    d = open(application.config.root_path + "/static/link.txt", "r")
    linko = d.read()

    resp = "<div class='column center border'><h3>Stream Areas</h3><img border='1px' width=300 class='center' src='static/chart.jpg'/></div>"
    
    JSON = GetNextHighTidePortsmouth(True)
    JSON = [obj for obj in JSON['tidalEventList'] if(obj['eventType'] == 0)] 
    dtnow = GetNextHighTidePortsmouth()
    
    link = linko
    link = link.replace("URL", f"pdf0")
    link = link.replace("TXT", f"<br/>Nearest Tidal Streams (+/- 6 hrs)")
    link = link.replace("TITLE", f"Click here for Solent & IOW \nStream Rates for the nearest tidal High tide")
    link = link.replace("DT", f"\n{getLocalTimestring(dtnow,'%a %d %b %Y %H:%M')}")
    link = link.replace("HEADING", f"Next Tidal Streams")
        
    resp = resp + link

    for Event in JSON:
        link = linko
        link = link.replace("HEADING", f"{getLocalTimestring(parser.parse(Event['dateTime']),'%a %d %b %Y %H:%M')}")
        link = link.replace("URL", f"pdf/{Event['dateTime']}")
        link = link.replace("TXT", f"<br/>{getLocalTimestring(parser.parse(Event['dateTime']),'%a %d %b %Y %H:%M')} ")
        link = link.replace("TITLE", f"Click here for Solent & IOW Stream Rates for \n{getLocalTimestring(parser.parse(Event['dateTime']),'%a %d %b %Y %H:%M')} ")
        link = link.replace("DT", f"\n{getLocalTimestring(parser.parse(Event['dateTime']),'%a %d %b %Y %H:%M')}")
        resp = resp + link
    
    return txt.replace("REPLACEME", resp)

@application.route('/route/<routein>')
def Getcourse(routein):
    return GetRouteTable(application, routein)

@application.route('/gpx/<routein>')
def GetGPX(routein):
    return GetGPXTrack(application, routein)

@application.route('/pdf/<datein>/<areasin>')
@application.route('/pdf/<datein>')
def Create_pdf_bydate(datein , areasin = "1234"):
    return Create_pdf(datein, areasin, application)


@application.route('/pdf0/<areasin>')
@application.route('/pdf0')
@application.
def Create_pdf_next(areasin = "1234"):
    #@application.representation('application/pdf')
    pdf = Create_pdf("", areasin, application)
    return pdf
   
cors = CORS(application)
application.config['CORS_HEADERS'] = 'Content-Type'
api = Api(application)

if __name__ == '__main__':
    application.run(host='172.17.0.3', port=8005)
    #application.run(host='172.17.0.3', port=8005, debug=True)