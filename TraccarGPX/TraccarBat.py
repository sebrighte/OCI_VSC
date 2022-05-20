
import requests
import json
import sys
from requests.auth import HTTPBasicAuth
import datetime
from datetime import timedelta
import os

#os.system('cls' if os.name == 'nt' else 'clear')


def BatteryGraph(period = 30):
    today = datetime.datetime.now()
    end = today.strftime("%Y-%m-%dT23:59:59Z")
    start = (today - timedelta(days=period)).strftime("%Y-%m-%dT00:00:00Z")
    traccrURL = f"https://traccar.sebright.synology.me/api/reports/route?deviceId=1&from={start}&to={end}"


    HTTPauth = HTTPBasicAuth('Ernie', 'Maplatlop2021!')
    response = requests.get(traccrURL, auth = HTTPauth)
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
                date.append(f"{pdt.day}/{pdt.month}")
                level.append(bl)
        except: pass

        lastday = day

    import matplotlib.pyplot as plt

    plt.figure()
    plt.plot(date, level)
    plt.plot(date, level, 'o', label='data')
    plt.title(f"WA10JHO Battery Charge State - {period} Days")
    plt.xlabel("Date")
    plt.ylabel("Battery Charge %")
    plt.show()
    #plt.savefig("/config/workspace/TraccarGPX/battery2.png")
    plt.savefig("/config/workspace/TraccarGPX/battery.pdf")

#BatteryGraph()
