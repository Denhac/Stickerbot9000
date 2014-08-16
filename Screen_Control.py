#!/usr/bin/python2

#includes
from Adafruit_CharLCDPlate import Adafruit_CharLCDPlate
from time import sleep
import cups
from os import listdir, remove
from os.path import isfile, join
import RPi.GPIO as GPIO

class stickerPrinter:

	imageLocation = ""
	files = {}
	currentID = ""
	lcd = None
	conn = None
	printer = None

	def __init__(self, imageLocation):
		self.imageLocation = imageLocation
		self.lcd = Adafruit_CharLCDPlate()
		self.lcd.message("Initializing\nStickerBOT9000")
		self.conn = cups.Connection()
		self.printer = self.conn.getPrinters().keys()[0]
		self.buttonPin=4
		GPIO.setmode(GPIO.BCM)
		GPIO.setup(self.buttonPin,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
		GPIO.add_event_detect(4, GPIO.RISING, bouncetime=3000)

	def getDollar(self):
#		self.loopcount = 0
		print "GETTING DOLLAR"
		self.printFile()
#		self.updateScreen("Insert Dollar")
#		while True:
#			self.loopcount = self.loopcount + 1
#			self.updateScreen("Insert Dollar "+str(((100-self.loopcount)/10)))
#			if (GPIO.input(self.buttonPin)):
#				print "Dollar In"
#				self.printFile()
#				return False
#			if (self.lcd.buttonPressed(self.lcd.UP)):
#				return False
#			if (self.lcd.buttonPressed(self.lcd.DOWN)):
#				return False
#			if self.loopcount > 90:
#				return False
#			sleep(.1)


	def updateScreen(self, text):
		self.lcd.clear()
		self.lcd.message("Image: "+str(self.currentID)+"\n"+text)

	def printFile(self):
		#self.getDollar()
		self.updateScreen("Now Printing")
		self.lcd.backlight(self.lcd.RED)
		image = self.imageLocation+self.files[self.currentID]
		print "printing: "+image
		printid = self.conn.printFile(self.printer, image, "Python_Status_print", {})
		while(self.conn.getJobs().get(printid,None) is not None):
			pass
		#sleep(3)
		self.updateScreen("\nPrinted. Thanks!")
		self.lcd.backlight(self.lcd.GREEN)
		sleep(3)
		if(self.currentID > 5):		
			remove(self.imageLocation+self.files[self.currentID])
			del self.files[self.currentID]
			self.getNextID()
		

	def checkFiles(self):
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
	def checkInput(self):
	#	if(self.lcd.buttonPressed(self.lcd.SELECT)):
		if(self.lcd.buttonPressed(self.lcd.RIGHT)):
			print"User: "+str(self.currentID)+" is trying to print"
			self.getDollar()
			sleep(.5)
			return True
		if(self.lcd.buttonPressed(self.lcd.UP)):
			self.getNextID()
			sleep(.5)
			return True
		if(self.lcd.buttonPressed(self.lcd.SELECT)):
			self.getNextID()
			sleep(.5)
			return True
		return False

	def run(self):
		self.lcd.clear()
		self.lcd.message("Ready")
		self.checkFiles()
		if len(list(self.files.viewkeys())) != 0:	
			self.currentID = int(list(self.files.viewkeys())[0])
		else:
			self.currentID = 0
		print "THE FIRST USER IS LUCKY NUMBER: "+str(self.currentID)
		self.updateScreen("Please Insert $1")
		while True:
			if self.currentID != 0:
				if (self.checkInput()):
					self.updateScreen("Please Insert $1")
			else:
				self.lcd.clear()
				self.lcd.message("Ready")
				while len(list(self.files.viewkeys())) == 0:
					sleep(.5)
					self.checkFiles()
				self.getNextID()
				self.updateScreen("Please Insert $1")	
			self.lcd.backlight(self.lcd.ON)
			self.checkFiles()

	def colorScreen(self, color):
		if(color == "RED"):
			self.lcd.backlight(self.lcd.RED)
		if(color == "GREEN"):
			self.lcd.backlight(self.lcd.GREEN)
		if(color == "WHITE"):
			self.lcd.backlight(self.lcd.WHITE)


if __name__ == "__main__":
	images = "/srv/http/images/"
	printStickers = stickerPrinter(images)
	printStickers.checkFiles()
	sleep(3)
	printStickers.run()
