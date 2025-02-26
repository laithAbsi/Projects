

def makeDicts():
    incomeDict = dict()
    countryDict = dict()
    countryList = [] # list of countries, in the order in the file
    gdpList = [] # list of GDPs, in the order in the file.
    initialList = [] #list of first letters of countries, same order
    with open('lab8.txt','r') as f:
        for line in f:
            line = line.upper().strip().split(':')
            countryList.append(line[0])
            gdpList.append(line[1])
            initial = line[0][0]
            initialList.append(initial)
        for i in range(len(countryList)):
            incomeDict[ countryList[i] ] = gdpList[i]
            if initialList[i] not in countryDict:
                countryDict[initialList[i]] = set( )
            countryDict[initialList[i]].add( countryList[i])
    return (incomeDict,countryDict)

def main():
    incomeDict, countryDict = makeDicts()
    userInp = input('enter a country nane or a letter: ')
    while userInp == 'DONE':
        break
    while len(userInp) == 1:
        for i in countryDict:
            if userInp == countryDict[i][0]:
                output = countryDict[i]

    print(output)
