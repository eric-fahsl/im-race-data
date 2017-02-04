import elasticsearchHelper
import imSplitCalculator
import json

RACE_SUMMARY_SPORTS = ['swim', 'bike', 'run', 'overall']

QUERY = 'arizona'

#first do a size 0 query to get the total hit size to compute number of pages
esPage = elasticsearchHelper.retrievePage(QUERY,0,0)

TOTAL_HITS = esPage['hits']['total']
PAGE_SIZE = 100
TOTAL_PAGES = TOTAL_HITS / PAGE_SIZE + 1  #adding one page to be safe

print 'total hits', TOTAL_HITS
print 'total pages', TOTAL_PAGES


for pageIndex in range(0, TOTAL_PAGES) :
    startIndex = pageIndex * PAGE_SIZE
    # endIndex = (pageIndex + 1) * PAGE_SIZE

    print 'querying for ' + QUERY, startIndex, PAGE_SIZE
    esPage = elasticsearchHelper.retrievePage(QUERY, startIndex, PAGE_SIZE)

    for raceResult in esPage['hits']['hits'] :
        #only if the raceSummarySeconds node does NOT exist
        if 'raceSummarySeconds' not in raceResult['_source']: 
            raceSummarySeconds = imSplitCalculator.getRaceSummarySecondsNode(raceResult['_source']['raceSummary'])
            
            raceResult['_source']['raceSummarySeconds'] = raceSummarySeconds
            elasticsearchHelper.updateDocument(raceResult['_source'], raceResult['_id'])

