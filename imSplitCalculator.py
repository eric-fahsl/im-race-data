import imScraperHelper
import json
import random
from datetime import datetime
import re
import sys

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
		split["splitTime"] = tds[2].string
		split["pace"] = tds[4].string
		split["raceTime"] = tds[3].string
		
		sportObject['splits'].append(split)

	return sportObject

def getTransitionData(soup, transitionString) :
	transitionSplits = list(soup.find(text=re.compile(transitionString)).findNext('table').find_all('tr'))
	transitionData = {}

	# transitionData['T1'] = transitionSplits[0].find_all('td')[1].string
	# transitionData['T2'] = transitionSplits[1].find_all('td')[1].string
	transitionData['T1'] = getNextDomValueAfterString(soup, 'T1:', 'td', False)
	transitionData['T2'] = getNextDomValueAfterString(soup, 'T2:', 'td', False)
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
    athleteInfo["name"] = soup.h1.contents[1]
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
	raceSummary['swim'] = getNextDomValueAfterString(soup, 'Swim:', 'td')
	raceSummary['bike'] = getNextDomValueAfterString(soup, 'Bike', 'td')
	raceSummary['run'] = getNextDomValueAfterString(soup, 'Run', 'td')
	raceSummary['overall'] = getNextDomValueAfterString(soup, 'Overall', 'td')
	return raceSummary

def getRanking(soup) :
	ranking = {}
	# NOTE - yes this is backwards, but that is how Ironman has it set up...
	ranking['overall'] = splitRankText(soup.select('#div-rank')[0].get_text())
	ranking['division'] = splitRankText(soup.select('#rank')[0].get_text())
	return ranking

def getRaceData(url) :
	soup = imScraperHelper.createSoup(url)

	allSports = {}
	allSports["athlete"] = getAthleteInfoDesktop(soup)
	allSports["raceSummary"] = getRaceSummary(soup)
	allSports["ranking"] = getRanking(soup)
	
	raceDetails = {}
	raceDetails["swim"] = createSportObjectNoPredictions(soup, 'SWIM DETAILS')
	raceDetails["bike"] = createSportObjectNoPredictions(soup, 'BIKE DETAILS')
	raceDetails["run"] = createSportObjectNoPredictions(soup, 'RUN DETAILS')
	raceDetails["transition"] = getTransitionData(soup, 'Transition Details')
	allSports['raceDetails'] = raceDetails
	
	return allSports	


