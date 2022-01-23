# Nate Schneider
# Martin Nguyen

from itertools import cycle
import time
import math
import random
import sys
import threading

# from version1N import printMapsHistory, updateHistory

global numCycles
numCycles = 1000000
global x_bound
x_bound = 50
global y_bound
y_bound = 50
global mainMap
mainMap = None
global currMaps
currMaps = []
global numMaps
numMaps = 1
# number of maps is equal to the size of the mapsArr
global mapsHistory
mapsHistory = []
global cycleCount
cycleCount = 0
global stagnationLimit
stagnationLimit = int(numMaps / 2)
global stagnationDepth
stagnationDepth = 18


class mapObj:
    id = 0
    isMain = False
    mapArray = None
    def __init__(self, ID):
        self.id = int(ID)
    
    def __str__(self):
        strArr = "Array Uninitiliazed"
        if (self.mapArray != None):
            strArr = "Map:\n"
            loopN = 0
            while(loopN < y_bound):
                strArr += str(self.mapArray[loopN]) + "\n"
                loopN += 1
            
        isMainVal = " is the main map\n" if self.isMain else ""
        # return("twoDimArray: " + str(self.id) + isMainVal + strArr)
        return("mapObj: " + str(self.id) +  "\n" + isMainVal + strArr)


def findNeighborHoodValue(arr, x, y):
    score = 0
    # print(arrayID)
    # arr = currMaps[arrayID]
    cellValue = arr[y][x]
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

    return(score, cellValue)


def generateArray():
    tempMap = []
    y = 0
    while (y < y_bound):
        x = 0
        newXarr = []
        while (x < x_bound):
            newXarr.append(random.randint(0,1))
            x += 1
        tempMap.append(newXarr)
        y += 1
    return tempMap



def initialization():
    tempN = 0
    # initThread = threading.Thread(target=initializeMainMap())
    # initThread.start()
    while (tempN < numMaps):
        tempMap = mapObj(tempN)
        tempMap.mapArray = generateArray()
        currMaps.append(tempMap)
        tempN += 1
    global mainMap
    tempMainMap = mapObj(numMaps + 1)
    tempMainMap.mapArray = generateArray()
    tempMainMap.isMain = True
    mainMap = tempMainMap
    # initThread.join()
    # mapsHistory.append(tempN)


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

def updateMap(id):
    tempOld = currMaps[id].mapArray
    # print(tempOld)
    newArr = []
    tempY = 0
    while (tempY < y_bound):
        tempX = 0
        tempNewXarr = []
        while (tempX < x_bound):
            tempNewVal = calculateNewVal(findNeighborHoodValue(tempOld, tempX, tempY))
            tempNewXarr.append(tempNewVal)
            tempX += 1
        newArr.append(tempNewXarr)
        tempY += 1
    return newArr

def updateHistory():
    # print("appending")
    mapsHistory.append(currMaps)

def updateMaps():
    updateHistory()
    tempN = 0
    newMaps = []
    global currMaps
    while (tempN < numMaps):
        tempObj = mapObj(tempN)
        tempObj.mapArray = updateMap(tempN)
        newMaps.append(tempObj)
        tempN += 1
    # mapsHistory.append(currMaps)
    currMaps = newMaps

def mapIsDead(map):
    loopY = 0
    while(loopY < y_bound):
        loopX = 0
        while (loopX < x_bound):
            if (map[loopY][loopX] != 0):
                return False
            loopX += 1
        loopY += 1
    return True

def compareTwoMaps(map1, map2):
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

def checkForEqualToMain(mapId):
    print("checking")
    return (compareTwoMaps(currMaps[mapId].mapArray, mainMap.mapArray) <= 5)#int((x_bound*x_bound)/2))

def checkAllEqualMain():
    tempN = 0
    # print("checking")
    while (tempN < numMaps):
        if (checkForEqualToMain(tempN)):
            print(mainMap)
            printSingleMap(tempN)
            return True
        tempN += 1
    return False

def checkForStagnation(mapId):
    if (mapIsDead(currMaps[mapId].mapArray)):
        return True
    # print(mapsHistory)
    loopN = 1
    while (loopN < stagnationDepth and loopN < cycleCount):
        if (compareTwoMaps(currMaps[mapId].mapArray, mapsHistory[cycleCount - loopN][mapId].mapArray) == 0):
          return True
        loopN += 1
    return False


def checkAllStagnation():
    tempN = 0
    accum = 0
    while(tempN < numMaps):
        if (checkForStagnation(tempN)):
            # stagnationRestart(tempN)
            accum += 1
        tempN += 1
    return accum


def printMaps():
    loopN = 0
    while (loopN < numMaps):
        print(currMaps[loopN])
        loopN += 1

def printMain():
    print(mainMap)

def printSingleMap(id):
    print(currMaps[id])

def stagnationRestart(id):
    tempNewStag = mapObj(id)
    tempNewStag.mapArray = generateArray()
    currMaps[id] = tempNewStag

def manageMemory():
    global mapsHistory
    print(mapsHistory.pop(0))
    print("popped")

def printHistory():
    print("HISTORY")
    tempN = 0
    while (tempN < len(mapsHistory)):
        tempNN = 0
        while (tempNN < numMaps):
            print(mapsHistory[tempN][tempNN])
            tempNN += 1
        tempN += 1

def cycles():
    # printMaps()
    
    global cycleCount
    cycleCount = 0
    global stagnationLimit
    stagnationLimit = numMaps - 1
    while (cycleCount < numCycles):
        print("Cycle: " + str(cycleCount))
        printMaps()
        updateMaps()
        # printMaps()
        if (cycleCount > 2):
            # print("history size: " + str(len(mapsHistory)))
            # printHistory()
            if (checkAllStagnation() > stagnationLimit):
                print("Stagnant")
            # printHistory()
                cycleCount = numCycles
            # manageMemory()
        # if (checkAllEqualMain()):
            # cycleCount = numCycles

        cycleCount += 1

def run():
    initialization()
    cycles()

run()
# cycles()

