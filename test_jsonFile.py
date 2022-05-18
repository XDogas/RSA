import jsonFile;

filePath = "examples/in_cam.json"

print("printData test")
jsonFile.printData(filePath)

print("\ntoDict test")
dataDict = jsonFile.toDict(filePath)
print(dataDict)
print(type(dataDict))

print("\ntoStr test")
dataStr = jsonFile.toStr(filePath)
print(dataStr)
print(type(dataStr))

print("\nwriteFile test")
dirPath = "my_jsons"
newFileName = "cam.json"
jsonFile.writeFile(dataDict, dirPath, newFileName)
newFilePath = dirPath + "/" + newFileName
print("file in:", newFilePath)

print("\nsetValue test")
print("value before:", dataDict["accEngaged"])
jsonFile.setValue(newFilePath, "accEngaged", False)
newDataDict = jsonFile.toDict(newFilePath)
print("value after:", newDataDict["accEngaged"])