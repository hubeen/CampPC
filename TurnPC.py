import subprocess as sp
from multiprocessing import Process, Queue, Manager
import xml.etree.cElementTree as ET
import threading
import time

m = Manager()
Ons = m.list()
Offs = m.list()

def chck(On,Off,x,y):
    for i in range(x, y+1):
        st, res = sp.getstatusoutput("ping -s1 -q -c1 -w1 " + "8.8.8." + str(i))
        if st == 0:
            On.append(str(i))
            #print (str(i) + " is Up !")
        else:
            Off.append(str(i))
            #print (str(i) + " is Down !")

def Multi():
    global Ons
    global Offs
    
    p0 = Process(target=chck, args=(Ons, Offs,1, 7))
    p1 = Process(target=chck, args=(Ons, Offs,8, 14))
    p2 = Process(target=chck, args=(Ons, Offs,15, 21))
    p3 = Process(target=chck, args=(Ons, Offs,22, 28))
    p4 = Process(target=chck, args=(Ons, Offs,29, 35))
    p5 = Process(target=chck, args=(Ons, Offs,36, 42))
    p6 = Process(target=chck, args=(Ons, Offs,43, 49))
    p7 = Process(target=chck, args=(Ons, Offs,50, 56))
    p8 = Process(target=chck, args=(Ons, Offs,57, 63))
    p9 = Process(target=chck, args=(Ons, Offs,63, 67))
    
    pro = [p0,p1,p2,p3,p4,p5,p6,p7,p8,p9]
    proc = []
    for p in pro:
        proc.append(p)
        p.start()

    for pc in proc:
        pc.join()

def Auto(sec=60.0):
    global Ons
    global Offs

    Multi()

    CampPC= ET.Element("CampPC")
    now  = time.localtime()

    for i in Ons:
        ET.SubElement(CampPC, "N" + str(i)).text = "사용중"

    for j in Offs:
        ET.SubElement(CampPC, "N" + str(j)).text = "미사용"
        
    ET.SubElement(CampPC, "time").text ="%04d-%02d-%02d %02d:%02d:%02d" % (now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec)
    
    tree = ET.ElementTree(CampPC)
    tree.write("OnOffList.xml")
    Ons = m.list()
    Offs = m.list()

if __name__ == '__main__':
    while(True):
        Auto()
        time.sleep(60)

