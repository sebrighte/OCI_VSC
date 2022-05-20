# sudo apt install python3-gpxpy
# https://www.gpsvisualizer.com/
import requests
import json
from requests.auth import HTTPBasicAuth
import gpxpy 
import gpxpy.gpx 
import geopy.distance
from geopy import distance
import os
import datetime

#from TraccarBat import *
#from TraccarBatDay import *

verbose = True

if verbose: print("1. Set up environment")
#Constants and Variables-----------------
GPXFeatCtr = 0
distInKM = 0.1 #in Km (e.g. 0.1 = 1/10Km = 100m)
traccrURL = "https://traccar.sebright.synology.me/api/reports/route?deviceId=7&from=2021-01-01T00:00:00Z&to=2025-10-29T12:30:00Z"
#traccrURL = "https://traccar.sebright.synology.me/api/reports/route?deviceId=1&from=2022-01-01T00:00:00Z&to=2025-10-29T12:30:00Z"

#filename = "vantrack.xml"
filename = "/config/workspace/TraccarGPX/vantrack.xml"


if verbose: print(f'2. Read Data from Traccar API "{traccrURL}"')
#----------------------------------------

HTTPauth = HTTPBasicAuth('Ernie', 'Maplatlop2021!')
response = requests.get(traccrURL, auth = HTTPauth)

if verbose: print("3. Parse API Data")
#----------------------------------------

JSON = json.loads(response.content)
(lat,lng) = (JSON[0]['latitude'],JSON[0]['longitude'])

if verbose: print("4. Create GPX XML structure")
#----------------------------------------

# Create GPX header
gpx = gpxpy.gpx.GPX()
# Create first track in our GPX:
gpx_track = gpxpy.gpx.GPXTrack()
gpx.tracks.append(gpx_track)
# Create first segment in our GPX track:
gpx_segment = gpxpy.gpx.GPXTrackSegment()
gpx_track.segments.append(gpx_segment)

if verbose: print("5. Generate GPX data")
#----------------------------------------

for result in JSON:
    if  distance.distance((lat, lng), (result['latitude'], result['longitude'])).km > distInKM:
        (lat, lng, ele, spd) = (result['latitude'], result['longitude'], result['altitude'],result['speed'])
        tme = datetime.datetime.strptime(result['fixTime'], '%Y-%m-%dT%H:%M:%S.%f+00:00')
        # Create point:
        gpx_segment.points.append(gpxpy.gpx.GPXTrackPoint(latitude=lat, longitude=lng, elevation=ele, time=tme, speed=spd, name=f"ID:{str(GPXFeatCtr)}"))
        GPXFeatCtr += 1

if verbose: print("6. Write GPX data to File")
#----------------------------------------

f = open(filename, "w")
f.write(gpx.to_xml())
f.close()

if verbose: print(f'7. Track "{os.getcwd()}/{filename}" created with {GPXFeatCtr} points (with min {int(distInKM*1000)}m movement)')
#----------------------------------------

if verbose: print("9. Create Battery Graph")
#BatteryGraph()
#BatteryGraphDay()
#----------------------------------------

if verbose: print("10. Task complete")
