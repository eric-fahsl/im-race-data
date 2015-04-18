from bs4 import BeautifulSoup
import urllib
# import xmlHelper
import json
import random

##RUN SECTION
# sectionIndex = xmlHelper.searchContentForTag("RUN DETAILS", "", "", "", str(soup), 0)[1]

# distanceResult = xmlHelper.searchContentForTag("km", "", "<td>", "</td>", str(soup), sectionIndex)
# distanceTime = xmlHelper.searchContentForTag("km", "", "<td>","</td", str(soup), distanceResult[1])
# sectionIndex = distanceTime[1]
# print [distanceResult[0], distanceTime[0], sectionIndex]

# xmlHelper.searchContentForTag("km", "km", "<td>", "</td>", str(soup), 19534)

# distanceUnit = "km"

def createSoup(url) :
	#snowUrl = "http://www.snow-forecast.com/resorts/White-Pass/feed.xml"
	snowPage = urllib.urlopen(url)
	soup = BeautifulSoup(snowPage)
	return soup

def convertStringTimeToSeconds(stringTime) :
	#First check if it is empty, ie --:--
	if stringTime[0] == "-" :
		return 0
	times = stringTime.split(':')
	seconds = 0
	if len(times) > 2 :
		seconds = 3600*int(times[0]) + 60*int(times[1]) + int(times[2])
	else :
		seconds = 60*int(times[0]) + int(times[1])
	return int(seconds)

def convertSecondsToTime(seconds) :
	seconds = int(round(seconds, 0))
	hours = seconds / 3600
	minutes = format((seconds / 60) % 60, '02d')
	sec = format(seconds % 60, '02d')
	convertedTime = minutes + ":" + sec
	if hours > 0 :
		convertedTime = str(hours) + ":" + convertedTime
	return convertedTime

def calculatePacePerHr(distance, seconds) :
	if seconds == 0 :
		return 0
	hours = seconds / 3600.0
	pace = distance/hours
	return round(pace, 2)

def convertPerHourToMinPer(mph) :
	secPerPace = 3600.0 / mph
	return convertSecondsToTime(secPerPace)

def calculateEstimatedTime(distance, pace) :
	if pace == 0 :
		return convertSecondsToTime(0)
	estimatedHours = float(distance) / pace
	estimatedSeconds = estimatedHours * 3600
	return convertSecondsToTime(estimatedSeconds)

def createSportObject(soup, sportTableIndex, totalTime=[0]) :

	sportObject = {}
	# sportObject["activity"] = sportName
	sportObject["splits"] = []
	runSoup = soup.find_all('table')[sportTableIndex]
	runSplits = list(runSoup.find_all('tr'))
	
	#for calculating average
	aggregatedTimeSeconds = 0
	aggregatedDistance = 0
	averageSoFar = 0
	latestRaceTime = "--:--"
	for i in range(2) :
		del runSplits[0]
	for tr in runSplits :
		tds = tr.find_all('td')
		split = {}
		split["totalDistance"] = tds[0].string.encode('ascii', 'ignore').replace('km', '').replace('mi', '')
		split["splitDistance"] = tds[1].string.replace('km', '').replace('mi','')
		split["splitTime"] = tds[2].string
		split["pace"] = tds[3].string
		split["raceTime"] = tds[4].string

		splitSeconds = convertStringTimeToSeconds(split["splitTime"])

		#Handle Total Row Differently
		totalDistance = split["totalDistance"]
		if split["totalDistance"] == "Total" :
			totalDistance = split["splitDistance"]
			splitSeconds = 0
		
		if splitSeconds > 0 :
			aggregatedDistance += float(split["splitDistance"])
			aggregatedTimeSeconds += splitSeconds
			totalTime[0] += splitSeconds
			averageSoFar = calculatePacePerHr(aggregatedDistance, aggregatedTimeSeconds)			

		if aggregatedDistance > 0 :		
			split['activityElapsedTime'] = convertSecondsToTime(aggregatedTimeSeconds)
			split["estimatedTime"] = calculateEstimatedTime(totalDistance, averageSoFar)
			splitEstimatedSeconds = calculateEstimatedTime(split["splitDistance"], averageSoFar)
			split["splitEstimatedTime"] = splitEstimatedSeconds
			split["overallEstimatedTime"] = convertSecondsToTime(totalTime[0])
			split["estimatedRaceTime"] = convertSecondsToTime(convertStringTimeToSeconds(latestRaceTime) \
				+ convertStringTimeToSeconds(splitEstimatedSeconds))
		
		# print splitSeconds, totalDistance, aggregatedTimeSeconds, averageSoFar
		

		# print totalDistance, averageSoFar	
		# split["estimatedTime"] = calculateEstimatedTime(totalDistance, averageSoFar)
		latestRaceTime = split["raceTime"]
		sportObject['splits'].append(split)

	if aggregatedDistance > 0 :
		sportObject['averagePerHour'] = calculatePacePerHr(aggregatedDistance, aggregatedTimeSeconds)
		sportObject['perMinuteAverage'] = convertPerHourToMinPer(sportObject['averagePerHour'])

	return sportObject

def getTransitionData(soup, transitionIndex, totalTime=[0]) :
	transitionSplits = list(soup.find_all('table')[transitionIndex].find_all('tr'))
	transitionData = {}
	transitionData['T1'] = transitionSplits[0].find_all('td')[1].string
	transitionData['T2'] = transitionSplits[1].find_all('td')[1].string
	totalTransitionTime = 0
	totalTransitionTime += convertStringTimeToSeconds(transitionData['T1'])
	totalTransitionTime += convertStringTimeToSeconds(transitionData['T2'])
	totalTime[0] += totalTransitionTime
	return transitionData

# RACE_ID = "2278373444"
RACE_ID="20150412"
RACE = "taiwan"
# BIB = 443
BIB=1571

# url = "http://tracking.ironmanlive.com/mobilesearch.php?rid=2278373444&race=taiwan&y=2015&athlete=559#axzz3X0O9WgL1"
url = "http://tracking.ironmanlive.com/mobilesearch.php?rid=" + RACE_ID + "&race=" + RACE + "&y=2015&athlete=" + str(BIB) + "#axzz3X0O9WgL1"
url = "http://tracking.ironmanlive.com/mobileathlete.php?rid=2147483676&race=florida70.3&bib=1571&v=3.0&beta=&1428859800#axzz3X6WZscVO"
print url

# soup = xmlHelper.createSoup(url)
# soup = BeautifulSoup(open("testdata/IMTW-bike-run.html"))
soup = BeautifulSoup(open("testdata/IMTW-bike.html"))

totalTime = [ 0 ]
allSports = {}
allSports["name"] = soup.h1.string
allSports["transition"] = getTransitionData(soup, 5, totalTime)
allSports["swim"] = createSportObject(soup, 2, totalTime)
allSports["bike"] = createSportObject(soup, 3, totalTime)
allSports["run"] = createSportObject(soup, 4, totalTime)


print json.dumps(allSports, sort_keys=True, indent=4, separators=(',', ': '))

# print calculatePacePerHr(30, convertStringTimeToSeconds('1:03:10'))