# Nate Schneider
# Martin Nguyen

import time
import math
import random
import sys
import threading

global numCycles
numCycles = 5
global x_bound
x_bound = 5
global y_bound
y_bound = 5
global mainMap
mainMap = None
global multiMaps
multiMaps = []
global numMaps
numMaps = 1
# number of maps is equal to the size of the mapsArr
global mapsHistory
mapsHistory = []
global cycleCount
cycleCount = 0
global stagnationLimit
stagnationLimit = int(numMaps / 2)


class mapObj:
    id = 0
    isMain = False
    mapArray = None
    def __init__(self, ID):
        self.id = ID
    
    def __str__(self):
        strArr = "Array Uninitiliazed"
        if (self.mapArray != None):
            strArr = "Map:\n"
            loopN = 0
            while(loopN < y_bound):
                strArr += str(self.mapArray[loopN]) + "\n"
                loopN += 1
            
        isMainVal = " is " if self.isMain else " is not "
        return("twoDimArray: " + str(self.id) + isMainVal +"the main map\n" + strArr)


def findNeighborHoodValue(arrayID, x, y):
    score = 0
    arr = multiMaps[arrayID]
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



