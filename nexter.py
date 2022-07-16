from icalendar import Calendar, Event, vCalAddress, vText
import pytz
from datetime import datetime
from pathlib import Path
import tvMazeAPI
import os
import sys
sys.path.insert(0, '../+utility/')
import python_utility as pyut

##########################################
#printing
def printNewsTerminal(dictShows):
	for i in dictShows:
		if(dictShows[i].get("founded")):
			print(i + "("+dictShows[i].get("rating") +")") #name of series and the rating

			print("\t#Seasons: "+dictShows[i].get("seasons")+" - (and "+dictShows[i].get("seasonOwned")+" owned)")
			print("\tStatus: "+dictShows[i].get("status"))

			print("\tDate of last episode: "+dictShows[i].get("lastEpisodeDate"))
			print("\tNext episode: "+dictShows[i].get("nextEpisode"))
			print("_____________________")
		else:
			print("SHOWS NOT FOUND: "+i)
			print("_____________________")

def printRunningSeries(dictShows):
	for i in dictShows:
		if(dictShows[i].get("founded") and dictShows[i].get("status")=="Running"):
			print(i + "("+dictShows[i].get("rating") +")") #name of series and the rating
			print("\t#Seasons: "+dictShows[i].get("seasons")+" - (and "+dictShows[i].get("seasonOwned")+" owned)")
			print("\tDate of last episode: "+dictShows[i].get("lastEpisodeDate"))
			print("\tNext episode: "+dictShows[i].get("nextEpisode"))
			print("_____________________")


#############################################
#create calendar events (ics ~ iCal)

def createiCloudEvents(nameShow, dateNextEpisode):

	cal = Calendar()
	#cal.add('attendee', 'MAILTO:abc@example.com')

	event = Event()
	event.add('summary', nameShow) #tv show's title
	dateTMP = dateNextEpisode.split("-")
	print()
	event.add('dtstart', datetime(int(dateTMP[0]), int(dateTMP[1]), int(dateTMP[2]),21, 0, 0, tzinfo=pytz.utc))
	event.add('dtend', datetime(int(dateTMP[0]), int(dateTMP[1]), int(dateTMP[2]), 22, 0, 0, tzinfo=pytz.utc))
	event.add('dtstamp', datetime(int(dateTMP[0]), int(dateTMP[1]), int(dateTMP[2]), 0, 0, 0, tzinfo=pytz.utc))

	# Adding events to calendar
	cal.add_component(event)

	directory = str(Path(__file__).parent.parent) + "/events/"
	f = open(os.path.join(directory, nameShow+'.ics'), 'wb')
	f.write(cal.to_ical())
	f.close()

def processJSONToCalendar(dictShows):

	for x in dictShows:
		if(dictShows[x].get("founded")== True and dictShows[x].get("nextEpisode") != "No info yet" ):
			createiCloudEvents(x, dictShows[x].get("nextEpisode"))
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

	print("Welcome!\n"+" 1) fetch all shows\n 2) the news only of the running series\n 3) create iCloud events for new episodes")
	x = input("Enter your choice: ")
	x = int(x)
	res = getNews(path)
	pyut.serialize_JSON(".","tvShowsReport.json",res)
	if(x==1):
		printNewsTerminal(res)
	elif(x==2):
		printRunningSeries(res)
	elif(x==3):
		processJSONToCalendar(res)




menu("/Volumes/Media/TvShows")
