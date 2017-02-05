import elasticsearchHelper
import imSplitCalculator
import json

RACE_SUMMARY_SPORTS = ['swim', 'bike', 'run', 'overall']

QUERY = 'arizona'
# QUERY = 'cozumel'

#first do a size 0 query to get the total hit size to compute number of pages
# esPage = elasticsearchHelper.retrievePage(QUERY,0,0)
searchBody = {
    "query": {
        "bool": {
            "must": {
                "match": {
                    "_all": QUERY
                }
            },
            "must_not": {
                "exists": {
                    "field": "raceSummaryHours"
                }
            }
        }
    },
    "size": 0
}
esPage = elasticsearchHelper.search(searchBody)

TOTAL_HITS = esPage['hits']['total']
PAGE_SIZE = 100
TOTAL_PAGES = TOTAL_HITS / PAGE_SIZE + 1  #adding one page to be safe

print 'total hits', TOTAL_HITS
print 'total pages', TOTAL_PAGES


for pageIndex in range(0, TOTAL_PAGES) :
    startIndex = pageIndex * PAGE_SIZE
    # endIndex = (pageIndex + 1) * PAGE_SIZE

    print 'querying for ' + QUERY, startIndex, PAGE_SIZE

    searchBody = {
        "query": {
            "bool": {
                "must": {
                    "match": {
                        "_all": QUERY
                    }
                },
                "must_not": {
                    "exists": {
                        "field": "raceSummaryHours"
                    }
                }
            }
        },
        "size": PAGE_SIZE,
        "from": startIndex
    }

    esPage = elasticsearchHelper.search(searchBody)

    for raceResult in esPage['hits']['hits'] :
        #only if the raceSummaryHours node does NOT exist
        if 'raceSummaryHours' not in raceResult['_source']: 
            raceSummaryHours = imSplitCalculator.getRaceSummaryHoursNode(raceResult['_source']['raceSummary'])
            
            raceResult['_source']['raceSummaryHours'] = raceSummaryHours
            elasticsearchHelper.updateDocument(raceResult['_source'], raceResult['_id'])

