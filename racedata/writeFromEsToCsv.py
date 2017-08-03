import imScraperHelper
import imSplitCalculator
import elasticsearchHelper
import imRaceInfo
import json
import sys

#For encoding issues
reload(sys)
sys.setdefaultencoding('utf-8')

QUERY = 'canada70.3'

if len(sys.argv) > 1 :
    QUERY = sys.argv[1]


esResults = elasticsearchHelper.genericSearch(QUERY, elasticsearchHelper.INDEX_NAME, 'result')
raceResults = {}
print imSplitCalculator.createCsvHeaderLine()
for raceData in esResults['hits']['hits'] :
    print imSplitCalculator.createCsvFriendlyFormat(raceData['_source'])

