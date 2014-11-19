#!/usr/bin/python2

#includes
from Adafruit_CharLCDPlate import Adafruit_CharLCDPlate
from time import sleep
import cups
import argparse
from os import listdir, remove
from os.path import isfile, join
import RPi.GPIO as GPIO
from enum import Enum


class Color(Enum):
	red = 1
	blue = 2
	green = 3
	white = 4

class ScreenController:

	# Class Variables! YAY!
	# should flesh these out more, possibly add some protection
	imageLocation = ""
	files = {}
	currentID = ""
	lcd = None
	conn = None
	printer = None
		
	# what's called when we make the stickerprinter. I'd like to make this less....hardcoded.
	
	def __init__(self, imageLocation):
		self.imageLocation = imageLocation
		self.lcd = Adafruit_CharLCDPlate()
		self.writeLCD("Initializing",Color.white)
		self.conn = cups.Connection()
		self.printer = self.conn.getPrinters().keys()[0]
		self.checkFiles()

	# This originally handled all the code for getting a dollar, but was slowly reduced down and now it does literally fuck-all
	# However, once we get the abiliy to control the bill acceptor, and make this much more robust,
	# I'd like to make it useful again.
	def getDollar(self):
		print "GETTING DOLLAR"
		self.printFile()

	# This was written as a way to easily update the LCD screen, since we do it so goddamn much.
	# Should be combined with the screen color method at the bottom of this file, because we change colors so much too.

	# This method handles all of the logic for actually getting a sticker from "selected" to printed.
	def printFile(self):
		self.writeLCD("Now Printing",Color.red)
		image = self.imageLocation+self.files[self.currentID]
		print "printing: "+image
		# Could use a much better descriptor here than "Python_Status_print"
		printid = self.conn.printFile(self.printer, image, "StickerBot Sticker: "+str(self.currentID), {})
		# Here we do nothing until the job is done. Literally a loop until the printer no longer has the job in it's queue.
		# Possible issue here. If there are other hung jobs in the printer, the printer can just sit there and the entire
		# bot can hang. should look into wiping out all jobs in queue at the start of stickerbot maybe?	
		while(self.conn.getJobs().get(printid,None) is not None):
			pass
		self.writeLCD("\nPrinted. Thanks!",Color.green)
		# This sleep is here purely so that the user gets a chance to see the message.
		sleep(3)
		# This was implemented at defcon in order to provide the standard stickers all the time.
		# Basically, 1-5 are the "Default" or Premade stickers, and those don't get deleted. Otherwise they do.
		if(self.currentID > 5):		
			remove(self.imageLocation+self.files[self.currentID])
			del self.files[self.currentID]
			self.getNextID()
		
	# This is called every single loop of the run method. Basically it checks to make sure no more images have
	# been added to the image folder (such as custom stickers from the website). While this isn't exactly perfect,
	# because it iterates through everything, I'm not entirely sure how to approach it in another less intensive fashion yet.
	# Maybe an MD5 hash of the directory, but hashing the directory is an expensive operation too.
	def checkFiles(self):
		for fileName in listdir(self.imageLocation):
			id = int(''.join(x for x in fileName if x.isdigit()))
			if(id not in self.files):
				self.files[id] = fileName

	# I realize it's nessesary, and the shortest way to do this, but it's still ugly and i hate it.
	# Basically, it just grabs the next image ID, with corner case handling.  
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

	def getPreviousID(self):
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
	
	# This loop is called by run, checks the different kinds of intput for stickerbot.
	# Currently the two buttons do the same exact thing, which is bad.
	# The idea is that the buttons will both be used to allow stickerbot to be more interactive.
	def checkInput(self):
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

	# This is the main loop of stickerbot. 
	# Running this method outside of a stickerbot object puts it in an indefinite loop.
	def run(self):
		writeLCD("Ready", Color.white)
		self.checkFiles()
		if len(list(self.files.viewkeys())) != 0:	
			self.currentID = int(list(self.files.viewkeys())[0])
		else:
			self.currentID = 0
		print "Pre-Loading: "+str(self.currentID)
		self.writeLCD("Please Insert $1",Color.white)
		while True:
			if self.currentID != 0:
				if (self.checkInput()):
					self.writeLCD("Please Insert $1",Color.white)
			else:
				self.writeLCD("Ready",Color.white)
				while len(list(self.files.viewkeys())) == 0:
					sleep(.5)
					self.checkFiles()
				self.getNextID()
				self.writeLCD("Image: "+self.currentID+"\nPlease Insert $1",Color.red)
			self.checkFiles()

	#This code is currently useless, but was intended originally to make setting the screen color easier.
	#Should probably be merged with code printing from the LCD.
	def writeLCD(self, inputText, color):
		if(color == Color.red):
			self.lcd.backlight(self.lcd.RED)
		if(color == Color.green):
			self.lcd.backlight(self.lcd.GREEN)
		if(color == Color.white):
			self.lcd.backlight(self.lcd.WHITE)
		if(color == Color.blue):
			self.lcd.backlight(self.lcd.BLUE)
		self.lcd.clear()
		self.lcd.message(inputText)

#If this is called instead of used as a class, we create an object and run it.
if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("-t","--test",action="store_true",
				help="enables test mode. This will turn verbosity up and disable printing")
	parser.add_argument("-v","--verbosity", 
				type=int, choices=[0, 1, 2, 3], help="turns up verbosity of the code. Will output more information")
	parser.add_argument("-s", "--stickerpack", 
				type=str, help="Pre-chose the sticker pack, pre-empting the menu when it starts")
	parser.add_argument("imageLocation", 
				help="The directory which image files will be dropped into")	
	parser.parse_args()
	printStickers = ScreenController(args.imageLocation)
	sleep(1)
	printStickers.run()
