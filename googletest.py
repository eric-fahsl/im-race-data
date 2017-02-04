

def validateListIsEqual(inputList) :
    previousValue = None
    for input in inputList :
        #first time through, don't need to validate
        if previousValue != None :
            if input != previousValue :
                return False
        previousValue = input

    return True


def splitStringIntoEqualArrays(myString, arrayCount) :
    #ensure divisibility
    if len(myString) % arrayCount != 0 :
        return False

    eachArrayLength = len(myString) / arrayCount
    
    myStringArray = []
    for i in range(0,arrayCount) :
        startingIndex = i * eachArrayLength
        myStringArray.append(myString[startingIndex : startingIndex + eachArrayLength])
    return myStringArray

# myList = 'ab ab ab ab b'.split(' ')
# print validateListIsEqual(myList)

inputString = 'abccbaabccbaabccbaabccbaabccbaabccbaabccbaabccbaabccbaabccbaabccbaabccbaabccbaabccbaabccbaabccbaabccbaabccbaabccbaabccbaabccbaabccbaabccbaabccbaa'
# inputString = 'cabcabcabcab'
# inputString = 'aaaaaaaaaaaa'

def answer(s) :
    if s == None or len(s) > 200 :
        return None
    s = s.upper()
    print s
    highestValidCount = 1

    for arrayCount in range (2, len(inputString) + 1) :
        # print 'arrayCount: ' + str(arrayCount)
        #only if cleanly divisible
        if len(inputString) % arrayCount == 0 :
            splitStringArray = splitStringIntoEqualArrays(inputString, arrayCount)
            # print 'splitStringArray: ' + str(splitStringArray)
            if validateListIsEqual(splitStringArray) :
                # print 'These arrays are all equal!'
                highestValidCount = arrayCount
    # print splitStringIntoEqualArrays('abccbaabccba', 4)

    # print 'highestValidCount: ' + str(highestValidCount)
    return highestValidCount

# print answer(inputString)