from datetime import datetime
from elasticsearch import Elasticsearch

import elasticsearchHelper

es = Elasticsearch()

'''
doc = {
    'author': 'kimchy',
    'text': 'Elasticsearch: cool. bonsai cool.',
    'timestamp': datetime.now(),
}
res = es.index(index="test-index", doc_type='tweet', id=2, body=doc)
print(res['created'])

res = es.get(index="test-index", doc_type='tweet', id=2)
print(res['_source'])

es.indices.refresh(index="test-index")

res = es.search(index="test-index", body={"query": {"match_all": {}}})
print("Got %d Hits:" % res['hits']['total'])
for hit in res['hits']['hits']:
    print("%(timestamp)s %(author)s: %(text)s" % hit["_source"])
'''

'''
res = es.get(index="racedata", doc_type='result', id='2016-florida-2872')
print(res['_source'])

print '----'

res = es.get(index="racedata", doc_type='result', id='2016-florida-2873')
print('source:' + res['_source'])

'''
print elasticsearchHelper.checkIfDocumentExists('2016-florida-2872')
print elasticsearchHelper.checkIfDocumentExists('2016-florida-2873')