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
numCycles = 100
global x_bound
x_bound = 10
global y_bound
y_bound = 10
global mainMap
mainMap = None
global mapsArr
mapsArr = []
global numMaps
numMaps = 10
# number of maps is equal to the size of the mapsArr






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


def updateMaps():
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


def cycles():
    cycleCount = 0
    while (cycleCount < numCycles):
        print("Cycle: " + str(cycleCount))
        updateMaps()
        printMaps()
        cycleCount += 1


initializationSetUp()
# printMaps()
cycles()