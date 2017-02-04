import imScraperHelper
import json
import random
from datetime import datetime


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

def createSportObject(soup, sportTableIndex, startTimeSeconds, desktop=False) :
	print desktop
	sportObject = {}
	# sportObject["activity"] = sportName
	sportObject["splits"] = []
	runSoup = soup.find_all('table')[sportTableIndex]
	runSplits = list(runSoup.find_all('tr'))
	
	#for calculating average
	aggregatedTimeSeconds = 0
	aggregatedDistance = 0
	averageSoFar = 0
	latestRaceTimeStr = "--:--"
	latestEstimatedRaceTimeStr = "--:--"
	index = 0
	for i in range(1) :
		del runSplits[0]
	for tr in runSplits :
		tds = tr.find_all('td')
		split = {}
		split["totalDistance"] = tds[0].string.encode('ascii', 'ignore').replace('km', '').replace('mi', '')
		split["splitDistance"] = tds[1].string.replace('km', '').replace('mi','')
		split["splitTime"] = tds[2].string
		if desktop :
			split["pace"] = tds[4].string
			split["raceTime"] = tds[3].string
			print split
        else :
        	split["pace"] = tds[3].string
        	split["raceTime"] = tds[4].string        

		splitSeconds = convertStringTimeToSeconds(split["splitTime"])
		split["estimatedRaceTime"] = "--:--"
		split["estimatedTimeOfDay"] = "--:--"
		#Handle Total Row Differently
		totalDistance = split["totalDistance"]
		if split["totalDistance"] == "Total" :
			totalDistance = split["splitDistance"]
			splitSeconds = 0
		
		if splitSeconds > 0 :
			aggregatedDistance += float(split["splitDistance"])
			aggregatedTimeSeconds += splitSeconds
			averageSoFar = calculatePacePerHr(aggregatedDistance, aggregatedTimeSeconds)

		if aggregatedDistance > 0 :		
			split['activityElapsedTime'] = convertSecondsToTime(aggregatedTimeSeconds)
			split["estimatedTime"] = calculateEstimatedTime(totalDistance, averageSoFar)
			splitEstimatedSeconds = calculateEstimatedTime(split["splitDistance"], averageSoFar)
			split["splitEstimatedTime"] = splitEstimatedSeconds
			latestRaceTimeSec = convertStringTimeToSeconds(split["raceTime"])
			if index > 0 :
				latestRaceTimeSec = convertStringTimeToSeconds(latestRaceTimeStr)
				if latestRaceTimeSec == 0 :
					latestRaceTimeSec = convertStringTimeToSeconds(latestEstimatedRaceTimeStr)
				estimatedRaceTimeSec = latestRaceTimeSec + convertStringTimeToSeconds(splitEstimatedSeconds)
				split["estimatedRaceTime"] = convertSecondsToTime( estimatedRaceTimeSec )
				split["estimatedTimeOfDay"] = convertSecondsToTime(startTimeSeconds + estimatedRaceTimeSec)

			
			#if its the last one, 
			if split["totalDistance"] == "Total" :
				split["estimatedRaceTime"] = latestEstimatedRaceTimeStr
				split["estimatedTimeOfDay"] = latestEstimatedTimeOfDayStr
				


			# split["estimatedRaceTime"] = convertSecondsToTime(convertStringTimeToSeconds(latestRaceTime) \
			# 	+ convertStringTimeToSeconds(splitEstimatedSeconds))
		
		# print splitSeconds, totalDistance, aggregatedTimeSeconds, averageSoFar
		

		# print totalDistance, averageSoFar	
		# split["estimatedTime"] = calculateEstimatedTime(totalDistance, averageSoFar)
		latestRaceTimeStr = split["raceTime"]
		latestEstimatedRaceTimeStr = split["estimatedRaceTime"]
		latestEstimatedTimeOfDayStr = split["estimatedTimeOfDay"]
		sportObject['splits'].append(split)
		index += 1

	if aggregatedDistance > 0 :
		sportObject['averagePerHour'] = calculatePacePerHr(aggregatedDistance, aggregatedTimeSeconds)
		sportObject['perMinuteAverage'] = convertPerHourToMinPer(sportObject['averagePerHour'])

	return sportObject

def getTransitionData(soup, transitionIndex) :
	transitionSplits = list(soup.find_all('table')[transitionIndex].find_all('tr'))
	transitionData = {}
	transitionData['T1'] = transitionSplits[0].find_all('td')[1].string
	transitionData['T2'] = transitionSplits[1].find_all('td')[1].string
	return transitionData

def getLatestUpdate(allSports) :
	sports = ["swim","bike","run"]
	lastSplit = {}
	totalDistance = 0
	allSplits = []

	#first combine all splits into a single one
	priorSplitTime = ""
	for sport in sports :
		
		for sportSplit in allSports[sport]["splits"] :
			#next make sure the same time isn't there, don't need duplicates
			if sportSplit["raceTime"] != priorSplitTime :
				sportSplit["sport"] = sport
				allSplits.append(sportSplit)
			priorSplitTime = sportSplit["raceTime"]

	#print json.dumps(allSplits)
	return getLastNextSplit(allSplits)
	# print getLastNextSplit(allSplits)
	# print json.dumps(getLastNextSplit(allSplits), sort_keys=True, indent=4, separators=(',', ': '))


#find the "next" index, and also return the "latest"
def getLastNextSplit(allSplits) :
	lastNextSplit = { 'totalDistance': 0 }	
	for split in allSplits :
		lastNextSplit['next'] = split
		lastNextSplit['totalDistance'] += float(split['splitDistance'])
		if split["raceTime"] == '--:--' :
			return lastNextSplit
		lastNextSplit['previous'] = split

	#If here, then the race is finished, delete the "next" node
	lastNextSplit['next'] = {}
	return lastNextSplit

def getAthleteInfoDesktop(soup) :
    athleteInfo = {}
    athleteInfo["name"] = soup.h1.contents[1]
    athleteInfo["division"] = soup.find(text="Division").findNext('td').string
    athleteInfo["state"] = soup.find(text="State").findNext('td').string
    athleteInfo["country"] = soup.find(text="Country").findNext('td').string
    athleteInfo["profession"] = soup.find(text="Profession").findNext('td').string
    return athleteInfo
