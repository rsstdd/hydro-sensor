
#!/usr/bin/python
# once a minute time lapse photo taker
# 22 April 16 - MCK
#
# Version 1.03
# 26 April	- moved counter to counter.py
# Version 2.08
# 8 May 	- rebuild counter file when missing

VERSION = "0.2.2"

import os
import time
import datetime
import socket
from pymongo import MongoClient
import gridfs


# setup paths

mypath=os.path.abspath(__file__)       # Find the full path of this python script
baseDir=mypath[0:mypath.rfind("/")+1]  # get the path location only
baseFileName=mypath[mypath.rfind("/")+1:mypath.rfind(".")]
progName = os.path.basename(__file__)
datePath=str(datetime.date.today())


#-----------------------------------------------------------------------------------------------
def showTime():
	rightNow = datetime.datetime.utcnow()
	currentTime = "%04d%02d%02d_%02d:%02d:%02d" % (rightNow.year, rightNow.month, rightNow.day, rightNow.hour, rightNow.minute, rightNow.second)
	return currentTime





#-----------------------------------------------------------------------------------------------
def showMessage(functionName, messageStr):
	now = showTime()
	print ("%s %s - %s " % (now, functionName, messageStr))
	return






# Check for variable file to import and error out if not found.
configFilePath = baseDir + "config.py"
if not os.path.isfile(configFilePath):
	msgStr = "ERROR - Missing config.py file - Could not find Configuration file %s"%(configFilePath)

	showMessage("readConfigFile", msgStr)
	quit()
else:
	# Read Configuration variables from config.py file
	from config import *


timelapsePath = baseDir + timelapseDir

# Check for counter file to import and error out if not found.
counter = 999999		#default if not defined in counter.py
maxCounter=1000000
counterFilePath = baseDir + "counter.py"
if not os.path.isfile(counterFilePath):
	msgStr = "ERROR - Missing counter.py file - Could not find Configuration file %s"%(counterFilePath)

	showMessage("readCounterFile", msgStr)
	filedata = None

	filedata = "# counter\ncounter = 1\nmaxCounter=1000000"
	# Write the file out again
	with open(counterFilePath, 'w') as file:
	  file.write(filedata)


else:
	# Read Configuration variables from counter.py file
	from counter import *

if counter == 999999:
	filedata = "# counter\ncounter = 1\nmaxCounter=1000000"
		# Write the file out again
	with open(counterFilePath, 'w') as file:
		file.write(filedata)



# check for dir

if not os.path.isdir(timelapsePath+"/"+datePath):
	msgStr = "Creating Time Lapse Image Storage Folder" + timelapsePath+"/"+datePath
	showMessage ("checkImagePath", msgStr)
	os.makedirs(timelapsePath+"/"+datePath)




# take pic


picFilename=timelapsePath+"/"+datePath+ "/" + imagePrefix + str(counter).zfill(len(str(maxCounter))) + ".jpg"
command ="raspistill -q 100 -o " + picFilename + picOptions + localPicOptions+ " 2>&1 | logger"
msgStr = "Executing "+command
showMessage("getpic", msgStr)
os.system(command)

#try :
#	client=MongoClient("10.9.0.1")
#	db=client.solstice_gr1_gridfs
#	fs=gridfs.GridFS(db)
#	picfile	=open(picFilename,'rb')
#	file_id	=fs.put(picfile.read(),origtime=os.path.getmtime(picFilename),filename=picFilename)
#except:
#	pass

# upload pic
#command = baseDir+"gpush.sh "+picFilename+" 2>&1 | logger"
#msgStr = "Executing "+command
#showMessage("getpic", msgStr)
#os.system(command)




# update counter

oldCounter=counter
counter += 1

if counter > maxCounter :
	counter = 1

# Read in the file
filedata = None


with open(counterFilePath, 'r') as file :
	filedata = file.read()

# Replace the target string
filedata = filedata.replace('counter = '+str(oldCounter), 'counter = '+str(counter))

# Write the file out again
with open(counterFilePath, 'w') as file:
	file.write(filedata)


# sync old pics

command="cd /home/thoth/timelapse && sudo python "+baseDir+" gsync2.py "+timelapsePath+"/"+datePath+" 2>&1 | logger"
msgStr = "Executing "+command
showMessage("getpic2", msgStr)
os.system(command)
