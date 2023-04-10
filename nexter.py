from icalendar import Calendar, Event, vCalAddress, vText
import pytz
from datetime import datetime
from pathlib import Path
import tvMazeAPI
import os
import sys
import platform 

import python_utility as pyut

##########################################
#printing
def printData(show):
	print(i + "("+show.get("rating") +")") #name of series and the rating

	print("\t#Seasons: "+show.get("seasons")+" - (and "+show.get("seasonOwned")+" owned)")
	print("\tStatus: "+show.get("status"))

	print("\tDate of last episode: "+show.get("lastEpisodeDate"))
	print("\tNext episode: "+show.get("nextEpisode"))
	print("_____________________")

def filterPrinting(dictShows,justRunning=False):
	for i in dictShows:
		if(justRunning and dictShows[i].get("status")=="Running"):
			printData(dictShows[i])			
		elif(not justRunning and dictShows[i].get("founded")):
			printData(dictShows[i])			
		elif(not dictShows[i].get("founded")):
			print("SHOWS NOT FOUND: "+i)
			print("_____________________")


#############################################
#create calendar events (ics ~ iCal)

def createiCloudEvents(nameShow, dateNextEpisode):

	cal = Calendar()

	event = Event()
	event.add('summary', nameShow) #tv show's title
	dateTMP = dateNextEpisode.split("-")
	print()
	event.add('dtstart', datetime(int(dateTMP[0]), int(dateTMP[1]), int(dateTMP[2]),21, 0, 0, tzinfo=pytz.utc))
	event.add('dtend', datetime(int(dateTMP[0]), int(dateTMP[1]), int(dateTMP[2]), 22, 0, 0, tzinfo=pytz.utc))
	event.add('dtstamp', datetime(int(dateTMP[0]), int(dateTMP[1]), int(dateTMP[2]), 0, 0, 0, tzinfo=pytz.utc))

	# TODO: a better way to store into filesysyem.. like save the hash of the name of the show
	outputPath=os.path.join("./events/", nameShow.replace(" ","").replace("&","-")+'.ics') #replace white space for a easier managemeent on file system 
	# Adding events to calendar
	cal.add_component(event)
	f = open(outputPath, 'wb')
	f.write(cal.to_ical())
	f.close()
	return outputPath

def processJSONToCalendar(dictShows):

	for x in dictShows:
		if(dictShows[x].get("founded")== True and dictShows[x].get("nextEpisode") != "No info yet" ):
			outputPath = createiCloudEvents(x, dictShows[x].get("nextEpisode"))
			# event created, try to open with default calendar
			if(platform.system()=="Darwin"):
				os.system("open "+str(outputPath))
			elif(platform.system()=="Windows"):
				pass # I really don't know windows
			print("Show: "+x + " on: "+ dictShows[x].get("nextEpisode"))
	print("\n --Events created on /events/ subfolder--")

########################################################
def getNumSeasonOwned(path,show):
	return str(len(next(os.walk(path+"/"+show))[1]))

#create shows dict.
#@path string of the tvshows path
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
def menu(path):

	#check if mode is passed as argument
	if(len(sys.argv)>1):
		x= int(sys.argv[1])
	else:
		print("Welcome!\n"+" 1) fetch all shows\n 2) the news only of the running series\n 3) create iCloud events for new episodes")
		x = input("Enter your choice: ")
		x = int(x)

	res = getNews(path)
	pyut.serialize_JSON(".","tvShowsReport.json",res)
	if(x==1):
		filterPrinting(res)
	elif(x==2):
		filterPrinting(res,True)
	elif(x==3):
		processJSONToCalendar(res)

menu("/Volumes/Media/TvShows")
