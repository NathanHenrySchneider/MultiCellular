# Nate Schneider
# Martin Nguyen



import time
import math
import random
import sys

# set size to 50x50
#Hardcoded values

global x_bound
x_bound = 50
global y_bound
y_bound = 50
global mainMap
mainMap = None






class twoDimArray:
    id = 0
    isMain = False
    arrMap = None
    def __init__ (self, ID):
        self.id = ID

    def __str__(self):
        return("twoDimArray: " + self.id + "/n")




def findNeighborhoodValue(arr, index):
    x = index % (x_bound + 1)
    y = (index - x) / (x_bound + 1)
    #get score from each adjacent cell starting at top going clockwise
    score = 0
    value = arr[x][y]

    #top
    if (y != 0):
        top = arr[index - x_bound - 1]
        score += top
        #print("top:"+str(top))

    #diagonal top right
    if (x != x_bound and y != 0):
        top_right = arr[index - x_bound]
        score += top_right
        #print("top_right:"+str(top_right))

    #right
    if (x != x_bound):
        right = arr[index + 1]
        score += right
        #print("right:"+str(right))

    #diagonal bottom right
    if (x != x_bound and y != y_bound):
        bottom_right = arr[index + x_bound + 2]
        score += bottom_right
        #print("bottom_right:"+str(bottom_right))

    #bottom
    if (y != y_bound):
        bottom = arr[index + x_bound + 1]
        score += bottom
        #print("bottom:"+str(bottom))

    #diagonal bottom left
    if (y != y_bound and x != 0):
        bottom_left = arr[index + x_bound]
        score += bottom_left
        #print("bottom_left:"+str(bottom_left))

    #left
    if (x != 0):
        left = arr[index - 1]
        score += left
        #print("left:"+str(left))

    #diagonal top left
    if (x != 0 and y != 0):
        top_left = arr[index - x_bound - 2]
        score += top_left
        #print("top_left:"+str(top_left))

    return(score, value)



def generateArray():
    cellMap = [[]]
    y = 0
    while (y < y_bound):
        x = 0
        while (x < x_bound):
            cellMap[x][y] = random.randint(0,1)
            x += 1
        y += 1
    return cellMap



def calculateNewVal (arr, index):
    retVal = findNeighborhoodValue(arr, index)
    score = retVal[0]
    value = retVal[1]
    if (value == 1 and score < 2):
        return 0
    if (value == 1 and (score == 2 or score == 3)):
        return 1
    if (value == 1 and score > 3):
        return 0
    if (value == 0 and score == 3):
        return 1
    return 0


def initializeMainMap():
    tempMainObj = twoDimArray()
    tempMainArr = generateArray()
    tempMainObj.isMain = True
    tempMainObj.arrMap = tempMainArr
    global mainMap
    mainMap = tempMainObj

def initializationSetUp():
    initializeMainMap()
    
