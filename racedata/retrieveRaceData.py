import imScraperHelper
import imSplitCalculator
import elasticsearchHelper
import imRaceInfo
import json
import sys

RACES_MASTER_DATA = "races-master-small.json"
# RACES_MASTER_DATA = "races-master.json"

SKIP_CONDITION_STRINGS = ['5150']

############
# Assumes race meta data already retrieved and stored in races-master.json.  
# If the race data entry has an attribute of 'read': True, then skip reading that race
############

def createElasticSearchId(race, bib) :
    raceId = str(race['year']) + '-' + str(race['name']) + '-' + str(bib)
    return raceId

def getRaces() :
	print 'Opening file for reading: ' + RACES_MASTER_DATA
	f = open(RACES_MASTER_DATA, 'r')
	fileData = f.read()
	allRacesInfo = json.loads(fileData)
	f.close()
	return allRacesInfo

def skipCondition(raceId) :
    retValue = False
    for skipString in SKIP_CONDITION_STRINGS :
        if skipString in raceId :
            retValue = True
    return retValue
    

# def getUrlsForRace(race) :

startLetter = 'a'
endLetter = 'z'

if len(sys.argv) > 1 :
    startLetter = sys.argv[1]
    endLetter = sys.argv[2]

print startLetter, endLetter


races = getRaces()
#iterate through all races
for id, race in races.iteritems() :

    #Skip certain kind of races
    if skipCondition(id) :
        print ("SKIPPING", id)
    else :
        # print 'race: ' + str(race)
        #get all of the Athlete URLs
        athleteUrls = imScraperHelper.getLinksForRace(race['year'], race['name'], startLetter, endLetter)

        for athleteUrl in athleteUrls :
            bibNumber = imRaceInfo.getBibNumberFromRaceLink(athleteUrl)
            esId = createElasticSearchId(race, bibNumber)

            #first make sure the doc isn't already in ElasticSearch, otherwise, don't query again
            if elasticsearchHelper.checkIfDocumentExists(esId) == False :
                print "Querying: " + athleteUrl
                athleteData = imSplitCalculator.getRaceData(athleteUrl) 
                athleteData['raceInfo'] = race
                athleteData['raceInfo']['bib'] = bibNumber
                
                elasticsearchHelper.createDocument(athleteData, esId)
            else:
                print "Document already exists in ES, skipping: " + esId

