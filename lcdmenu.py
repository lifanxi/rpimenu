#!/usr/bin/python
#
# Created by Alan Aufderheide, February 2013
#
# This provides a menu driven application using the LCD Plates
# from Adafruit Electronics.

import commands
from string import split
from time import sleep, strftime, localtime
from xml.dom.minidom import *
from Adafruit_CharLCD import Adafruit_CharLCD
from ListSelector import ListSelector
from Buttons import Buttons
from subprocess import * 
from time import sleep, strftime
from datetime import datetime

configfile = 'lcdmenu.xml'

# set DEBUG=1 for print debug statements
DEBUG = 0

DISPLAY_ROWS = 2
DISPLAY_COLS = 16

# set busnum param to the correct value for your pi
# RS, E, [Data] 
lcd = Adafruit_CharLCD(14, 15, [17,18,27,22])
btn = Buttons("lcdmenu", "/home/pi/.lircrc")

# in case you add custom logic to lcd to check if it is connected (useful)
#if lcd.connected == 0:
#    quit()

lcd.begin(DISPLAY_COLS, DISPLAY_ROWS)

# commands
def DoQuit():
    lcd.clear()
    lcd.message('Are you sure?\nPress Sel for Y')
    while 1:
        nb = btn.readButton()
        if nb == 'left':
            break;
        if nb == 'sel':
            lcd.clear()
            quit()
        sleep(0.25)

def DoShutdown():
    lcd.clear()
    lcd.message('Are you sure?\nPress Sel for Y')
    while 1:
        nb = btn.readButton()
        if nb == 'left':
            break
        if nb == 'sel':
            lcd.clear()
            commands.getoutput("sudo shutdown -h now")
            quit()
        sleep(0.25)

def LcdOff():
        pass

def LcdOn():
        pass

def LcdRed():
        pass

def LcdGreen():
        pass

def LcdBlue():
        pass

def LcdYellow():
        pass

def LcdTeal():
        pass

def LcdViolet():
        pass

def ShowDateTime():
    if DEBUG:
        print('in ShowDateTime')
    lcd.clear()
    while not (btn.readButton() == 'left'):
        sleep(0.25)
        lcd.home()
        lcd.message(strftime('%a %b %d %Y\n%I:%M:%S %p', localtime()))
    
def SetDateTime():
    if DEBUG:
        print('in SetDateTime')

def ShowIPAddress():
    if DEBUG:
        print('in ShowIPAddress')
    lcd.clear()
    lcd.message(commands.getoutput("/sbin/ifconfig").split("\n")[1].split()[1][5:])
    while 1:
        if btn.readButton() == 'left':
            break
        sleep(0.25)

def DoubanPlay():
    if DEBUG:
        print('in DoubanPlay')
    lcd.clear()
    lcd.message('Starting Douban')
    if commands.getoutput('netstat -nap | grep 10098 | grep LISTEN | wc -l')[0] == "0":
        commands.getoutput("sudo -u pi /home/pi/fmd/fmd")
        i = 0
        while commands.getoutput('netstat -nap | grep 10098 | grep LISTEN | wc -l')[0] == "0":
            i = i + 1
            sleep (1)
            if i > 10:
                lcd.clear()
                lcd.message("fmd start failed")
                sleep(1)
                return
    commands.getoutput("/home/pi/fmd/fmc play")
    DoubanInfo()

def DoubanStop():
    if DEBUG:
        print('in DoubanStop')
    lcd.clear()
    lcd.message('Stopping Douban')
    commands.getoutput("/home/pi/fmd/fmc stop")
    commands.getoutput("/home/pi/fmd/fmc end")

def DoubanLike():
    if DEBUG:
        print('in DoubanLike')
    lcd.clear()
    lcd.message('Like this song')
    commands.getoutput("/home/pi/fmd/fmc like")
    DoubanInfo()

def DoubanSkip():
    if DEBUG:
        print('in Douban Skip')
    lcd.clear()
    lcd.message('Skip this song')
    commands.getoutput("/home/pi/fmd/fmc skip")
    DoubanInfo()

def DoubanBan():
    if DEBUG:
        print('in DoubanPlay')
    lcd.clear()
    lcd.message('Ban this song')
    commands.getoutput("/home/pi/fmd/fmc ban")
    DoubanInfo()

def run_cmd(cmd,l):
        p = Popen(cmd % l, shell=True, stdout=PIPE)
        output = p.communicate()[0]
	output = output[0:len(output)-1]
        return output

def DoubanInfo():
    cmd = "/home/pi/fmd/fmc | sed -n %dp"
    if DEBUG:
        print('in DoubanPlay')
    lcd.clear();
    oldsong = ''
    lastpos = 0;
    while 1:
        nb = btn.readButton();
        if nb == 'left':
            break;
        if nb == 'right':
            lcd.clear()
            lcd.message('Skip this song')
            commands.getoutput("/home/pi/fmd/fmc skip")
        if nb == 'up':
            lcd.clear()
            lcd.message('Like this song')
            commands.getoutput("/home/pi/fmd/fmc like")
        if nb == 'down':
            lcd.clear()
            lcd.message('Ban this song')
            commands.getoutput("/home/pi/fmd/fmc ban")
            
        sleep(0.25)
        song = '                ' + run_cmd(cmd,2)
        time1 = run_cmd(cmd,3)
        if song == oldsong:
            lcd.home()
            t = song[lastpos:16+lastpos]
            if len(t) < 16:
                t += '                '[0:16-len(t)]
            lcd.message(t)
            lcd.write4bits(0xC0)
            lcd.message(time1) 
            lastpos = lastpos + 1
            if lastpos >= len(song):
                lastpos = 0
            continue
        oldsong=song
        lcd.clear()
        lcd.home()
        lastpos =0;
        lcd.message(song[lastpos:16])
        lcd.write4bits(0xC0)
        lcd.message(time1);
    
#only use the following if you find useful
def Use10Network():
    "Allows you to switch to a different network for local connection"
    lcd.clear()
    lcd.message('Are you sure?\nPress Sel for Y')
    while 1:
        nb = btn.readButton()
        if nb == 'left':
            break
        if nb == 'sel':
            # uncomment the following once you have a separate network defined
            commands.getoutput("sudo cp /etc/network/interfaces.static /etc/network/interfaces")
            lcd.clear()
            lcd.message('Please reboot')
            sleep(1.5)
            break
        sleep(0.25)

#only use the following if you find useful
def UseDHCP():
    "Allows you to switch to a network config that uses DHCP"
    lcd.clear()
    lcd.message('Are you sure?\nPress Sel for Y')
    while 1:
        nb = btn.readButton();
        if nb == 'left':
            break
        if nb == 'sel':
            # uncomment the following once you get an original copy in place
            commands.getoutput("sudo cp /etc/network/interfaces.dhcp /etc/network/interfaces")
            lcd.clear()
            lcd.message('Please reboot')
            sleep(1.5)
            break
        sleep(0.25)

def ShowLatLon():
    if DEBUG:
        print('in ShowLatLon')

def SetLatLon():
    if DEBUG:
        print('in SetLatLon')
    
def SetLocation():
    if DEBUG:
        print('in SetLocation')
    global lcd
    list = []
    # coordinates usable by ephem library, lat, lon, elevation (m)
    list.append(['New York', '40.7143528', '-74.0059731', 9.775694])
    list.append(['Paris', '48.8566667', '2.3509871', 35.917042])
    selector = ListSelector(list, lcd)
    item = selector.Pick()
    # do something useful
    chosen = list[item]

def CompassGyroViewAcc():
    if DEBUG:
        print('in CompassGyroViewAcc')

def CompassGyroViewMag():
    if DEBUG:
        print('in CompassGyroViewMag')

def CompassGyroViewHeading():
    if DEBUG:
        print('in CompassGyroViewHeading')

def CompassGyroViewTemp():
    if DEBUG:
        print('in CompassGyroViewTemp')

def CompassGyroCalibrate():
    if DEBUG:
        print('in CompassGyroCalibrate')
    
def CompassGyroCalibrateClear():
    if DEBUG:
        print('in CompassGyroCalibrateClear')
    
def TempBaroView():
    if DEBUG:
        print('in TempBaroView')

def TempBaroCalibrate():
    if DEBUG:
        print('in TempBaroCalibrate')
    
def AstroViewAll():
    if DEBUG:
        print('in AstroViewAll')

def AstroViewAltAz():
    if DEBUG:
        print('in AstroViewAltAz')
    
def AstroViewRADecl():
    if DEBUG:
        print('in AstroViewRADecl')

def CameraDetect():
    if DEBUG:
        print('in CameraDetect')
    
def CameraTakePicture():
    if DEBUG:
        print('in CameraTakePicture')

def CameraTimeLapse():
    if DEBUG:
        print('in CameraTimeLapse')

class CommandToRun:
    def __init__(self, myName, theCommand):
        self.text = myName
        self.commandToRun = theCommand
    def Run(self):
        self.clist = split(commands.getoutput(self.commandToRun), '\n')
        if len(self.clist) > 0:
            lcd.clear()
            lcd.message(self.clist[0])
            for i in range(1, len(self.clist)):
                while 1:
                    if btn.readButton() == 'down':
                        break
                    sleep(0.25)
                lcd.clear()
                lcd.message(self.clist[i-1]+'\n'+self.clist[i])          
                sleep(0.5)
        while 1:
            if btn.readButton() == 'left':
                break

class Widget:
    def __init__(self, myName, myFunction):
        self.text = myName
        self.function = myFunction
        
class Folder:
    def __init__(self, myName, myParent):
        self.text = myName
        self.items = []
        self.parent = myParent

def HandleSettings(node):
    global lcd
    # if node.getAttribute('lcdColor').lower() == 'red':
    #     lcd.backlight(lcd.RED)
    # elif node.getAttribute('lcdColor').lower() == 'green':
    #     lcd.backlight(lcd.GREEN)
    # elif node.getAttribute('lcdColor').lower() == 'blue':
    #     lcd.backlight(lcd.BLUE)
    # elif node.getAttribute('lcdColor').lower() == 'yellow':
    #     lcd.backlight(lcd.YELLOW)
    # elif node.getAttribute('lcdColor').lower() == 'teal':
    #     lcd.backlight(lcd.TEAL)
    # elif node.getAttribute('lcdColor').lower() == 'violet':
    #     lcd.backlight(lcd.VIOLET)
    # elif node.getAttribute('lcdColor').lower() == 'white':
    #     lcd.backlight(lcd.ON)
    # if node.getAttribute('lcdBacklight').lower() == 'on':
    #     lcd.backlight(lcd.ON)
    # elif node.getAttribute('lcdBacklight').lower() == 'off':
    #     lcd.backlight(lcd.OFF)

def ProcessNode(currentNode, currentItem):
    children = currentNode.childNodes

    for child in children:
        if isinstance(child, xml.dom.minidom.Element):
            if child.tagName == 'settings':
                HandleSettings(child)
            elif child.tagName == 'folder':
                thisFolder = Folder(child.getAttribute('text'), currentItem)
                currentItem.items.append(thisFolder)
                ProcessNode(child, thisFolder)
            elif child.tagName == 'widget':
                thisWidget = Widget(child.getAttribute('text'), child.getAttribute('function'))
                currentItem.items.append(thisWidget)
            elif child.tagName == 'run':
                thisCommand = CommandToRun(child.getAttribute('text'), child.firstChild.data)
                currentItem.items.append(thisCommand)

class Display:
    def __init__(self, folder):
        self.curFolder = folder
        self.curTopItem = 0
        self.curSelectedItem = 0
    def display(self):
        if self.curTopItem > len(self.curFolder.items) - DISPLAY_ROWS:
            self.curTopItem = len(self.curFolder.items) - DISPLAY_ROWS
        if self.curTopItem < 0:
            self.curTopItem = 0
        if DEBUG:
            print('------------------')
        str = ''
        for row in range(self.curTopItem, self.curTopItem+DISPLAY_ROWS):
            if row > self.curTopItem:
                str += '\n'
            if row < len(self.curFolder.items):
                if row == self.curSelectedItem:
                    cmd = '-'+self.curFolder.items[row].text
                    if len(cmd) < 16:
                        for row in range(len(cmd), 16):
                            cmd += ' '
                    if DEBUG:
                        print('|'+cmd+'|')
                    str += cmd
                else:
                    cmd = ' '+self.curFolder.items[row].text
                    if len(cmd) < 16:
                        for row in range(len(cmd), 16):
                            cmd += ' '
                    if DEBUG:
                        print('|'+cmd+'|')
                    str += cmd
        if DEBUG:
            print('------------------')
        lcd.home()
        lcd.message(str)

    def update(self, command):
        if DEBUG:
            print('do',command)
        if command == 'u':
            self.up()
        elif command == 'd':
            self.down()
        elif command == 'r':
            self.right()
        elif command == 'l':
            self.left()
        elif command == 's':
            self.select()
    def up(self):
        if self.curSelectedItem == 0:
            return
        elif self.curSelectedItem > self.curTopItem:
            self.curSelectedItem -= 1
        else:
            self.curTopItem -= 1
            self.curSelectedItem -= 1
    def down(self):
        if self.curSelectedItem+1 == len(self.curFolder.items):
            return
        elif self.curSelectedItem < self.curTopItem+DISPLAY_ROWS-1:
            self.curSelectedItem += 1
        else:
            self.curTopItem += 1
            self.curSelectedItem += 1
    def left(self):
        if isinstance(self.curFolder.parent, Folder):
            # find the current in the parent
            itemno = 0
            index = 0
            for item in self.curFolder.parent.items:
                if self.curFolder == item:
                    if DEBUG:
                        print('foundit')
                    index = itemno
                else:
                    itemno += 1
            if index < len(self.curFolder.parent.items):
                self.curFolder = self.curFolder.parent
                self.curTopItem = index
                self.curSelectedItem = index
            else:
                self.curFolder = self.curFolder.parent
                self.curTopItem = 0
                self.curSelectedItem = 0
    def right(self):
        if isinstance(self.curFolder.items[self.curSelectedItem], Folder):
            self.curFolder = self.curFolder.items[self.curSelectedItem]
            self.curTopItem = 0
            self.curSelectedItem = 0
        elif isinstance(self.curFolder.items[self.curSelectedItem], Widget):
            if DEBUG:
                print('eval', self.curFolder.items[self.curSelectedItem].function)
            eval(self.curFolder.items[self.curSelectedItem].function+'()')
        elif isinstance(self.curFolder.items[self.curSelectedItem], CommandToRun):
            self.curFolder.items[self.curSelectedItem].Run()

    def select(self):
        if DEBUG:
            print('check widget')
        if isinstance(self.curFolder.items[self.curSelectedItem], Widget):
            if DEBUG:
                print('eval', self.curFolder.items[self.curSelectedItem].function)
            eval(self.curFolder.items[self.curSelectedItem].function+'()')

# now start things up
uiItems = Folder('root','')

dom = parse(configfile) # parse an XML file by name

top = dom.documentElement

ProcessNode(top, uiItems)

display = Display(uiItems)
display.display()

while 1:
    nb = btn.readButton()
    if not nb:
        sleep(0.2)
        continue

    if nb == 'left':
        display.update('l')
        display.display()
        continue

    if nb == 'up':
        display.update('u')
        display.display()
        continue

    if nb == 'down':
        display.update('d')
        display.display()
        continue

    if nb == 'right':
        display.update('r')
        display.display()
        continue

    if nb == 'sel':
        display.update('s')
        display.display()
        continue
