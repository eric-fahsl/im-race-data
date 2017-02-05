from datetime import datetime
from elasticsearch import Elasticsearch
import json
import sys

es = Elasticsearch( http_auth=('elastic', 'changeme'))


def createDocument(documentObject,
                   docId=None,
                   inputIndex='racedata',
                   docType='result'):
    try:
        if (docId == None):
            docId = 'toBeDeleted'
        #create an ES document in the specified index and document type
        res = es.index(
            index=inputIndex, doc_type=docType, id=docId, body=documentObject)
        print(res['created'])
    except:
        print("Unexpected error:", str(sys.exc_info()))
        print "Document could not be created: " + str(
            docId) + "\n" + json.dumps(documentObject)

def updateDocument(documentObject,
                   docId,
                   inputIndex='racedata',
                   docType='result'):
    try:
        res = es.update(
            index=inputIndex, doc_type=docType, id=docId, body={'doc': documentObject})
        print(res)
    except:
        print("Unexpected error:", str(sys.exc_info()))
        print "Document could not be created: " + str(
            docId) + "\n" + json.dumps(documentObject)

#Checks if the document already exists in ES
def checkIfDocumentExists(docId, inputIndex='racedata', docType='result'):
    try:
        res = es.get(index="racedata", doc_type='result', id=docId)
        return True
    except:
        return False

    return False


def retrievePage(searchTerm, pageSize, startingFrom, inputIndex='racedata', docType='result'):
    # res = es.search(index="racedata", doc_type='result', params='q=coeur*&size=2&from=30')
    searchBody = {
        "query": {
            "match": {
                "_all": searchTerm
            }
        },
        "size": pageSize,
        "from": startingFrom
    }
    res = es.search(index="racedata", doc_type='result', body=searchBody)
    return res

def search(searchBody, inputIndex='racedata', docType='result'):
    res = es.search(index="racedata", doc_type='result', body=searchBody)
    return res