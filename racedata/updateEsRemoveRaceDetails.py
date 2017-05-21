import elasticsearchHelper
import imSplitCalculator
import json

RACE_SUMMARY_SPORTS = ['swim', 'bike', 'run', 'overall']

QUERY = '*'
# QUERY = 'cozumel'

#first do a size 0 query to get the total hit size to compute number of pages
# esPage = elasticsearchHelper.retrievePage(QUERY,0,0)
searchBody = {
	"query": {
		"bool": {
			"must": [{
				"exists": {
					"field": "doc"
				}
			}]
		}
	},
	"size": 0
}
esPage = elasticsearchHelper.search(searchBody)

TOTAL_HITS = esPage['hits']['total']
TOTAL_HITS = 10
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
                "must": [
                    
                    {
                    "exists": {
                        "field": "doc"
                    }
                }]
            }
        },
        "size": PAGE_SIZE,
        "from": startIndex
    }

    esPage = elasticsearchHelper.search(searchBody)

    for raceResult in esPage['hits']['hits'] :
        raceResult['_source'] = raceResult['_source']['doc']
        # print raceResult
        elasticsearchHelper.updateDocument(raceResult['_source'], raceResult['_id'])

