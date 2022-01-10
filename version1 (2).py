# Nate Schnieder
# Martin Nguyen

import time 
import math
import random
import sys

# Set size to 50x50
global x_bound 
global y_bound 
global mainMap
x_bound = 50
y_bound = 50
# General class for the 2D array

class twoDimArray:
    id = 0
    isMain = False
    arrMap = None 
    def __init__(self,x):
        self.id = x
    
    def __str__(self):
        return("twoDimArray: " + self.x)


#finding the values surrounding the current cell
def findSurrVal(arr,index):
    x = index % (x_bound + 1)
    y = (index - x) / (x_bound + 1)
    #get score from each adjacent cells from top going clockwise
    score = 0
    value = arr[x][y]

    #top
    if (y != 0):
        top = arr[index - x_bound - 1]
        score += top
        #print("top:"+str(top))

    #top right
    if (x != x_bound and y != 0):
        top_right = arr[index - x_bound]
        score += top_right
        #print("top_right:"+str(top_right))

    #right
    if (x != x_bound):
        right = arr[index + 1]
        score += right
        #print("right:"+str(right))

    #bottom right
    if (x != x_bound and y != y_bound):
        bottom_right = arr[index + x_bound + 2]
        score += bottom_right
        #print("bottom_right:"+str(bottom_right))

    #bottom
    if (y != y_bound):
        bottom = arr[index + x_bound + 1]
        score += bottom
        #print("bottom:"+str(bottom))

    #bottom left
    if (y != y_bound and x != 0):
        bottom_left = arr[index + x_bound]
        score += bottom_left
        #print("bottom_left:"+str(bottom_left))

    #left
    if (x != 0):
        left = arr[index - 1]
        score += left
        #print("left:"+str(left))

    #top left
    if (x != 0 and y != 0):
        top_left = arr[index - x_bound - 2]
        score += top_left

    return(score, value)

def generateArray():
    cellMap = [[]]
    y = 0
    while(y < y_bound): #traversing up and down a row
        x = 0
        while(x < x_bound): #traversing through the row
            cellMap[x][y] = random.randinit(0,1)
            x+=1
        y+=1
    return cellMap

# Conway rules
def calculateNewVal(arr,index):
    retValue = findSurrVal(arr,index)
    score = retValue[0]
    value = retValue[1]
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
    tempMainObj = twoDimArray()
    tempMainArr = generateArray()
    tempMainObj.isMain = True
    tempMainObj.cellMap = tempMainArr
    mainMap = tempMainObj

def initializationSetUp():
    initialzationMainMap()



