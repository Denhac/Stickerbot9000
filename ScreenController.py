#! /usr/bin/python2

####################################################################
#                      Stickerbot Sticker Printer                  #
#                               By Krav                            #
#                                 v1.1                             #
####################################################################

# Includes
from Adafruit_CharLCDPlate import Adafruit_CharLCDPlate
from time import sleep
import cups
from os import listdir, remove
import RPi.GPIO as GPIO
import sys


class stickerPrinter:

    imageLocation = ""
    files = {}
    currentID = ""
    lcd = None
    conn = None
    printer = None
    waiting_for_input = 0

    def __init__(self, imageLocation):
        print "Setting defaults and initializing software"
        self.imageLocation = imageLocation
        self.lcd = Adafruit_CharLCDPlate()
        self.lcd.message("Initializing\nStickerBOT9000")
        self.conn = cups.Connection()
        self.printer = self.conn.getPrinters().keys()[0]
        self.buttonPin = 4
        print "Turning on GPIO"
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.buttonPin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.add_event_detect(4, GPIO.RISING, bouncetime=3000)
        self.checkFiles()

    def printFile(self):
        print "Starting to print a sticker"
        self.updateScreen("Now Printing", "RED")
        image = self.imageLocation+self.files[self.currentID]
        print "Printing: "+image
        print "Contacting CUPS, the printer daemon"
        printid = self.conn.printFile(self.printer, image, "Python_Status_print", {})
        print "Waiting for the print job to complete."
        while(self.conn.getJobs().get(printid, None) is not None):
            pass
        self.updateScreen("\nPrinted. Thanks!", "GREEN")
        self.lcd.backlight(self.lcd.GREEN)
        sleep(3)
        print "Checking if the image is a one-time sticker"
        if(self.currentID > 5):
            print "Sticker is a one time sticker. Deleting"
            remove(self.imageLocation+self.files[self.currentID])
            del self.files[self.currentID]
            self.getNextID()
        else:
            print "Sticker is not a one time sticker. Keeping"

    def checkFiles(self):
        if self.waiting_for_input != 1:
            print "I'm waiting for a button press or dollar bill"
            print "Until i get one of those, I'll be checking for new stickers!"
            self.waiting_for_input = 1
        for fileName in listdir(self.imageLocation):
            id = int(''.join(x for x in fileName if x.isdigit()))
            if(id not in self.files):
                self.files[id] = fileName

    def getNextID(self):
        ids = list(self.files.viewkeys())
        if len(ids) != 0:
            if self.currentID != 0:
                if self.currentID in self.files:
                    location = ids.index(self.currentID)
                    if location == len(ids)-1:
                        self.currentID = list(self.files.viewkeys())[0]
                    else:
                        self.currentID = list(self.files.viewkeys())[location+1]
                else:
                    self.currentID = list(self.files.viewkeys())[0]
            else:
                self.currentID = list(self.files.viewkeys())[0]
        else:
            self.currentID = 0
        print "Switching up to image"

    def getPrevID(self):
        ids = list(self.files.viewkeys())
        if len(ids) != 0:
            if self.currentID != 0:
                if self.currentID in self.files:
                    location = ids.index(self.currentID)
                    if location == 0:
                        self.currentID = list(self.files.viewkeys())[len(ids)-1]
                    else:
                        self.currentID = list(self.files.viewkeys())[location-1]
                else:
                    self.currentID = list(self.files.viewkeys())[0]
            else:
                self.currentID != list(self.files.viewkeys())[0]
        else:
            self.currentID = 0
        print "Switching down to image"

    def checkInput(self):
        if(self.lcd.buttonPressed(self.lcd.RIGHT)):
            print "User: "+str(self.currentID)+" is trying to print"
            self.printFile()
            sleep(.5)
            return True
        if(self.lcd.buttonPressed(self.lcd.UP)):
            self.getNextID()
            sleep(.5)
            return True
        if(self.lcd.buttonPressed(self.lcd.SELECT)):
            self.getPrevID()
            sleep(.5)
            return True
        return False

    def run(self):
        print ("Ready to go")
        self.updateScreen("Ready", "WHITE")
        if len(list(self.files.viewkeys())) != 0:
            self.currentID = int(list(self.files.viewkeys())[0])
        else:
            self.currentID = 0
        print "Starting with Sticker : "+str(self.currentID)
        self.updateScreen("Please Insert $1", "BLUE")
        while True:
            if self.currentID != 0:
                if (self.checkInput()):
                    self.updateScreen("Please Insert $1", "BLUE")
            else:
                self.updateScreen("Ready", "WHITE")
                while len(list(self.files.viewkeys())) == 0:
                    sleep(.5)
                    self.checkFiles()
                self.getNextID()
                self.updateScreen("Please Insert $1", "BLUE")

            self.lcd.backlight(self.lcd.ON)
            self.checkFiles()

    # updateScreen - A simple method to ease changing of the screen.
    #   text  - Text to update the screen to.
    #   color - The color to change the screen. In this case you choose between RED, GREEN, BLUE, and WHITE.

    def updateScreen(self, text, color):
        print "Updating Screen: %s" + text
        self.lcd.clear()
        self.lcd.message("Image: "+str(self.currentID)+"\n"+text)
        if(color == "BLUE"):
            print "Changing the color of my screen to blue"
            self.lcd.backlight(self.lcd.BLUE)
        if(color == "RED"):
            print "changing the color of my screen to red"
            self.lcd.backlight(self.lcd.RED)
        if(color == "GREEN"):
            print "changing the color of my screen to green"
            self.lcd.backlight(self.lcd.GREEN)
        if(color == "WHITE"):
            print "changing the color of my screen to white"
            self.lcd.backlight(self.lcd.WHITE)

# main method. for doing main method things.

if __name__ == "__main__":
    if(len(sys.argv) < 2):
        print("\tUsage: %s imageDirectory" % sys.argv[0])
        exit(0)
    # Print out a bit of info about stickerbot
    print "----------- Hello! I'm --------------"
    print"   _____ _______ _____ _____ _  ________ _____  ____   ____ _______    ___   ___   ___   ___  "
    print"  / ____|__   __|_   _/ ____| |/ /  ____|  __ \|  _ \ / __ \__   __|  / _ \ / _ \ / _ \ / _ \ "
    print" | (___    | |    | || |    | ' /| |__  | |__) | |_) | |  | | | |    | (_) | | | | | | | | | |"
    print"  \___ \   | |    | || |    |  < |  __| |  _  /|  _ <| |  | | | |     \__, | | | | | | | | | |"
    print"  ____) |  | |   _| || |____| . \| |____| | \ \| |_) | |__| | | |       / /| |_| | |_| | |_| |"
    print" |_____/   |_|  |_____\_____|_|\_\______|_|  \_\____/ \____/  |_|      /_/  \___/ \___/ \___/ "
    print ""
    print "I was designed by members of denhac (the booth you're at right now) as a donation box"
    print "for DEFCON 22. DEFCON is one of the biggest, if not the biggest security convention in"
    print "the entire world, held in Las Vegas every August. There were 6 members of the denhac"
    print "team who worked on me. 2 built the case you see here, 2 worked on the electronics and a"
    print "final two wrote software and configured my systems to make me do all sorts of cool stuff"
    print ""
    print "I've got several different parts that make me do the cool things I do. My brain is made"
    print "with a raspberry pi running \"rasbian\" linux. It takes input from the two buttons and"
    print "the dollar bill acceptor and outputs on the little LCD and on it's terminal (what you're"
    print "reading right now). I've been told to be extra talkative about what happens every time"
    print "you push a button, or insert a dollar, so feel free to push buttons and I'll tell you what"
    print "I'm doing as I do it"
    print "-------------------------------------"
    printStickers = stickerPrinter(sys.argv[1])
    printStickers.run()
