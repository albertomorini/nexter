# Nexter a simply tv tracker.

Nexter scans your TvShows's directory and for each folder it will search on <a href="https://tvmaze.com>">TvMaze</a> the info related.

It will also count how seasons you have of the all seasons that exists of that show.


**Attention:** I assume a good structure of your media library, like Kodi/Plex does where in the TvShows there is a single folder for each Show and inside this there is a single folder for each season.
**Example**
>
	TvSeries/
		Euphoria/
			Extras/
				Episode1.mkv
				Episode2.mkv
			Season1/
				Episode1.mkv
				...
				Episode8.mkv
		Dexter/
			Season1/
				...
			...
			Season8/
		...

## Dependencies:
I use my python utility file "+utility/python_utility.py", you can find it on the parent of this folder.

## Usage
`$ python3 tvTracker.py`

* option 1: show all tv series
* option 2: print just the running tv shows
* option 3: create an .ics file for each tv show having the date of the next episode, you have to manually open these file with calendar (iCloud) to create the events.


**Warning:** I print some emoji on terminal, this could cause some problems if you doesn't have any emoji pack installed.
on MacOS are installed by default, didn't tried on other os sorry.

## Output be like:

![Output example](https://github.com/albertomorini/nexter/blob/main/imgExample/example.png)

### Calendar's event output:

![Output example](https://github.com/albertomorini/nexter/blob/main/imgExample/1.png)
![Output example](https://github.com/albertomorini/nexter/blob/main/imgExample/2.png)
