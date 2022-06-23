import json
import os

def printData(filePath):                                # function to print dictionary with jason data
    with open(filePath, "r") as f:                      # open to read-only
        print(json.load(f))                             # print dictionary

def toDict(filePath):                                   # function to convert json file to dictionary
    with open(filePath, "r") as f:                      # open to read-only
        return json.load(f)                             # returns dictionary

def toStr(filePath):                                    # function to convert json file to string
    return json.dumps(toDict(filePath))                 # returns string

def writeFile(dataDict, dirPath, newFileName):          # function to write data to a new jason file
    if not os.path.isdir(dirPath):                      # check if directory exists
        os.mkdir(dirPath)                               # create directory
    with open(dirPath + "/" + newFileName, "w") as f:   # open to write
        json.dump(dataDict, f)                          # create json file

def setValue(filePath, key, value):                     # function to set a value associated with a certain key
    dataDict = toDict(filePath)                         # convert json file to a dictionary
    dataDict[key] = value                               # set value associated with thekey
    with open(filePath, "w") as f:                      # open to write
        json.dump(dataDict, f)                          # create json file with the new value

def updateFile(filePath, dataDict):                     # funciton to update file
    with open(filePath, "w") as f:                      # open to write
        json.dump(dataDict, f)                          # create json file with the new value