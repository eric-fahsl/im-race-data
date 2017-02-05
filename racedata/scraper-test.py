import imSplitCalculator
import elasticsearchHelper
import imScraperHelper
import json
import re
import imRaceInfo

raceId = "2147483720"
# RACE_ID="2278373444"
race = "canada"
bib = 517
raceStartTime = "7:00:00"

# BIB=1571
# url = "http://tracking.ironmanlive.com/mobilesearch.php?rid=2278373444&race=taiwan&y=2015&athlete=559#axzz3X0O9WgL1"
# url = "http://tracking.ironmanlive.com/mobilesearch.php?rid=" + raceId + "&race=" + race + "&y=2015&athlete=" + str(bib) + "#axzz3X0O9W" + str(randomNum)
#url = "http://tracking.ironmanlive.com/mobilesearch.php?rid=2147483658&race=stgeorge70.3&y=2015&athlete=1856#axzz3X0O9W9"
# url = "http://tracking.ironmanlive.com/mobileathlete.php?rid=2147483716&race=steelhead70.3&bib=20&v=3.0&beta=&1439134200#axzz3iKf8Dzxl"
# url = "http://tracking.ironmanlive.com/mobilesearch.php?rid=2147483720&race=canada&y=2015&athlete=517#axzz3X0O9W70"
#url = "http://track.ironman.com/newsearch.php?y=2016&race=arizona&v=3.0&athlete=169"
url = "http://track.ironman.com/newsearch.php?y=2015&race=arizona&v=3.0&athlete=1991"
# url = "http://track.ironman.com/newathlete.php?rid=2147483738321&race=florida&bib=2804&v=3.0&beta=&1479664800"
# url = "http://track.ironman.com/newathlete.php?rid=26&race=newzealand&bib=3&v=3.0&beta=&1479667500"

# athleteData = imSplitCalculator.getRaceData(url)
# print json.dumps(athleteData, sort_keys=True, indent=4, separators=(',', ': '))
# soup = imScraperHelper.createSoup(url)

# print imSplitCalculator.getNextDomValueAfterString(soup, 'Swim:', 'td')
# print imSplitCalculator.getNextDomValueAfterString(soup, 'Bike', 'td')
# print imSplitCalculator.getNextDomValueAfterString(soup, 'Run', 'td')
# print imSplitCalculator.getNextDomValueAfterString(soup, 'Overall', 'td')


def confirmTestValue(received, expected, testName) :
    if str(received) == str(expected) :
        print '***' + testName + ' PASSED'
    else :
        print testName + ' FAILED. Expected: ' + str(expected) + ', but received: ' + str(received)

def testDesktopEricIMAZ() :
    url = "http://track.ironman.com/newsearch.php?y=2015&race=arizona&v=3.0&athlete=1991"
    athleteData = imSplitCalculator.getRaceData(url)
    strVal = json.dumps(athleteData)
    # print json.dumps(athleteData, sort_keys=True, indent=4, separators=(',', ': '))
    confirmTestValue(len(strVal), 3671, 'testDesktopEricIMAZ')

def test703WithNoSwim() :
    url = "http://track.ironman.com/newathlete.php?rid=2147483736012&race=longhorn70.3&bib=9&v=3.0&beta=&1479693600"
    # soup = imScraperHelper.createSoup(url)
    athleteData = imSplitCalculator.getRaceData(url)
    # print json.dumps(athleteData, sort_keys=True, indent=4, separators=(',', ': '))
    strVal = json.dumps(athleteData)
    confirmTestValue(len(strVal), 2105, 'test703WithNoSwim')


def testOldRaceWithNoSwimData() :
    url = "http://track.ironman.com/newathlete.php?rid=26&race=newzealand&bib=3&v=3.0&beta=&1479667500"
    athleteData = imSplitCalculator.getRaceData(url)
    # print json.dumps(athleteData, sort_keys=True, indent=4, separators=(',', ': '))
    strVal = json.dumps(athleteData)
    confirmTestValue(len(strVal), 493, 'testOldRaceWithNoSwimData')

def testScraperBibLogic() :
    confirmTestValue(imRaceInfo.getBibNumberFromRaceLink('newathlete.php?rid=2147483738321&race=florida&bib=2804&v=3.0&beta=&1479707100'),2804,'testScraperBibLogic: bib=')
    confirmTestValue(imRaceInfo.getBibNumberFromRaceLink('http://track.ironman.com/newsearch.php?y=2015&race=arizona&v=3.0&athlete=1991'),1991,'testScraperBibLogic: athlete=')

def testGetAthleteLinksForRace() :
    athleteLinks = imScraperHelper.getLinksForRace(2016, 'florida', 'a', 'a')
    # print json.dumps(athleteLinks)
    confirmTestValue(len(json.dumps(athleteLinks)), 8982, 'testGetAthleteLinksForRace: Florida 2016 letter A')

def testStringTimeToSeconds() :
    secondsValue = imSplitCalculator.convertTimeToSeconds('43:20')
    confirmTestValue(secondsValue, 2600, 'testStringTimeToSeconds 43:20')
    secondsValue = imSplitCalculator.convertTimeToSeconds('00:43:20')
    confirmTestValue(secondsValue, 2600, 'testStringTimeToSeconds 00:43:20')
    secondsValue = imSplitCalculator.convertTimeToSeconds('10:43:20')
    confirmTestValue(secondsValue, 38600, 'testStringTimeToSeconds 10:43:20')
    secondsValue = imSplitCalculator.convertTimeToSeconds('--:--')
    confirmTestValue(secondsValue, 0, 'testStringTimeToSeconds --:--')

def testStringTimeToHours() :
    hoursValue = imSplitCalculator.convertTimeToHours('43:20')
    confirmTestValue(hoursValue, 0.722222222222, 'testStringTimeToHours 43:20')
    hoursValue = imSplitCalculator.convertTimeToHours('00:43:20')
    confirmTestValue(hoursValue, 0.722222222222, 'testStringTimeToHours 00:43:20')
    hoursValue = imSplitCalculator.convertTimeToHours('10:43:20')
    confirmTestValue(hoursValue, 10.722222222222, 'testStringTimeToHours 10:43:20')
    hoursValue = imSplitCalculator.convertTimeToHours('--:--')
    confirmTestValue(hoursValue, 0, 'testStringTimeToHours --:--')


# testScraperBibLogic()
# testDesktopEricIMAZ()
# test703WithNoSwim()
# testOldRaceWithNoSwimData()
# testGetAthleteLinksForRace()
testStringTimeToSeconds()
testStringTimeToHours()