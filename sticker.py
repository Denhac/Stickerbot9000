 #!/usr/bin/python2

from hashlib import md5

class sticker:

	imageLocation = ""
	printCount = 0
	deleteable = False
	md5 = ""
	
	def __init__(self, imageLocation, deletable = True, printCount = 0):
		self.imageLocation = imageLocation
		self.deletable = deletable
		self.printCount = printCount
		md5Generator = hashlib.md5()
		md5 = md5Generator.update(open(imageLocation).read).digest()
 
	def addPrint(self):
		self.printCount += 1	

	def getDeletable(self):
		return self.deletable

	def duplicateFile(self,fileLocation):
		md5Generator = hashlib.md5()
		if md5 == md5Generator.update(open(fileLocation).read).digest():
			return true
		else:
			return false
		
	
