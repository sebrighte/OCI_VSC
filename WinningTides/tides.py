from flask import make_response
# from flask_restful import Resource, Api, reqparse
# from flask_cors import CORS, cross_origin
import os
import datetime as dt
from datetime import datetime
from dateutil import parser
from fpdf import FPDF
#from PIL import Image, ImageFont, ImageDraw
import pytz
import requests
import json
import datetime

#workingdir = "/var/www/html/"#os.path.abspath(os.getcwd())

def Create_pdf(date, areas, appication):
    pdf = FPDF()
    dtnow = GetNextHighTidePortsmouth() if date == "" else GetHighTidePortsmouth(date)
    name=f"SolentStreams {dtnow.strftime('%d-%m-%y')}"
    if "1" in areas: CreatePDFNorth(pdf, dtnow, "North Solent", appication)
    if "2" in areas: CreatePDFNWest(pdf, dtnow, "North West Solent", appication)
    if "3" in areas: CreatePDFSWest(pdf, dtnow, "South West IOW", appication)
    if "4" in areas: CreatePDFEast(pdf, dtnow, "East IOW", appication)
    response = make_response(pdf.output(dest='S').encode('latin-1'))
    response.headers.set('Content-Disposition', 'attachment', filename=name + '.pdf')
    response.headers.set('Content-Type', 'application/pdf')
    return response

def getLocalTimestring(dttest, formatA):
    testUTC = dttest.strftime(formatA)
    testBST = dttest.astimezone(pytz.timezone('Europe/London')).strftime(formatA)
    if testUTC != testBST: return testBST + " BST"
    else: return testUTC + " UTC"

def GetNextHighTidePortsmouth(data=False):
    dtn = datetime.datetime.now() + dt.timedelta(hours=-6)
    dtTime = ""
    dtHeight = 0
    response = requests.get("https://easytide.admiralty.co.uk/Home/GetPredictionData?stationId=0065")
    JSON = json.loads(response.content)
    if data == True: return JSON
    for tidalEventList in JSON['tidalEventList']:
        if tidalEventList['eventType'] == 0: 
            dtTime = parser.parse(tidalEventList['dateTime'])
            dtHeight = tidalEventList['height']
            if dtTime >= dtn:
                break
    return (dtTime)

def GetHighTidePortsmouth(date):
    dt = parser.parse(date)
    dtTime = ""
    dtHeight = 0
    response = requests.get("https://easytide.admiralty.co.uk/Home/GetPredictionData?stationId=0065")
    JSON = json.loads(response.content)
    for tidalEventList in JSON['tidalEventList']:
        if tidalEventList['eventType'] == 0: 
            dtTime = parser.parse(tidalEventList['dateTime'])
            if dtTime >= dt:
                break
    return (dtTime)

def CreatePDFTtitlePage(pdf, dtnow, loc, application, orientation = "P"):
    pdf.add_page(orientation)
    pdf.set_font('arial','B',18)
    pdf.write(0, 'Winning Tides - Tidal Streams')
    pdf.ln(10)
    pdf.set_font('arial','',16)
    pdf.write(0, f'UK Solent ({loc})')
    pdf.ln(10)
    pdf.set_font('arial','B',10)
    pdf.write(0, f"Tidal Location: Portsmouth")
    pdf.ln(5)
    pdf.write(0, f"Prediction Date: {dtnow.strftime('%d-%m-%y')}")
    pdf.ln(5)
    pdf.write(0, f"Start: (-6 hrs): {getLocalTimestring((dtnow + dt.timedelta(hours=-6)),'%d-%m-%y %H:%M')}")
    pdf.ln(5)
    pdf.write(0, f"High Water (0 hrs): {getLocalTimestring(dtnow,'%d-%m-%y %H:%M')}")
    pdf.ln(5)
    pdf.write(0, f"End: (+6 hrs):{getLocalTimestring((dtnow + dt.timedelta(hours=6)),'%d-%m-%y %H:%M')}")
    pdf.ln(10)
    pdf.cell(0, 0, 'https://www.winningtides.co.uk/',link ="https://www.winningtides.co.uk/")
    pdf.image(f"{application.config.root_path}/static/winningtides.jpg", 10, 65, 115, 115/1.58)

def CreatePDFNorth(pdf, dtnow, loc, application):
    page = True
    offset = 10
    directory = f"{application.config.root_path}/baseimages/North"
    CreatePDFTtitlePage(pdf, dtnow, loc, application)
    for filename in sorted(os.listdir(directory)):
        f = os.path.join(directory, filename)
        if os.path.isfile(f):
            sp = filename.replace('.jpg', '').split('-')
            hrs = int(sp[3])
            if hrs > 9: hrs = hrs / 10
            if sp[3] == '05': hrs = 0.5
            if sp[2] == 'm' : hrs = hrs * -1
            if page == False: 
                pdf.add_page()
                offset = 10
            else: offset = 150
            page = not page
            #loadNorth(dtnow = dtnow, pdf=pdf, filePath=f, fileName=filename, offset=offset, hrs=hrs, textX=948, textY=741, dir="North")
            loadImage(dtnow,pdf,hrs,f,10,offset,185,130,156,125)

def CreatePDFNWest(pdf, dtnow, loc, application):
    page = True
    offset = 10
    directory = f"{application.config.root_path}/baseimages/NWest"
    CreatePDFTtitlePage(pdf, dtnow, loc, application)
    for filename in sorted(os.listdir(directory)):
        f = os.path.join(directory, filename)
        if os.path.isfile(f):
            sp = filename.replace('.jpg', '').split('-')
            hrs = int(sp[3])
            if hrs > 9: hrs = hrs / 10
            if sp[3] == '05': hrs = 0.5
            if sp[2] == 'm' : hrs = hrs * -1
            if page == False: 
                pdf.add_page()
                offset = 10
            else: offset = 150
            page = not page
            #loadNWest(dtnow = dtnow, pdf=pdf, filePath=f, fileName=filename, offset=offset, hrs=hrs, textX=64, textY=191, dir="NEast")
            loadImage(dtnow,pdf,hrs,f,10,offset,185,130,150,120)

def CreatePDFSWest(pdf, dtnow, loc, application):
    page = True
    offset = 10
    directory = f"{application.config.root_path}/baseimages/SWest"
    CreatePDFTtitlePage(pdf, dtnow, loc, application)
    for filename in sorted(os.listdir(directory)):
        f = os.path.join(directory, filename)
        if os.path.isfile(f):
            sp = filename.replace('.jpg', '').split('-')
            hrs = int(sp[3])
            if hrs > 9: hrs = hrs / 10
            if sp[3] == '05': hrs = 0.5
            if sp[2] == 'm' : hrs = hrs * -1
            if page == False: 
                pdf.add_page()
                offset = 10
            else: offset = 150
            page = not page
            loadImage(dtnow,pdf,hrs,f,10,offset,185,130,145,10)

def CreatePDFEast(pdf, dtnow, loc, application):
    page = True
    offset = 10
    directory = f"{application.config.root_path}/baseimages/East"
    CreatePDFTtitlePage(pdf, dtnow, loc, application, "L")
    for filename in sorted(os.listdir(directory)):
        f = os.path.join(directory, filename)
        if os.path.isfile(f):
            sp = filename.replace('.jpg', '').split('-')
            hrs = int(sp[3])
            if hrs > 9: hrs = hrs / 10
            if sp[3] == '05': hrs = 0.5
            if sp[2] == 'm' : hrs = hrs * -1
            if page == False: 
                pdf.add_page("L")
                offset = 10
            else: offset = 150
            page = not page
            loadImage(dtnow, pdf, hrs, f, offset, 20, 130, 170, offset + 85, 152)

def loadImage(dtnow, pdf, hrs, filePath, offset1, offset2, sizeX, sizeY, textX, textY):
    delta = dtnow + dt.timedelta(hours=hrs)
    title_text = getLocalTimestring(delta,'%d-%m-%y @ %H:%M')
    
    pdf.image(filePath, offset1, offset2, sizeX, sizeY)
    pdf.rect(offset1, offset2, sizeX, sizeY)
    pdf.set_fill_color(255,255,255)
    pdf.rect(textX-1, offset2-4 + textY,40,6,"F")
    pdf.text(textX, offset2 + textY, title_text)
