from datetime import datetime
from elasticsearch import Elasticsearch
import json
import sys

INDEX_NAME = 'racedata'

es = Elasticsearch( http_auth=('elastic', 'changeme'))


def createDocument(documentObject,
                   docId=None,
                   inputIndex=INDEX_NAME,
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
                   inputIndex=INDEX_NAME,
                   docType='result'):
    try:
        res = es.index(
            index=inputIndex, doc_type=docType, id=docId, body=documentObject)
        print(res)
    except:
        print("Unexpected error:", str(sys.exc_info()))
        print "Document could not be created: " + str(
            docId) + "\n" + json.dumps(documentObject)

#Checks if the document already exists in ES
def checkIfDocumentExists(docId, inputIndex='racedata', docType='result'):
    try:
        res = es.get(index=INDEX_NAME, doc_type='result', id=docId)
        return True
    except:
        return False

    return False


def retrievePage(searchTerm, pageSize, startingFrom, inputIndex=INDEX_NAME, docType='result'):
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
    res = es.search(index=INDEX_NAME, doc_type='result', body=searchBody)
    return res

def search(searchBody, inputIndex=INDEX_NAME, docType='result'):
    res = es.search(index=INDEX_NAME, doc_type=docType, body=searchBody)
    return res

def genericSearch(searchString, inputIndex=INDEX_NAME, docType='result') :
    
    queryBody = {
        "query": {
            "bool": {
                "must": {
                    "match": {
                        "_all": searchString
                    }
                },
                "must_not": {
                    "match": {
                        "raceSummary.completed": "false"
                    },
                    "match": {
                        "raceInfo.year": "2016"
                    },
                    "match": {
                        "raceInfo.year": "2015"
                    },
                    "match": {
                        "raceInfo.year": "2014"
                    }
                    ,
                    "match": {
                        "raceInfo.year": "2013"
                    }
                }
            }
        },
        "size": 10000
    }
    # print docType
    return search(queryBody, inputIndex, docType)