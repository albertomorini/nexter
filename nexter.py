from icalendar import Calendar, Event, vCalAddress, vText
import pytz
from datetime import datetime
from pathlib import Path
import tvMazeAPI
import os
import sys
import json

### Utility

def serializeJSON(dir, filename, dataDictionary):
	with open(dir+"/"+filename,"a", encoding='utf-8') as fileToStore:
   		json.dump(dataDictionary, fileToStore, ensure_ascii=False)

def readJson(path):
	with open(path) as dataStored:
		return json.load(dataStored)

def doMD5(digest):
	return hashlib.md5(digest.encode()).hexdigest()
# PRINTING STUFF

## print the info of a show
# @param nameofshow [string] the name of the show (makes key into the dataset)
# @param show [Object] the show we'd like to print
def printData(nameofshow, show):
	print(nameofshow+"("+show.get("rating") +")") #name of series and the rating
	print("\t#Seasons: "+show.get("seasons")+" - (and "+show.get("seasonOwned")+" owned)")
	print("\tStatus: "+show.get("status"))
	print("\tDate of last episode: "+show.get("lastEpisodeDate"))
	print("\tNext episode: "+show.get("nextEpisode"))
	print("_____________________")

## apply a fielter on printing list
def filterPrinting(dictShows,justRunning=False):
	for i in dictShows:
		if(justRunning and dictShows[i].get("status")=="Running"): ## only the shows in status running
			printData(i,dictShows[i])			
		elif(not justRunning and dictShows[i].get("founded")): ## all the shows
			printData(i,dictShows[i])			
		elif(not dictShows[i].get("founded")):
			print("SHOWS NOT FOUND: "+i)
			print("_____________________")


#############################################
# CALENDAR STUFF

# create an ics event
# @nameShow [string] the name of the show (title of the event)
# @dateNextEpisode [string] date of the next episode
# return the path of the ics file
def createCalendarEvent(nameShow, dateNextEpisode):

	event = Event()
	event.add('summary', nameShow) #tv show's title
	dateTMP = dateNextEpisode.split("-") # get just the date

	# create the event that will be in the evening 21-22.
	event.add('dtstart', datetime(int(dateTMP[0]), int(dateTMP[1]), int(dateTMP[2]),21, 0, 0, tzinfo=pytz.utc))
	event.add('dtend', datetime(int(dateTMP[0]), int(dateTMP[1]), int(dateTMP[2]), 22, 0, 0, tzinfo=pytz.utc))
	event.add('dtstamp', datetime(int(dateTMP[0]), int(dateTMP[1]), int(dateTMP[2]), 0, 0, 0, tzinfo=pytz.utc))

	outputPath=os.path.join("./events/", doMD5(nameShow)+'.ics') #store the event as ics (hash of the tvshow title)

	# Adding events to calendar
	cal = Calendar()
	cal.add_component(event)
	#store the ics file
	f = open(outputPath, 'wb')
	f.write(cal.to_ical())
	f.close()
	return outputPath 


# create the ics event and opens with default calendar app
def updateCalender(dictShows):
	for x in dictShows:
		if(dictShows[x].get("founded")== True and dictShows[x].get("nextEpisode") != "No info yet" ):
			outputPath = createCalendarEvent(x, dictShows[x].get("nextEpisode"))
			# event created, try to open with default calendar
			if(platform.system()=="Darwin"):
				os.system("open "+str(outputPath))
				os.remove(outputPath) #remove the event once opened in the calendar
			elif(platform.system()=="Windows"):
				pass #TODO: I really don't know windows


########################################################
# return the number of the seasons owned on disk
def getNumSeasonOwned(path,show):
	return str(len(next(os.walk(path+"/"+show))[1]))

#create shows dict.
#@path [string] of the tvshows path
def getNews(path):
	dictShows = {}
	tvShows = next(os.walk(path))[1]

	for i in tvShows:
		info = i.split("(")[0] #remove stuff like year that could bring us different results
		info = tvMazeAPI.getInfo(info)
		if(info != None):
			dictShows[tvMazeAPI.getName(info)]={
				"founded":True,
				"status": tvMazeAPI.getStatus(info),
				"lastEpisodeDate": tvMazeAPI.getDateLastEpisode(info),
				"nextEpisode":tvMazeAPI.getNextEpisode(info),
				"seasons":tvMazeAPI.getNumberOfSeasons(info),
				"seasonOwned":getNumSeasonOwned(path,i),
				"rating":tvMazeAPI.getRating(info)
			}
		else:
			dictShows[i]={"founded":False}

	return dictShows

###############################################################

# allows the user to insert the root path of the tvshows dir
def insertRootPath():
	isValid=False
	rootPath = ""
	while(not isValid and rootPath!="q"):
		rootPath = input("Insert the root directory: ")
		if os.path.exists(rootPath): # directory doesn't exists
			try:
				if(os.chdir(rootPath)==None): # can't access to the folder, missing permission
					isValid=True
			except PermissionError:
				print ("Access tenied to:", rootPath)
		else:
			print("Path doesn't exists, retry (or insert 'q' to quit)")

	return rootPath

def menu():
	path=""
	#check if mode is passed as argument
	if(len(sys.argv)>1):
		path=sys.argv[1] #path
		x= int(sys.argv[2]) #mode
	else:
		path=insertRootPath()
		print("Welcome!\n"+" 1) fetch all shows\n 2) the news only of the running series\n 3) create iCloud events for new episodes")
		x = int(input("Enter your choice: "))

	## get the news and store it into a report
	news = getNews(path)
	serializeJSON("./","tvShowsReport.json",news)
	if(x==1):
		filterPrinting(news)
	elif(x==2): #just running
		filterPrinting(news,True) 
	elif(x==3):
		updateCalender(news)

menu()
