
import requests
import json
import sys
from requests.auth import HTTPBasicAuth
import datetime
from datetime import timedelta
import os

#os.system('cls' if os.name == 'nt' else 'clear')

def BatteryGraphDay(period = 7):
    today = datetime.datetime.now()
    end = today.strftime("%Y-%m-%dT%H:%M:%SZ")
    start = (today - timedelta(days=period)).strftime("%Y-%m-%dT%H:%M:%SZ")
    traccrURL = f"https://traccar.sebright.synology.me/api/reports/route?deviceId=1&from={start}&to={end}"


    HTTPauth = HTTPBasicAuth('Ernie', 'Maplatlop2021!')
    response = requests.get(traccrURL, auth = HTTPauth)
    JSON = json.loads(response.content)

    date = []
    level = []
    lastday = 0
    day = 0
    ctr = 0

    for result in JSON:
        try: 
            result2 = result['attributes']
            bl = result2['batteryLevel']
            tm = result['fixTime']
            ctr += 1

            pdt = datetime.datetime.strptime(tm, '%Y-%m-%dT%H:%M:%S.000+00:00')
            #day = pdt.hour
            if pdt.hour != lastday:
             date.append(f"{pdt.day} {pdt.hour}")
             level.append(bl)
             lastday = pdt.hour
        except: pass

    import matplotlib.pyplot as plt

    fig = plt.figure()
    plt.plot(date, level)
    plt.plot(date, level, 'o', label='data')
    plt.title(f"WA10JHO {period} day Battery Charge State - {pdt} ({bl}%)")
    plt.xlabel("Date")
    plt.ylabel("Battery Charge %")
    plt.show()
    plt.xticks(rotation=45)
    plt.savefig("/config/workspace/TraccarGPX/battery.png")
    return fig
    #plt.savefig("/config/workspace/TraccarGPX/battery.pdf")

BatteryGraphDay(7)
