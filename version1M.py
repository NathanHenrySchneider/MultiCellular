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
numCycles  = 3
x_bound = 10 # setting size
y_bound = 10 # setting size
mapsArr = []
numberOfMaps = 10


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
    tempMainObj.cellMap = tempMainArr
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


def cycles():
    cycleCount = 0
    while(cycleCount < numCycles):
        updateMaps()
        printMaps()
        cycleCount += 1

initializationSetUp()
cycles()