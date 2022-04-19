# -*- coding: utf-8 -*-


# This file is part of Editor_NAO_V2.3.

# Editor_NAO_V2.3 is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

# Editor_NAO_V2.3 is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

# You should have received a copy of the GNU General Public License along with Editor_NAO_V2.3. If not, see <https://www.gnu.org/licenses/>.
import sys
import argparse
from Tkinter import *
import tkMessageBox
from naoqi import ALProxy
import math

reload(sys)
sys.setdefaultencoding("utf-8")

def  test(ip,port):
    port=int(port)
    try:
        test=ALProxy("ALRobotPosture", ip, port)
    except:
        return False
    return True

def pozice(ip,port, pozice):
    port=int(port)
    #print(ip)
    #print(port)
    #print(pozice)
    try:
        #motion  = ALProxy("ALMotion", ip, port)
        posture = ALProxy("ALRobotPosture", ip, port)
    except Exception, e:

        k=str(e)
        tkMessageBox.showerror("Chyba","Nedokázal jsem se připojit: \n " + k)
        return 1
    try:
        posture.goToPosture(pozice, 0.8)
        #print posture.getPostureFamily()

    except Exception, x:
        x=str(x)
        tkMessageBox.showerror("Chyba","Z nějakého důvodu nemohu provést požadovanou akci \n " + x)
        return 2
    return 0

def mluv(ip,port,text):
    port=int(port)
    try:
        tts = ALProxy("ALTextToSpeech", ip, port)
        tts.setLanguage("Czech")
        tts.say(text)
    except Exception, e:
        k=str(e)
        tkMessageBox.showerror("Chyba","Nedokázal jsem se připojit: \n " + k)
        return 1
    return 0
        
def cti(ip,port,data):
    k=mluv(ip,port,data)
    return k

def jdi(ip,port,vzdalenost):
    port=int(port)
    vzdalenost=float(vzdalenost)
    vzdalenost=vzdalenost/100
    #print vzdalenost
    try:
        motion  = ALProxy("ALMotion", ip, port)
        posture = ALProxy("ALRobotPosture", ip, port)
    except Exception, e:
        k=str(e)
        tkMessageBox.showerror("Chyba","Nedokázal jsem se připojit: \n " + k)
        return 1

    try:
        if posture.getPostureFamily() =="StandInit":
            motion.setStiffnesses("Body", 1.0)
            motion.moveTo(vzdalenost, 0, 0)
        else:
            posture.goToPosture("StandInit", 0.8)
            motion.setStiffnesses("Body", 1.0)
            motion.moveTo(vzdalenost, 0, 0)
            #problem s post, vytvari unblocking call -> paralelismus
        posture.goToPosture("Stand")
    except Exception,e :
        pass
    return 0

def otoc(ip,port,hodnota):
    port=int(port)
    hodnota=float(hodnota)
    hodnota= hodnota*math.pi/180
    #print hodnota
    try:
        motion  = ALProxy("ALMotion", ip, port)
        posture = ALProxy("ALRobotPosture", ip, port)
    except Exception, e:
        k=str(e)
        tkMessageBox.showerror("Chyba","Nedokázal jsem se připojit: \n " + k)
        return 1

    try:
        if posture.getPostureFamily() =="StandInit":
            motion.setStiffnesses("Body", 1.0)
            motion.moveTo(0, 0, hodnota)
        else:
            posture.goToPosture("StandInit", 0.8)
            motion.setStiffnesses("Body", 1.0)
            motion.moveTo(0, 0, hodnota)
        
    except Exception,e :
        x=str(e)
        tkMessageBox.showerror("Chyba","Chyba","Z nějakého důvodu nemohu provést požadovanou akci \n "+ x)
        return 2
    return 0
