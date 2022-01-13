# Nate Schnieder
# Martin Nguyen
# using multithreading with cellular automata

import time 
import math
import random
import sys
import threading

# Declaring global Variables

global x_bound 
global y_bound 
global mainMap
global mapsArr
global numberOfMaps
global numCycles
global mapsHistory
global cycleCount
global stagLim
mainMap = []
cycleCount = 0
mapsHistory = []
numCycles  = 5
x_bound = 3 # setting size
y_bound = 3 # setting size
mapsArr = []
numberOfMaps = 3
stagLim = int(numberOfMaps/2)


# General class for the 2D array

class twoDimArray:
    id = 0
    isMain = False
    arrMap = None 
    def __init__(self,id):
        self.id = id
    
    def __str__(self):
        strArr = "Array Uninitialized"
        if(self.arrMap != None):
            strArr = "Map:\n"
            loopN = 0
            while(loopN < y_bound):
                strArr += str(self.arrMap[loopN]) + "\n"
                loopN += 1
        isMainVal = "is" if self.isMain else "is not"
        return("twoDimArray: " + str(self.id) + " " + isMainVal + " the main map\n" + strArr)


#finding the values surrounding the current cell

def findSurrVal(arr, x, y):
    # x = index % (x_bound + 1)
    # y = (index - x) / (x_bound + 1)
    #get score from each adjacent cells from top going clockwise
    score = 0
    value = arr[y][x]

    #top
    if (y != 0):
        top = arr[y - 1][x]
        score += top
        #print("top:"+str(top))

    #top right
    if (x != x_bound -1 and y != 0):
        top_right = arr[y - 1][x + 1]
        score += top_right
        #print("top_right:"+str(top_right))

    #right
    if (x != x_bound - 1):
        right = arr[y][x + 1]
        score += right
        #print("right:"+str(right))

    #bottom right
    if (x != x_bound -1 and y != y_bound - 1):
        bottom_right = arr[y + 1][x + 1]
        score += bottom_right
        #print("bottom_right:"+str(bottom_right))

    #bottom
    if (y != y_bound - 1):
        bottom = arr[y + 1][x]
        score += bottom
        #print("bottom:"+str(bottom))

    #bottom left
    if (y != y_bound - 1 and x != 0):
        bottom_left = arr[y + 1][x - 1]
        score += bottom_left
        #print("bottom_left:"+str(bottom_left))

    #left
    if (x != 0):
        left = arr[y][x - 1]
        score += left
        #print("left:"+str(left))

    #top left
    if (x != 0 and y != 0):
        top_left = arr[y - 1][x - 1]
        score += top_left

    return(score, value)

# populating the array

def generateArray():
    cellMap = []
    y = 0
    while(y < y_bound): #traversing up and down a row
        x = 0
        newXarr = []
        while(x < x_bound): #traversing through the row
            newXarr.append(random.randint(0,1))
            x+=1
        cellMap.append(newXarr)
        y+=1
    return cellMap

# Conway rules

def calculateNewVal(inputVals):
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

def initialzationMainMap():
    tempMainObj = twoDimArray(0)
    tempMainArr = generateArray()
    tempMainObj.isMain = True
    tempMainObj.arrMap = tempMainArr
    global mainMap
    mainMap = tempMainObj

# does the threading with initialization for main map

def initializationSetUp():
    initThread = threading.Thread(target=initialzationMainMap())
    initThread.start()
    tempNumber = 0
    while(tempNumber < numberOfMaps):
        tempMap = twoDimArray(0)
        tempMap.arrMap = generateArray()
        tempMap.id = int(tempNumber)
        mapsArr.append(tempMap)
        tempNumber += 1
    initThread.join()
    #printMaps()
    #print(mapsArr[0].arrMap)

# printing the maps for visualization confirmation

def printMaps():
    loopN = 0
    while(loopN<numberOfMaps):
        print(mapsArr[loopN])
        loopN += 1

# updating the map 
# calls findSurrVal to update the map
def updateMap(id):
    oldArr = mapsArr[id].arrMap
    newArr = []
    tempY = 0
    while(tempY < y_bound):
        tempX = 0
        tempNewXarr = []
        while(tempX < x_bound):
            tempVal = calculateNewVal(findSurrVal(oldArr,tempX,tempY))
            tempNewXarr.append(tempVal)
            tempX += 1
        newArr.append(tempNewXarr)
        tempY += 1
    mapsArr[id].arrMap = newArr

def updateMaps():
    mapsHistory.append(mapsArr)
    tempNID = 0
    threads = []
    while(tempNID < numberOfMaps):
        containedN = tempNID
        threads.append(threading.Thread(target=updateMap(containedN)))
        threads[containedN].start()
        tempNID += 1
    tempJoin = 0
    while(tempJoin < numberOfMaps):
        threads[tempJoin].join()
        tempJoin += 1

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

def mapIsDead(map):
    loopY = 0
    while(loopY < y_bound):
        loopX = 0
        while (loopX < x_bound):
            if (map.arrMap[loopY][loopX] != 0):
                return False
            loopX += 1
        loopY += 1
    return True

def checkAllMapsDead():
    tempN = 0
    while (tempN < numberOfMaps):
        if (mapIsDead(mapsArr[tempN]) == False):
            print("All maps are not dead")
            return False
        tempN += 1
    print("All maps are dead")
    return True

def compareAllMaps():
    comparisons = []
    outerN = 0
    while (outerN < numberOfMaps):
        innerN = outerN + 1
        while (innerN < numberOfMaps):
            difVal = compareTwoMaps(mapsArr[outerN].arrMap, mapsArr[innerN].arrMap)
            tempComp = []
            tempComp.append(outerN)
            tempComp.append(innerN)
            tempComp.append(difVal)
            comparisons.append(tempComp)
            innerN += 1
        outerN += 1
    print("comparisons: " + str(comparisons))


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
    #print("Map: " + str(map.id) + " is " + str(score) + " close to main")
    return score

def checkAllAgainstMain():
    closeness = []
    tempN = 0
    while (tempN < numberOfMaps):
        closeness.append(checkAgainstMain(mapsArr[tempN]))
        tempN += 1
    tempN = 0
    highestScore = closeness[0]
    highestArrs = []
    while (tempN < numberOfMaps):
        if (closeness[tempN] == highestScore):
            highestArrs.append(tempN)
        elif (closeness[tempN] < highestScore):
            highestArrs = []
            highestArrs.append(tempN)
            highestScore = closeness[tempN]
       
        tempN += 1
    #print("closest score: " + str(highestScore) + " belonging to map(s): " + str(highestArrs))

def checkForStagnation(mapNumID):
    #print("History~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    #print(mapsHistory[cycleCount][mapNumID].arrMap)
    #print(mapsHistory[cycleCount-1][mapNumID].arrMap)
    if(mapIsDead(mapsHistory[cycleCount][mapNumID])):
        return True
    
    if(compareTwoMaps(mapsHistory[cycleCount][mapNumID].arrMap, mapsHistory[cycleCount-1][mapNumID].arrMap) == 0):
        return True
    
    if(compareTwoMaps(mapsHistory[cycleCount][mapNumID].arrMap, mapsHistory[cycleCount-2][mapNumID].arrMap) == 0):
        return True
    
    
    return False

def checkAllForStagnation():
    tempN = 0
    stagAccum = 0
    while(tempN < numberOfMaps):
        if(checkForStagnation(tempN)):
            stagAccum += 1
        tempN += 1
    return stagAccum

def cycles():
    cycleCount = 0
    while(cycleCount < numCycles):
        updateMaps()
        printMaps()
        compareAllMaps()
        checkAllAgainstMain()
        print("cycle: " + str(cycleCount))
        if(cycleCount > 3):
            stagAccum = checkAllForStagnation()
        cycleCount += 1

initializationSetUp()
cycles()