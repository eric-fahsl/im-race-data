import imScraperHelper
import json
import random
from datetime import datetime
import elasticsearchHelper
import sys

BASE_RACE_RESULTS_URL = "http://www.ironman.com/triathlon/coverage/past.aspx?p="
RACES_MASTER_DATA = "races-master.json"

def extractRaceInfo(soup) :
	# for header in soup.find_all('header'):
	# 	print header.find('a').get('href')
	racesInfo = []
	for link in soup.select('.titleLink') :
		raceHrefLink = link.get('href')
		racesInfo.append(imScraperHelper.parseRaceNameAndYearFromUrl(raceHrefLink))

	#Now add the date for each of those races
	i = 0
	for dateSection in soup.select('.articleData') :
		# print 'dateSection: ' + dateSection
		dateString = dateSection.time['datetime']
		racesInfo[i]['date'] = dateString.split(' ')[0]
		i += 1

	return racesInfo

def getBibNumberFromRaceLink(href) :
	#Formats:
	#newathlete.php?rid=2147483738321&race=florida&bib=2804&v=3.0&beta=&1479707100
	#http://track.ironman.com/newsearch.php?y=2015&race=arizona&v=3.0&athlete=1991
	#newest  http://www.ironman.com/triathlon/coverage/athlete-tracker.aspx?y=2017&rd=20170730&race=canada70.3&bidid=3146&detail=1
	bib = ''
	if 'bidid=' in href :
		bib = href.split('bidid=')[1].split('&')[0]
	if 'bib=' in href :
		bib = href.split('bib=')[1].split('&')[0]
	if 'athlete=' in href :
		bib = href.split('athlete=')[1].split('&')[0]
	print 'BIB: ' + str(bib)
	return bib	

def getAllRaceInfo(pageStart = 2, pageEnd = 4) :
	print 'Opening file for reading: ' + RACES_MASTER_DATA
	f = open(RACES_MASTER_DATA, 'r')
	fileData = f.read()
	# if file is empty, initialize to empty array
	if len(fileData) < 2 : 
		fileData = '{}'
	allRacesInfo = json.loads(fileData)
	print allRacesInfo
	f.close()
	
	for page in range(pageStart, pageEnd) :
		print 'PAGE: '  + str(page)
		url = BASE_RACE_RESULTS_URL + str(page)
		soup = imScraperHelper.createSoup(url)
		thisPageRaces = extractRaceInfo(soup)

		#iterate through the races on the page.  If race not already tracked, add to the dictionary
		for race in thisPageRaces :
			try :
				raceId = str(race['year']) + '-' + str(race['name'])
				# print 'allRaceInfo.get value: |' + str(allRacesInfo.get(raceId)) + '|'
				# print 'allRacesInfo logic check value: ' + raceId + ', ' + str(allRacesInfo.get(raceId) == '')
				if (allRacesInfo.get(raceId) == None) :
					print 'New Race: ' + raceId + ', adding to race master dictionary.'
					allRacesInfo[raceId] = race
			except: 
				print("Could not parse race: ", str(race), str(sys.exc_info()))
	
	print json.dumps(allRacesInfo)
	print 'Opening file for writing: ' + RACES_MASTER_DATA
	f = open(RACES_MASTER_DATA, 'w')
	f.write(json.dumps(allRacesInfo))
	f.close()
	# '''

def getAllRaceInfoToElasticSearch(pageStart = 2, pageEnd = 4) :
	
	for page in range(pageStart, pageEnd) :
		print 'PAGE: '  + str(page)
		url = BASE_RACE_RESULTS_URL + str(page)
		soup = imScraperHelper.createSoup(url)
		thisPageRaces = extractRaceInfo(soup)

		#iterate through the races on the page.  If race not already tracked, add it to ES
		for race in thisPageRaces :
			try :
				raceId = str(race['year']) + '-' + str(race['name'])

				#first make sure the doc isn't already in ElasticSearch, otherwise, don't query again
				if elasticsearchHelper.checkIfDocumentExists(raceId) == False :
					elasticsearchHelper.createDocument(race, raceId, elasticsearchHelper.INDEX_NAME, 'raceinfo')
					print "ADDING " + raceId
				else:
					print "Document already exists in ES, skipping: " + raceId

			except: 
				print("Could not parse race: ", str(race), str(sys.exc_info()))


#Actual execution of grabbing new data
# getAllRaceInfo()

"""
url = "http://www.ironman.com/triathlon/coverage/past.aspx"
soup = imScraperHelper.createSoup(url)

extractRaceInfo(soup)

url = 'http://track.ironman.com/newsearch.php?y=2016&race=florida&v=3.0&letter=q'
soup = imScraperHelper.createSoup(url)

for link in soup.select('.athlete') :
	print link.get('href')
"""

# print getBibNumberFromRaceLink("newathlete.php?rid=2147483738321&race=florida&bib=2804&v=3.0&beta=&1479707100")