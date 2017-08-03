import imScraperHelper
import json
import random
from datetime import datetime
import re
import sys

GETALLRACEDETAILS = True
CSVDIVIDER = '\t'

def createSportObjectNoPredictions(soup, sportName) :

	sportObject = {}
	# sportObject["activity"] = sportName
	sportObject["splits"] = []
	try : 
		runSoup = soup.find(text=re.compile(sportName)).findNext('table')
	except AttributeError :
		#no sport name found, return empty object
		return {}

	runSplits = list(runSoup.find_all('tr'))
	
	for i in range(1) :
		del runSplits[0]
	for tr in runSplits :
		tds = tr.find_all('td')
		split = {}
		split["totalDistance"] = tds[0].string.encode('ascii', 'ignore').replace('km', '').replace('mi', '')
		split["splitDistance"] = tds[1].string.replace('km', '').replace('mi','').replace(' ','')
		split["splitTime"] = cleanseTime(tds[2].string)
		split["pace"] = tds[4].string
		split["raceTime"] = cleanseTime(tds[3].string)
		
		sportObject['splits'].append(split)

	return sportObject

def getTransitionData(soup, transitionString) :
	transitionSplits = list(soup.find(text=re.compile(transitionString)).findNext('table').find_all('tr'))
	transitionData = {}

	# transitionData['T1'] = transitionSplits[0].find_all('td')[1].string
	# transitionData['T2'] = transitionSplits[1].find_all('td')[1].string
	transitionData['T1'] = cleanseTime(getNextDomValueAfterString(soup, 'T1:', 'td', False))
	transitionData['T2'] = cleanseTime(getNextDomValueAfterString(soup, 'T2:', 'td', False))
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

def getNextDomValueAfterString(soup, input, domType, exactMatch=True) :
	domElementSearchingFor = None
	if (exactMatch) :
		domElementSearchingFor = soup.find(text=input)
	else :
		domElementSearchingFor = soup.find(text=re.compile(input))
	if domElementSearchingFor != None :
		return domElementSearchingFor.findNext(domType).string
	else :
		return ''

def getAthleteInfoDesktop(soup) :
    athleteInfo = {}
    athleteInfo["name"] = getNextDomValueAfterString(soup, ' Back to Results', 'h1')
	# athleteInfo["name"] = soup.h1.contents[1]
	
    athleteInfo["division"] = getNextDomValueAfterString(soup, 'Division', 'td')
    athleteInfo["state"] = getNextDomValueAfterString(soup, 'State', 'td')
    athleteInfo["country"] = getNextDomValueAfterString(soup, 'Country', 'td')
    athleteInfo["profession"] = getNextDomValueAfterString(soup, 'Profession', 'td')
    return athleteInfo

def splitRankText(input) :
	rank = input.split(':')[1]
	rank = rank.replace(' ','')
	#for older cases like "2 OF 100"
	rank = rank.split('of')[0]
	rank = rank.replace("\\u00a0", " ")
	return rank

def getRaceSummary(soup) :
	raceSummary = {}
	raceSummary['swim'] = cleanseTime(getNextDomValueAfterString(soup, 'Swim:', 'td'))
	raceSummary['bike'] = cleanseTime(getNextDomValueAfterString(soup, 'Bike', 'td'))
	raceSummary['run'] = cleanseTime(getNextDomValueAfterString(soup, 'Run', 'td'))
	raceSummary['overall'] = getNextDomValueAfterString(soup, 'Overall', 'td')
	raceSummary['completed'] = determineCompletedStatus(raceSummary['overall'])
	return raceSummary

def determineCompletedStatus(overallTime) :
	if (overallTime == '--:--') :
		return False
	return True	

def determineDistanceOfRace(raceTitle) :
	distance = 140.6
	if ("70.3" in raceTitle) :
		distance = 70.3
	elif ("5150" in raceTitle) :
		distance = 32.2
	return distance


def getRanking(soup) :
	ranking = {}
	# NOTE - yes this is backwards, but that is how Ironman has it set up...
	ranking['overall'] = splitRankText(soup.select('#div-rank')[0].get_text())
	ranking['division'] = splitRankText(soup.select('#rank')[0].get_text())
	return ranking

def getRaceData(url) :
	soup = imScraperHelper.createSoup(url)

	allSports = {}
	try :
		allSports["athlete"] = getAthleteInfoDesktop(soup)
		allSports["raceSummary"] = getRaceSummary(soup)
		# allSports["raceSummarySeconds"] = getRaceSummarySecondsNode(allSports["raceSummary"])
		allSports["raceSummaryHours"] = getRaceSummaryHoursNode(allSports["raceSummary"])
		allSports["ranking"] = getRanking(soup)
		
		#GOING TO SKIP ADDING THE RACE DETAILS EXCEPT FOR SPECIFIC RACES
		if (GETALLRACEDETAILS) :
			raceDetails = {}
			raceDetails["swim"] = createSportObjectNoPredictions(soup, 'SWIM DETAILS')
			raceDetails["bike"] = createSportObjectNoPredictions(soup, 'BIKE DETAILS')
			raceDetails["run"] = createSportObjectNoPredictions(soup, 'RUN DETAILS')
			raceDetails["transition"] = getTransitionData(soup, 'Transition Details')
			allSports['raceDetails'] = raceDetails

	except: 
		#ignore errors
		print "COULD NOT LOAD URL: " + str(url), sys.exc_info() 
		
	return allSports	


def getRaceSummarySecondsNode(raceSummaryNode) :
	
	raceSummarySeconds = {}
	overallSeconds = convertTimeToSeconds(raceSummaryNode['overall'])
	
	#create a new node under the raceSummary for just the seconds amount
	if (overallSeconds > 0) :
		raceSummarySeconds = {
			'overall': overallSeconds,
			'swim': convertTimeToSeconds(raceSummaryNode['swim']),
			'bike': convertTimeToSeconds(raceSummaryNode['bike']),
			'run': convertTimeToSeconds(raceSummaryNode['run'])
		}
	return raceSummarySeconds	

def convertTimeToSeconds(stringTime) :
    #check to see if there is an actual time or --:--
    
    if (stringTime.find('--') >= 0) :
        return 0
    splitTime = stringTime.split(':')
    if len(splitTime) == 2 :
        splitTime.insert(0, '0')
    secondsTime = 3600 * int(splitTime[0]) + 60 * int(splitTime[1]) + int(splitTime[2])
    return secondsTime

def cleanseTime(stringTime) :
	if (stringTime is None) :
		return stringTime
		
	splitTime = stringTime.split(':')
	if len(splitTime) == 2 :
		splitTime.insert(0, '0')
		return ':'.join(splitTime)
	return stringTime

def getRaceSummaryHoursNode(raceSummaryNode) :
	
	raceSummaryHours = {}
	overallHours = convertTimeToHours(raceSummaryNode['overall'])
	
	#create a new node under the raceSummary for just the Hours amount
	if (overallHours > 0) :
		raceSummaryHours = {
			'overall': overallHours,
			'swim': convertTimeToHours(raceSummaryNode['swim']),
			'bike': convertTimeToHours(raceSummaryNode['bike']),
			'run': convertTimeToHours(raceSummaryNode['run'])
		}
	return raceSummaryHours

def convertTimeToHours(stringTime) :
    #check to see if there is an actual time or --:--
    
    if (stringTime == '' or stringTime.find('--') >= 0 or stringTime.find('Summary') >= 0) :
        return None
    splitTime = stringTime.split(':')
    if len(splitTime) == 2 :
        splitTime.insert(0, '0')
    hoursTime = int(splitTime[0]) + float(splitTime[1])/60 + float(splitTime[2])/3600
    return hoursTime

def createCsvHeaderLine() :
	headers = ["YEAR", "BIB", "NAME", "STATE", "DIVISION", "TOTAL TIME", "SWIM", "T1", "BIKE", "T2", "RUN"]
	return CSVDIVIDER.join(headers)

def emptyValIfNull(inputValue) :
	if not inputValue :
		return ''
	else :
		return inputValue

def createCsvFriendlyFormat(athleteInfo) :
	line = []
	#athlete info - bib, name, state, division
	line.extend( [athleteInfo['raceInfo']['year'], athleteInfo['raceInfo']['bib'], athleteInfo['athlete']['name'], athleteInfo['athlete']['state'], athleteInfo['athlete']['division']] )
	
	#raceSummaryInfo - total time, swim, bike, run, t1, t2
	line.extend([athleteInfo['raceSummary']['overall'], athleteInfo['raceSummary']['swim'], athleteInfo['raceDetails']['transition']['T1'], athleteInfo['raceSummary']['bike'], athleteInfo['raceDetails']['transition']['T2'], athleteInfo['raceSummary']['run'] ])
	# line.extend([athleteInfo['raceSummary']['overall'], athleteInfo['raceSummary']['swim'],  athleteInfo['raceSummary']['bike'],  athleteInfo['raceSummary']['run'] ])

	#ranking - division / overall

	#full splits - swim, bike, run
	
	if 'raceDetails' in athleteInfo :
		sports = ['swim', 'bike', 'run']
		for sport in sports :
			if 'splits' in athleteInfo['raceDetails'][sport] :
				for split in athleteInfo['raceDetails'][sport]['splits'] :
					line.append(emptyValIfNull(split['splitDistance']))
					line.append(emptyValIfNull(split['splitTime']))
					line.append(emptyValIfNull(split['pace']))

	return CSVDIVIDER.join(line)