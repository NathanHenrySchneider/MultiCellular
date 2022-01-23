# Nate Schneider
# Martin Nguyen


import time
import math
import random
import sys
import threading

# from version1M import initialzationMainMap

# set size to 50x50
#Hardcoded values


global numCycles
numCycles = 5
global x_bound
x_bound = 5
global y_bound
y_bound = 5
global mainMap
mainMap = None
global mapsArr
mapsArr = []
global numMaps
numMaps = 1
# number of maps is equal to the size of the mapsArr
global mapsHistory
mapsHistory = []
global cycleCount
cycleCount = 0
global stagnationLimit
stagnationLimit = int(numMaps / 2)





class twoDimArray:
    id = 0
    isMain = False
    arrMap = None
    def __init__ (self, ID):
        self.id = ID

    def __str__(self):
        strArr = "Array Uninitiliazed"
        if (self.arrMap != None):
            strArr = "Map:\n"
            loopN = 0
            while(loopN < y_bound):
                strArr += str(self.arrMap[loopN]) + "\n"
                loopN += 1
            
        isMainVal = " is " if self.isMain else " is not "
        return("twoDimArray: " + str(self.id) + isMainVal +"the main map\n" + strArr)




def findNeighborhoodValue(arr, x, y):
    #get score from each adjacent cell starting at top going clockwise
    score = 0
    value = arr[y][x]

# arr[y+1][x]

    #top
    if (y != 0):
        # print("TOP")
        top = arr[y-1][x]
        score += top
        # print("top:"+str(top))
    # else:
    #     print("INVALID top")

    #diagonal top right
    if (x != x_bound - 1 and y != 0):
        # print("DIAGONAL TOP RIGHT")
        top_right = arr[y - 1][x + 1]
        score += top_right
        # print("top_right:"+str(top_right))
    # else:
    #     print("INVALID top right")

    #right
    # print(x)
    if (x != x_bound - 1):
        right = arr[y][x + 1]
        score += right
    #     print("right:"+str(right))
    # else:
    #     print("INVALID right")

    #diagonal bottom right
    if (x != x_bound - 1 and y != y_bound - 1):
        bottom_right = arr[y + 1][x + 1]
        score += bottom_right
    #     print("bottom_right:"+str(bottom_right))
    # else:
    #     print("INVALID bottom right")

    #bottom
    if (y != y_bound - 1):
        bottom = arr[y + 1][x]
        score += bottom
    #     print("bottom:"+str(bottom))
    # else:
    #     print("INVALID bottom")

    #diagonal bottom left
    if (y != y_bound - 1 and x != 0):
        bottom_left = arr[y + 1][x - 1]
        score += bottom_left
    #     print("bottom_left:"+str(bottom_left))
    # else:
    #     print("INVALID bottom left")

    #left
    if (x != 0):
        left = arr[y][x - 1]
        score += left
    #     print("left:"+str(left))
    # else:
    #     print("INVALID left")

    #diagonal top left
    if (x != 0 and y != 0):
        top_left = arr[y - 1][x - 1]
        score += top_left
    #     print("top_left:"+str(top_left))
    # else:
    #     print("INVALID top left")

    return(score, value)



def generateArray():
    cellMap = []
    y = 0
    while (y < y_bound):
        x = 0
        newXarr = []
        while (x < x_bound):
            newXarr.append(random.randint(0,1))
            x += 1
        cellMap.append(newXarr)
        y += 1
    return cellMap



def initializeMainMap():
    tempMainObj = twoDimArray(0)
    tempMainArr = generateArray()
    tempMainObj.isMain = True
    tempMainObj.arrMap = tempMainArr
    global mainMap
    mainMap = tempMainObj

def initializationSetUp():
    initThread = threading.Thread(target=initializeMainMap())
    initThread.start()
    tempN = 0
    while (tempN < numMaps):
        tempMap = twoDimArray(0)
        tempMap.arrMap = generateArray()
        tempMap.id = int(tempN)
        mapsArr.append(tempMap)
        tempN += 1
    initThread.join()
    mapsHistory.append(mapsArr)
    # printMaps()
    # print(mapsArr[0].arrMap)
    

def printMaps():
    loopN = 0
    while (loopN < numMaps):
        print(mapsArr[loopN])
        loopN += 1

def updateMap(id):
    # print("Start: " + str(id))
    oldArr = mapsArr[id].arrMap
    newArr = []
    tempY = 0
    while (tempY < y_bound):
        tempX = 0
        tempNewXarr = []
        while (tempX < x_bound):
            tempNewVal = calculateNewVal(findNeighborhoodValue(oldArr, tempX, tempY))
            tempNewXarr.append(tempNewVal)
            tempX += 1
        newArr.append(tempNewXarr)
        tempY += 1
    mapsArr[id].arrMap = newArr
    # print("End: " + str(id))


def compareTwoMapsHelper(map1, map2):
    score = 0
    loopY = 0
    while (loopY < y_bound):
        loopX = 0
        while (loopX < x_bound):
            if (map1[loopY][loopX] != map2[loopY][loopX]):
                score += 1
            loopX += 1
        loopY += 1
    return score


def compareTwoMaps(map1, map2):
    map1temp = None
    map2temp = None
    if (isinstance(map1, list)):
        map1temp = map1
    else:
        map1temp = map1.arrMap
    if (isinstance(map2, list)):
        map2temp = map2
    else:
        map2temp = map2.arrMap
    
    return compareTwoMapsHelper(map1temp, map2temp)



def compareTwoMapsObjs(map1,map2):
    # print("PROBLEM PROBLEM PROBLEM:")
    # print(str(map1))
    # print(str(map2))
    return(compareTwoMaps(map1.arrMap, map2))

# def compare

def mapIsDeadFirstHelper(map):
    loopY = 0
    while(loopY < y_bound):
        loopX = 0
        while (loopX < x_bound):
            if (map[loopY][loopX] != 0):
                return False
            loopX += 1
        loopY += 1
    return True

def mapIsDead(map):
    if (isinstance(map, list)):
        return mapIsDeadFirstHelper(map)
    else:
        return mapIsDeadFirstHelper(map.arrMap)

def checkAllMapsDead():
    tempN = 0
    while (tempN < numMaps):
        if (mapIsDead(mapsArr[tempN]) == False):
            # print("All maps are not dead")
            return False
        tempN += 1
    # print("All maps are dead")
    return True

def compareAllMaps():
    comparisons = []
    outerN = 0
    while (outerN < numMaps):
        innerN = outerN + 1
        while (innerN < numMaps):
            difVal = compareTwoMaps(mapsArr[outerN].arrMap, mapsArr[innerN].arrMap)
            tempComp = []
            tempComp.append(outerN)
            tempComp.append(innerN)
            tempComp.append(difVal)
            comparisons.append(tempComp)
            innerN += 1
        outerN += 1
    # print("comparisons: " + str(comparisons))


def checkAgainstMain(map):
    score = 0
    loopY = 0
    while (loopY < y_bound):
        loopX = 0
        while (loopX < x_bound):
            if (map.arrMap[loopY][loopX] != mainMap.arrMap[loopY][loopX]):
                score += 1
            loopX += 1
        loopY += 1
    # print("Map: " + str(map.id) + " is " + str(score) + " close to main")
    return score

def checkAllAgainstMain():
    closeness = []
    tempN = 0
    while (tempN < numMaps):
        closeness.append(checkAgainstMain(mapsArr[tempN]))
        tempN += 1
    tempN = 0
    highestScore = closeness[0]
    highestArrs = []
    while (tempN < numMaps):
        if (closeness[tempN] == highestScore):
            highestArrs.append(tempN)
        elif (closeness[tempN] < highestScore):
            highestArrs = []
            highestArrs.append(tempN)
            highestScore = closeness[tempN]
       
        tempN += 1
    # print("closest score: " + str(highestScore) + " belonging to map(s): " + str(highestArrs))
    # return values tbd


def calculateNewVal (inputVals):
    score = inputVals[0]
    value = inputVals[1]
    if (value == 1 and score < 2):
        return 0
    if (value == 1 and (score == 2 or score == 3)):
        return 1
    if (value == 1 and score > 3):
        return 0
    if (value == 0 and score == 3):
        return 1
    return 0

def copyArrayDeep(map):
    tempArr = []
    tempY = 0
    while (tempY < y_bound):
        tempX = 0
        tempYArr = []
        while(tempX < x_bound):
            tempYArr.append(map[tempY][tempX])
            tempX += 1
        tempArr.append(tempYArr)
        tempY += 1
    return tempArr

def updateHistory():
    tempN = 0
    newHistoryTemp = []
    while (tempN < numMaps):
        newHistoryTemp.append(copyArrayDeep(mapsArr[tempN].arrMap))
        tempN += 1
    mapsHistory.append(newHistoryTemp)

def updateMaps():
    # tempArrShallowCopy = 

    updateHistory()
    tempIDN = 0
    threads = []
    while (tempIDN < numMaps):
        # print("thread: " + str(tempIDN))
        containedN = tempIDN
        threads.append(threading.Thread(target=(updateMap(containedN))))
        threads[containedN].start()
        tempIDN += 1
    # tempJoin = 0
    # while (tempJoin < numMaps):
    #     threads[tempJoin].join()
    #     tempJoin += 1


def checkOneForStagnation(mapIDNum):
    # global cycleCount
    # check for dead
    print("checking for stagnation")
    if (mapIsDead(mapsHistory[cycleCount][mapIDNum])):
        return True
    
    # check for same as previoius iterations
    # check against n-1
    # print(str(mapsHistory[cycleCount][mapIDNum]))
    tempNNNN = mapsHistory[cycleCount - 1]
    # print(tempNNNN)
    # print("\n\n357" + str(mapsHistory[cycleCount - 1][mapIDNum]))
    
    # print("n-1" + str(compareTwoMaps(mapsHistory[cycleCount][mapIDNum], mapsHistory[cycleCount - 1][mapIDNum])))
    # print("dubeq:" + str(mapsHistory[cycleCount][mapIDNum].arrMap == mapsHistory[cycleCount - 1][mapIDNum].arrMap))
    if (compareTwoMaps(mapsHistory[cycleCount][mapIDNum], mapsHistory[cycleCount - 1][mapIDNum]) == 0):
        return True
    
    # check against n-2
    # print("n -2" + str(compareTwoMaps(mapsHistory[cycleCount][mapIDNum], mapsHistory[cycleCount - 2][mapIDNum])))
    if (compareTwoMaps(mapsHistory[cycleCount][mapIDNum], mapsHistory[cycleCount - 2][mapIDNum]) == 0):
        return True
    
    return False


def checkAllIsStagnation():
    # print("maps history: " + str(mapsHistory))
    tempN = 0
    stagAccum = 0
    while (tempN < numMaps):
        # print("hit stagnant")
        # print("NEW ERROROROROROROROR: "+ str(tempN))
        if (checkOneForStagnation(tempN)):
            stagAccum += 1
        tempN += 1
    return stagAccum


def printMapsHistory():
    # global cycleCount
    tempN = 0
    print("printing maps history\ncyclecount:" + str(cycleCount) + "\n")
    while (tempN < cycleCount ):
        print("cycle count: " + str(cycleCount))
        print("history cycle: " + str(tempN))
        tempNN = 0
        while (tempNN < numMaps):
            print(str(mapsHistory[tempN][tempNN]))
            tempNN += 1
        tempN += 1

def cycles():
    global cycleCount
    cycleCount = 0
    # print("Seed Arrays: ")
    # printMaps()
    while (cycleCount < numCycles):
        print("Cycle: " + str(cycleCount))
        updateMaps()
        printMaps()
        # compareAllMaps()
        checkAllAgainstMain()
        checkAllMapsDead()
        if (cycleCount > 2):
            stagAccum = checkAllIsStagnation()
            prntStr = "is not "
            if (stagAccum == numMaps):
                prntStr = "is"
            print (prntStr + " stagnant")
        print("MAPS HISTORY -----------------\n")
        printMapsHistory()
        print("end maps history -------------------\n")
        # print("OFFFICIALALALA CYCLE COUNTTTSSSS: " + str(cycleCount))
        cycleCount += 1
        print("\n---------------------\n")


# initializationSetUp()
# printMaps()
# cycles()


# make deep copy of arrays for maps history
# print("YEHAW")