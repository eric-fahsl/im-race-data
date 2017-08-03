from bs4 import BeautifulSoup
import urllib
import urllib2
from random import randint

TRACK_URL_DOMAIN = 'http://track.ironman.com/'
RACE_TRACK_URL_BASE = TRACK_URL_DOMAIN + 'newsearch.php'

USER_AGENTS = [ 
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36', 
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36', 
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/602.2.14 (KHTML, like Gecko) Version/10.0.1 Safari/602.2.14', 
    'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0', 
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36', 
];


data = {}

def createSoup(url) :
    values = {}
    headers = {
        'User-Agent': USER_AGENTS[randint(0,4)],
        'Referer': 'http://www.ironman.com/'
    }
    data = urllib.urlencode(values)
    request = urllib2.Request(url, data, headers)
    response = urllib2.urlopen(request)
	# print response

    the_page = response.read()
    soup = BeautifulSoup(the_page)
    return soup


def searchContentForTag(uniqueText, uniqueText2, tagNameOpen, tagNameClose, content, offset) :
    uniqueTextIndex = content.find(uniqueText, offset)

    if (len(uniqueText2) > 0) :
        uniqueTextIndex = content.find(uniqueText2, uniqueTextIndex)

    tagNameIndex = content.find(tagNameOpen, uniqueTextIndex)
    #if (includeTagOpen != True) :
    tagNameIndex += len(tagNameOpen)
    tagNameCloseIndex = content.find(tagNameClose, tagNameIndex)
    #if (includeTagClose) :
    #tagNameCloseIndex += len(tagNameClose)

    tagContent = content[tagNameIndex:tagNameCloseIndex]

    return [ tagContent, tagNameCloseIndex ]


# http://www.ironman.com/triathlon/coverage/detail.aspx?race=xiamen70.3&y=2016
def parseRaceNameAndYearFromUrl(urlpath) :
    raceNameStartIndex = urlpath.find('race=') + 5 
    raceNameEndIndex = urlpath.find('&y=')
    race = urlpath[ raceNameStartIndex : raceNameEndIndex ]
    year = urlpath [ raceNameEndIndex + 3:]
    return {        
        'name': race,
        'year': year
    }


def getLinksForRace(year, raceName, startLetter='a', endLetter='z') :
    #http://track.ironman.com/newsearch.php?y=2016&race=florida&v=3.0&letter=c
    # http://www.ironman.com/triathlon/coverage/athlete-tracker.aspx?rd=20170730&race=canada70.3&y=2017&l=A
    resultLinks = []

    for letterInt in range (ord(startLetter), ord(endLetter)+1) :
        letterChar = chr(letterInt)
        url = RACE_TRACK_URL_BASE + '?y=' + str(year) + '&race=' + str(raceName) + '&v=3.0&letter=' + letterChar
        
        print url
        soup = createSoup(url)

        for link in soup.findAll('a') :
            print link
            urlLink = link['href']
            # Check if hostname already included in URL
            if 'ironman.com' not in urlLink :
                urlLink = TRACK_URL_DOMAIN + urlLink
            
            resultLinks.append(urlLink)
        
    return resultLinks

def getLinksForRaceV2(year, raceName, startLetter='a', endLetter='z') :
    #http://track.ironman.com/newsearch.php?y=2016&race=florida&v=3.0&letter=c
    resultLinks = []

    for letterInt in range (ord(startLetter), ord(endLetter)+1) :
        letterChar = chr(letterInt)
        # url = RACE_TRACK_URL_BASE + '?y=' + str(year) + '&race=' + str(raceName) + '&v=3.0&letter=' + letterChar
        #http://www.ironman.com/triathlon/coverage/detail.aspx?race=canada70.3&y=2017#axzz4oMiK6LLc
        url = 'http://www.ironman.com/triathlon/coverage/athlete-tracker.aspx?race=' + str(raceName) + '&y=' + str(year) + '&l=' + letterChar
        
        print url
        appendLinksFromPage(url, resultLinks)
        # soup = createSoup(url)
        # appendLinksFromPage(soup, url)

        # print soup
        '''
        for link in soup.findAll('a', {'class':'athlete'}) :            
            urlLink = link.get('href')
            # Check if hostname already included in URL
            if 'ironman.com' not in urlLink :
                urlLink = 'http://www.ironman.com/triathlon/coverage/athlete-tracker.aspx' + urlLink
            
            resultLinks.append(urlLink)
        '''
    
    # print resultLinks
    return resultLinks
    # return []

def appendLinksFromPage(url, resultLinks) :
    soup = createSoup(url)
    for link in soup.findAll('a', {'class':'athlete'}) :            
        urlLink = link['href']
        # Check if hostname already included in URL
        if 'ironman.com' not in urlLink :
            urlLink = 'http://www.ironman.com/triathlon/coverage/athlete-tracker.aspx' + urlLink
        
        resultLinks.append(urlLink)
    
    for nextLink in soup.findAll('a', {'class':'nextPage'}) :
        appendLinksFromPage(nextLink['href'], resultLinks)
    