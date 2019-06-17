from bs4 import BeautifulSoup 
import xml.etree.cElementTree as ET
import urllib

frame = urllib.urlopen("http://www.mfds.go.kr/egg_detail.html")
sc = frame.read()
frame.close()

cd = BeautifulSoup(sc, "html.parser")
tb = cd.find("table")
#trs = tb.tbody.find_all("tr")
trs = tb.findAll('tr')
clear = []

for i in range(1,len(trs)):
    clear.append(trs[i].findAll('td'))

EGG = ET.Element("EGG")

for i in range(len(clear)):
    cnt = ET.SubElement(EGG, "Farm")
    ET.SubElement(cnt,"code").text = clear[i][1].get_text()
    ET.SubElement(cnt,"name").text = clear[i][3].get_text()
    ET.SubElement(cnt,"addr").text = clear[i][4].get_text()
    ET.SubElement(cnt,"drug").text = clear[i][8].get_text()

tree = ET.ElementTree(EGG)
tree.write("EggList.xml")

