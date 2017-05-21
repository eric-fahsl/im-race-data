import imScraperHelper
import imSplitCalculator
import elasticsearchHelper
import imRaceInfo
import json
import sys

QUERY = 'santarosa70.3'

if len(sys.argv) > 1 :
    QUERY = sys.argv[1]


esResults = elasticsearchHelper.genericSearch(QUERY, elasticsearchHelper.INDEX_NAME, 'result')
raceResults = {}
for raceData in esResults['hits']['hits'] :
    bib = raceData['_source']['raceInfo']['bib']
    raceData = raceData['_source']
    print imSplitCalculator.createCsvFriendlyFormat(bib, raceData)

