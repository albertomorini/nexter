import requests
import re

########################
# make the query
#return info of a single tv show
def getInfo(nameShow):
	#remove points and punctuaction that can bring us wrong results
	info = re.sub('[^A-Za-z0-9]+', '-', nameShow)
	info = requests.get('https://api.tvmaze.com/singlesearch/shows?q='+nameShow)
	info = info.json()
	return info

#return an array with all the tv shows that match the name provided.
def getShowsResults(nameShow):
	info = re.sub('[^A-Za-z0-9]+', ' ', nameShow)
	info = requests.get("https://api.tvmaze.com/search/shows?q="+nameShow)
	info = info.json()
	return info


########################
#single episode

#return the title of a single episode
def getTitleEpisode(info, season, numberEpisode):
	try:
		url ='https://api.tvmaze.com/shows/'+str(info.get("id"))+'/episodebynumber?season='+season+'&number='+str(numberEpisode)
		title = requests.get(url)
		return title.json().get("name")
	except Exception as e:
		return "info not found"

#return minutes of the duration of the episode
def getRuntimeEpisode(info, season, numberEpisode):
	try:
		url ='https://api.tvmaze.com/shows/'+str(info.get("id"))+'/episodebynumber?season='+season+'&number='+str(numberEpisode)
		title = requests.get(url)
		return title.json().get("runtime")
	except Exception as e:
		return "info not found"

def getSummaryEpisode(info,season,numberEpisode):
	try:
		url ='https://api.tvmaze.com/shows/'+str(info.get("id"))+'/episodebynumber?season='+season+'&number='+str(numberEpisode)
		title = requests.get(url)
		return title.json().get("summary")
	except Exception as e:
		return "info not found"

##############################

#return the date of the next episode
def getNextEpisode(info):
	try:
		nextEpisodeLink = info.get("_links").get("nextepisode").get("href")
		nextEpisode = requests.get(nextEpisodeLink).json().get("airdate")
		if (nextEpisode != None):
			return nextEpisode
	except Exception as e:
		return "No info yet"

#return the date of the last episode
def getDateLastEpisode(info):
	seasons= requests.get('https://api.tvmaze.com/shows/'+str(info.get("id"))+"/seasons")
	seasons = seasons.json()
	lastEpisode=""
	#we have to get the greatest date, not the date of the last episode (it couldn't be determined yet)
	for i in range(0,len(seasons)):
		if(seasons[i].get("endDate"))!=None:
			lastEpisode=seasons[i].get("endDate")

	return str(lastEpisode)

#return the number of seasons
def getNumberOfSeasons(info):
	seasons= requests.get('https://api.tvmaze.com/shows/'+str(info.get("id"))+"/seasons")
	seasons = seasons.json()
	return str(len(seasons))

#return the status (still running or termined or something)
def getStatus(info):
	return info.get("status")

#return the generes
def getGenres(info):
	return info.get("genres")

def getRating(info):
	return str(info.get("rating").get("average"))

def getLinkImage(info):
	return info.get("image").get("medium")

def getSummary(info):
	return info.get("summary")

def getUrlImage(info):
	return info.get("image").get("original")

#return an emoji related to the genere
def getEmojiByGenre(info):
	genre = getGenres(info)
	strRes =""
	if ("Drama" in genre):
		strRes += "🎭"
	if("Action" in genre):
		strRes +="🔥"
	if("Crime" in genre):
		strRes +="🔪"
	if("Comedy" in genre):
		strRes +="😂"
	if("Romance" in genre):
		strRes +="🫀"
	if("Science-Fiction" in genre):
		strRes +="🧪👀"

	return strRes

#return the title of the tv show
def getName(info):
	return info.get("name")+getEmojiByGenre(info)
