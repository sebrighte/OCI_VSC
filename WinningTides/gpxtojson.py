
import requests
from flask import Response
import xmltodict, json
from geographiclib.geodesic import Geodesic
import os
    
clear = lambda: os.system('clear')
clear()

def calc(marks, leg, mf, mt):
    for mark in marks:
        if mark['name'] == mf[:2]: markf2 = mark
        if mark['name'] == mt[:2]: markt2 = mark

    ans = Geodesic.WGS84.Inverse(float(markf2['@lat']),float(markf2['@lon']),float(markt2['@lat']),float(markt2['@lon']))
    dist = (ans['s12']/1000)*0.539957
    brg = ans['azi2']
    if brg < 0: brg = brg + 360
    response = ""
    response = response + f"<tr><td>{leg}.</td><td>{'%.0f' % brg + '&#xb0;'}</td><td>{'%.1fnm' % dist}</td>"
    response = response + f"<td>-</td>" if len(mt) == 2 else response + f"<td>{mt[2]}</td>"
    response = response + f"<td>{'[' + markf2['sym'] + '] ' + markf2['desc'] + ' (' + markf2['name'] + ') to [' + markt2['sym'] + '] ' + markt2['desc'] + ' (' + markt2['name'] + ')'}</td></tr>"
    #return response, brg, dist, markt2['sym'], markt2['desc'], markt2['name']
    return response, brg, dist, markf2 , markt2

def findMark(marks, markin):
    for mark in marks:
        if mark['name'] == markin[:2]: return mark

def GetRouteTable(application, race):
    
    #gpxURL = "https://www.scra.org.uk/assets/documents/solentmarks-1.gpx"
    #marks = json.loads(json.dumps(xmltodict.parse(requests.get(gpxURL).content)))

    f = open(application.config.root_path + "/static/solentmarks-1.gpx", "r") 
    marks = json.loads(json.dumps(xmltodict.parse(f.read())))
    
    marks = marks['gpx']['wpt']
    dist = 0
    leg = 1
    ret = "<table class='center'><tr><th>Leg</th><th>Bearing</th><th>Distance</th><th>Rounding</th><th>Details</th></tr>"
    race = race.upper()
    course = race.split(" ")
    for i in range(0,len(course)-1):
        c = calc(marks,leg,course[i],course[i+1])
        dist = dist + c[2]
        ret = ret + c[0]
        leg = leg + 1
    return ret + "</table><br/><b>Total Distance:</b> %.1fnm" % dist

def GetGPXTrack(application, race):

    import gpxpy 

    # Create GPX header
    gpx = gpxpy.gpx.GPX()
    # Create first track in our GPX:
    gpx_track = gpxpy.gpx.GPXTrack()
    gpx.tracks.append(gpx_track)
    # Create first segment in our GPX track:
    gpx_segment = gpxpy.gpx.GPXTrackSegment()
    gpx_track.segments.append(gpx_segment)

    #gpxURL = "https://www.scra.org.uk/assets/documents/solentmarks-1.gpx"
    #marks = json.loads(json.dumps(xmltodict.parse(requests.get(gpxURL).content)))

    f = open(application.config.root_path + "/static/solentmarks-1.gpx", "r") 
    marks = json.loads(json.dumps(xmltodict.parse(f.read())))
    
    marks = marks['gpx']['wpt']
    race = race.upper()
    course = race.split(" ")
    try:
        for i in range(0,len(course)):
            markf2 = findMark(marks, course[i])
            gpx_segment.points.append(gpxpy.gpx.GPXTrackPoint(latitude=markf2['@lat'], longitude=markf2['@lon'], name=markf2['name']))
    except: return Response("One of the marks was not found, please check")
    return Response(gpx.to_xml(), mimetype='application/xml')
