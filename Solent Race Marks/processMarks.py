
import xml.etree.ElementTree as ET
import requests
from urllib.request import urlopen
import os

#import easygui
#easygui.msgbox("This is a message!", title="simple gui")

def dumpInc(msg, pos = 0):
    if pos == -1: 
        os.system('cls' if os.name=='nt' else 'clear')
        print("...Start")
    if pos == 1 : print("...End")
    if pos == 0 : print(f"{dumpInc.counter}. {msg}")
    dumpInc.counter += 1

dumpInc.counter = 0

path = 'Solent Race Marks/'
fileName = 'iSailor Solent Marks 2022.gpx'
url = 'https://www.scra.org.uk/assets/documents/solentmarks-1.gpx'

dumpInc("",-1)
#-----------------------------------------------------------
try:
    os.remove(path + fileName)
    dumpInc(f"Delete existing GPX file '{fileName}'")
except: pass

dumpInc(f"Load Base GPX '{url}'")
#-----------------------------------------------------------
#tree = ET.parse('Solent Race Marks/solentmarks-1.gpx')
tree = ET.parse(urlopen(url))
root = tree.getroot()
attrib = {}

root.set('xmlns', 'http://www.topografix.com/GPX/1/1')
root.set('version', '1.1')
root.set('creator', 'Wärtsilä iSailor')
root.set('author', 'SebrightSoftware')

dumpInc('Reading ' +  str(sum(1 for _ in root.iter("wpt"))) + ' Waypoints')
#-----------------------------------------------------------
for elem in root.iter('wpt'):
    sym = elem.find('sym').text
    id = elem.find('name').text
    desc = elem.find('desc').text
    elem.remove(elem.find('desc'))
    elem.find('name').text = id + '- ' + desc + ' (' + sym + ')'
    elem.append(elem.makeelement('type',attrib))
    elem.find('type').text = 'Symbol'
    elem.append(elem.makeelement('cmt',attrib))
    elem.find('cmt').text = desc
    elem.find('sym').text = 'Waypoint'
    elem.append(elem.makeelement('geoidheight',attrib))
    elem.find('geoidheight').text = '0'

    #elem.append(elem.makeelement('id',attrib))
    #elem.find('id').text = id

dumpInc("Create GPX file")
#-----------------------------------------------------------
#ET.indent(ET.ElementTree(root), space="\t", level=0)

dumpInc(f"Save updated GPX file")
#-----------------------------------------------------------
tree.write(path + fileName, encoding="utf-8", xml_declaration=True)

if os.path.exists(path + fileName):
    dumpInc(f"Saved GPX file '{fileName}'")
else:
    dumpInc(f"Error: file '{fileName}' not saved")

dumpInc("",1)
#-----------------------------------------------------------
