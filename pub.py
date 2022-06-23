from pydoc_data.topics import topics
import paho.mqtt.client as mqtt
import time
import sys
import logging
import jsonFile
from ipyleaflet import Map, Marker
from ipywidgets import Layout
import math
import random

def distanceBetween(coor1, coor2):
    lat1 = math.radians(coor1[0])
    lon1 = math.radians(coor1[1])
    lat2 = math.radians(coor2[0])
    lon2 = math.radians(coor2[1])

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    # Haversine formula
    a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2

    c = 2 * math.asin(math.sqrt(a))

    r = 6371    # Radius of earth in kilometers

    return (c * r) * 10**3

def getCoordinates(inicio, fim):
    positions = []

    positions.append(inicio)

    distance = distanceBetween(inicio, fim)

    distBetweenPositions = 1

    percentage = distBetweenPositions/distance

    latTraveled = fim[0] - inicio[0]
    lonTraveled = fim[1] - inicio[1]

    latDiff = latTraveled * percentage
    lonDiff = lonTraveled * percentage

    newCoor = inicio
    while distanceBetween(newCoor, fim) > distBetweenPositions/2:
        newLat = newCoor[0] + latDiff
        newLon = newCoor[1] + lonDiff
        newCoor = (newLat, newLon)
        positions.append(newCoor)

    positions.append(fim)
    semaforo = positions[int(len(positions)/2 - 1)]

    return positions, semaforo

def randomIdx():
    start = 1/freq # 1st second index
    end = 4/freq # 4th second index
    return random.randint(start, end)

def updateCam(camFileName, dataDict, coordinates, speed, lastSpeed):
    dataDict["latitude"] = coordinates[0]
    dataDict["longitude"] = coordinates[1]
    dataDict["speed"] = speed
    currSpeed = dataDict["speed"]
    acceleration = (currSpeed - lastSpeed) / freq
    # dataDict["acceleration"] = (currSpeed - lastSpeed) / freq
    dataDict["brakePedal"] = False
    if acceleration < 0 or lastSpeed == speed == 0:
        dataDict["brakePedal"] = True
    dataDict["gasPedal"] = not dataDict["brakePedal"]
    jsonFile.updateFile(camFileName, dataDict)

# client logging function
def on_log(client, userdata, level, buf):
    return # apagar quando descomentar a linha abaixo
    #logging.info("log: " + buf)

# callback functions
def on_connect(client, userdata, flags, rc):
    if rc==0:
        client.connected_flag = True    # set flag
        #logging.info("connected OK")
    else:
        #logging.info("Bad connection returned code " + rc)
        client.loop_stop()

def on_disconnect(client, userdata, flags, rc=0):
    #logging.info("disconnected result code " + str(rc))
    client.connected_flag = False

def on_subscribe(lient, userdata, mid, granted_qos):
    return # apagar quando descomentar a linha abaixo
    #logging.info("subscribed")

def on_message(client, userdata, message):
    return # apagar quando descomentar a linha abaixo
    #logging.info("message received: " + str(message.payload.decode("utf-8")))
    #logging.info("message topic =",message.topic)
    #logging.info("message qos =",message.qos)
    #logging.info("message retain flag =",message.retain)

# connect function
def connectClientToBroker(client, broker):
    print("connecting to brocker " + broker)
    try:
        client.connect(broker)          # connect to broker
    except:
        print("connection failed")
        sys.exit()
    client.loop_start()                 # start loop
    while not client.connected_flag:    # wait for connection
        print("establishing connection...")
        time.sleep(1)

inicio = (40.6315902455964, -8.648363571983388)
#semaforo = (40.63248427696954, -8.648497339035185)
fim = (40.633377601639815, -8.648627265512228)
positions, semaforo = getCoordinates(inicio, fim)

positionsIdxOBU1 = 0
positionsIdxOBU2 = 0
positionsIdxOBU3 = 0

# map
defaultLayout=Layout(width='960px', height='960px')
center = (40.63249, -8.64848)
m = Map(center=center, zoom=20, layout=defaultLayout)

idx = 0

freq = 1/5 # itera 5 vezes por segundo
rsuGreen = False
obuWaiting = False
delayToGreen = 0 # number of iterations after the obu stopped waiting for green light
endDelayToGreen = 10/freq # 10 seconds -> 10/0.2 = 50 iterations
delayToMove = 0 # number of iterations after the rsu publishes demn (green light)
endDelayToMove = 2/freq # 2 seconds -> 2/0.2 = 10 iterations
endDelayToMove = randomIdx() # 1 to 4 seconds -> 5 to 20 iterations
leaderPressedGasPedal = False

#logging.basicConfig(level=logging.INFO)

mqtt.Client.connected_flag = False  # create flag in class

# brokers to connect
brokerRSU = "192.168.98.10"
brokerOBU1 = "192.168.98.20"
brokerOBU2 = "192.168.98.30"
brokerOBU3 = "192.168.98.40"

# topics
camTopic = "vanetza/in/cam"     # CAMs
denmTopic = "vanetza/in/denm"   # DENMs
cpmTopic = "vanetza/in/cpm"     # CPMs

# clients
clients = []
nClients = 4
for i in range(nClients):
    client_name = "client_" + str(i)
    client = mqtt.Client(client_name)  # create client instances
    clients.append(client)

# bind callback functions
for client in clients:
    client.on_log = on_log  # client logging
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.on_message = on_message
    client.on_subscribe = on_subscribe

connectClientToBroker(clients[0], brokerRSU)
connectClientToBroker(clients[1], brokerOBU1)
connectClientToBroker(clients[2], brokerOBU2)
connectClientToBroker(clients[3], brokerOBU3)

# subscribe
for client in clients:
    print("subscribing to " + camTopic)
    client.subscribe(camTopic)
    print("subscribing to " + denmTopic)
    client.subscribe(denmTopic)
    print("subscribing to " + cpmTopic)
    client.subscribe(cpmTopic)

# RSU ----------------------------------------------------------
# CAM
camRSUFilePath = "my_jsons/cam_rsu.json"
camRSUDataDict = jsonFile.toDict(camRSUFilePath)
camRSUDataDict["latitude"] = semaforo[0]
camRSUDataDict["longitude"] = semaforo[1]
jsonFile.writeFile(camRSUDataDict, "my_jsons", "cam_rsu.json")
camRSUDataStr = jsonFile.toStr(camRSUFilePath)
# DENM
denmRSUFilePath = "my_jsons/denm_rsu.json"
denmRSUDataStr = jsonFile.toStr(denmRSUFilePath)
# CPM
# cpmRSUFilePath = "my_jsons/cpm_rsu.json"
# cpmRSUDataDict = jsonFile.toDict(cpmRSUFilePath)
# cpmRSUDataDict["cpmParameters"]["managementContainer"]["stationType"] = 15
# cpmRSUDataDict["cpmParameters"]["managementContainer"]["referencePosition"]["latitude"] = semaforo[0]
# cpmRSUDataDict["cpmParameters"]["managementContainer"]["referencePosition"]["latitude"] = semaforo[1]
# cpmRSUDataDict["cpmParameters"]["stationDataContainer"]["originatingVehicleContainer"]["speed"]["speedValue"] = 0
# --------------------------------------------------------------

# OBUs ----------------------------------------------------------
# CAM
camOBUFilePath = "my_jsons/cam_obu.json"
camOBUDataDict = jsonFile.toDict(camOBUFilePath)
# CPM
# cpmOBUFilePath = "my_jsons/cpm_obu.json"
# cpmOBUDataDict = jsonFile.toDict(cpmOBUFilePath)
# --------------------------------------------------------------

# OBU 1 --------------------------------------------------------
# CAM
camOBUDataDict["stationID"] = 2
camOBUDataDict["latitude"] = positions[0][0]
camOBUDataDict["longitude"] = positions[0][1]
dirPath = "my_jsons"
fileName= "cam_obu1.json"
camOBU1filePath = dirPath + "/" + fileName
jsonFile.writeFile(camOBUDataDict, dirPath, fileName)
startIdxOBU1 = 0
# currSpeedOBU1 = 5
lastSpeedOBU1 = 5
# CPM
# ...
# map
markerOBU1 = Marker(location=inicio, draggable=False)
m.add_layer(markerOBU1)
# --------------------------------------------------------------

# OBU 2 --------------------------------------------------------
# CAM
camOBUDataDict["stationID"] = 3
camOBUDataDict["latitude"] = positions[0][0]
camOBUDataDict["longitude"] = positions[0][1]
dirPath = "my_jsons"
fileName= "cam_obu2.json"
camOBU2filePath = dirPath + "/" + fileName
jsonFile.writeFile(camOBUDataDict, dirPath, fileName)
startIdxOBU2 = startIdxOBU1 + randomIdx()
# print("startIdxOBU2 =", startIdxOBU2)
readyOBU2 = False
lastSpeedOBU2 = 5
# CPM
# ...
# map
markerOBU2 = Marker(location=inicio, draggable=False)
# m.add_layer(markerOBU2)
# --------------------------------------------------------------

# OBU 3 --------------------------------------------------------
# CAM
camOBUDataDict["stationID"] = 4
camOBUDataDict["latitude"] = positions[0][0]
camOBUDataDict["longitude"] = positions[0][1]
dirPath = "my_jsons"
fileName= "cam_obu3.json"
camOBU3filePath = dirPath + "/" + fileName
jsonFile.writeFile(camOBUDataDict, dirPath, fileName)
startIdxOBU3 = startIdxOBU2 + randomIdx()
# print("startIdxOBU3 =", startIdxOBU3)
readyOBU3 = False
lastSpeedOBU3 = 5
# CPM
# ...
# map
markerOBU3 = Marker(location=inicio, draggable=False)
# m.add_layer(markerOBU3)
# --------------------------------------------------------------

# map
m.save('htmls/map'+str(idx)+'.html')
m.remove_layer(markerOBU1)
# m.remove_layer(markerOBU2)
# m.remove_layer(markerOBU3)

idx += 1

while True:

    # RSU
    # print("----RSU publishing cam")
    print("\nRSU:")
    print("Publishing CAM")
    camRSURes = clients[0].publish(camTopic, camRSUDataStr)
    if not camRSURes[0]==0:
        break
    if obuWaiting:
        delayToGreen += 1
        if delayToGreen == endDelayToGreen:
            rsuGreen = True
            obuWaiting = False
            print("Publishing DENM")
            denmRSURes = clients[0].publish(denmTopic, denmRSUDataStr)
            if not denmRSURes[0]==0:
                break

    # OBU 1
    print("\nOBU 1:")
    dataDict = jsonFile.toDict(camOBU1filePath)
    currCoordinates = (dataDict["latitude"], dataDict["longitude"])
    if not rsuGreen:
        if distanceBetween(currCoordinates, semaforo) > 5:
            positionsIdxOBU1 += 1
            newCoordinates = (positions[positionsIdxOBU1][0], positions[positionsIdxOBU1][1])
            #
            newSpeed = 5
            updateCam(camOBU1filePath, dataDict, newCoordinates, newSpeed, lastSpeedOBU1)
            lastSpeedOBU1 = newSpeed
            #
            # dataDict["latitude"] = newCoordinates[0]
            # dataDict["longitude"] = newCoordinates[1]
            # dataDict["speed"] = 5
            # currSpeedOBU1 = dataDict["speed"]
            # dataDict["acceleration"] = (currSpeedOBU1 - lastSpeedOBU1) / freq
            # lastSpeedOBU1 = currSpeedOBU1
            # dataDict["brakePedal"] = False
            # dataDict["gasPedal"] = True
            #
            # print("OBU 1: coordinates =", newCoordinates, ", speed = 5 m/s")
            print("Percurso antes do semáforo")
            # map
            locationOBU1 = positions[positionsIdxOBU1]
        else:
            newSpeed = 0
            updateCam(camOBU1filePath, dataDict, currCoordinates, newSpeed, lastSpeedOBU1)
            lastSpeedOBU1 = newSpeed
            # dataDict["speed"] = 0
            # dataDict["brakePedal"] = True
            # dataDict["gasPedal"] = False
            # print("OBU 1: parou, coordinates =", currCoordinates, ", speed = 0 m/s")
            print("Parou")
            obuWaiting = True
            # map
            locationOBU1 = positions[positionsIdxOBU1]
    else:
        if delayToMove != endDelayToMove:
            delayToMove += 1 # apenas atualizado na OBU 1
            # print("OBU 1: delay to move, coordinates =", currCoordinates, ", speed = 0 m/s")
            print("Tempo de espera para reagir")
            # map
            locationOBU1 = positions[positionsIdxOBU1]
        else:
            leaderPressedGasPedal = True
            positionsIdxOBU1 += 1
            newCoordinates = (positions[positionsIdxOBU1][0], positions[positionsIdxOBU1][1])
            newSpeed = 5
            updateCam(camOBU1filePath, dataDict, newCoordinates, newSpeed, lastSpeedOBU1)
            lastSpeedOBU1 = newSpeed
            # dataDict["latitude"] = newCoordinates[0]
            # dataDict["longitude"] = newCoordinates[1]
            # dataDict["speed"] = 5
            # dataDict["brakePedal"] = False
            # dataDict["gasPedal"] = True
            # print("OBU 1: coordinates =", newCoordinates, ", speed = 5 m/s")
            print("Continuar percurso")
            # map
            locationOBU1 = positions[positionsIdxOBU1]    
    # jsonFile.updateFile(camOBU1filePath, dataDict)
    dataStr = jsonFile.toStr(camOBU1filePath)
    print("Publishing CAM: coordinates = (" + str(dataDict["latitude"]) + ", " + str(dataDict["longitude"]) + "), speed =", dataDict["speed"], "m/s")
    res = clients[1].publish(camTopic, dataStr)
    if not res[0]==0:
        break

    # OBU 2
    if idx == startIdxOBU2:
        readyOBU2 = True
    if readyOBU2:
        print("\nOBU 2:")
        dataDict = jsonFile.toDict(camOBU2filePath)
        currCoordinates = (dataDict["latitude"], dataDict["longitude"])
        if not rsuGreen:
            if distanceBetween(currCoordinates, locationOBU1) > 5:
                positionsIdxOBU2 += 1
                newCoordinates = (positions[positionsIdxOBU2][0], positions[positionsIdxOBU2][1])
                #
                newSpeed = 5
                updateCam(camOBU2filePath, dataDict, newCoordinates, newSpeed, lastSpeedOBU2)
                lastSpeedOBU2 = newSpeed
                #
                # dataDict["latitude"] = newCoordinates[0]
                # dataDict["longitude"] = newCoordinates[1]
                # dataDict["speed"] = 5
                # dataDict["brakePedal"] = False
                # dataDict["gasPedal"] = True
                #
                # print("OBU 2: coordinates =", newCoordinates, ", speed = 5 m/s")
                print("Percurso antes do semáforo")
                # map
                locationOBU2 = positions[positionsIdxOBU2]
            else:
                newSpeed = 0
                updateCam(camOBU2filePath, dataDict, currCoordinates, newSpeed, lastSpeedOBU2)
                lastSpeedOBU2 = newSpeed
                # dataDict["speed"] = 0
                # dataDict["brakePedal"] = True
                # dataDict["gasPedal"] = False
                # print("OBU 2: parou, coordinates =", newCoordinates, ", speed = 0 m/s")
                print("Parou")
                locationOBU2 = currCoordinates
        else:
            if not leaderPressedGasPedal:
                # print("OBU 2: delay to move, coordinates =", currCoordinates, ", speed = 0 m/s")
                print("Tempo de espera para OBU 1 reagir")
                # map
                locationOBU2 = positions[positionsIdxOBU2]
            else:
                positionsIdxOBU2 += 1
                newCoordinates = (positions[positionsIdxOBU2][0], positions[positionsIdxOBU2][1])
                newSpeed = 5
                updateCam(camOBU2filePath, dataDict, newCoordinates, newSpeed, lastSpeedOBU2)
                lastSpeedOBU2 = newSpeed
                # dataDict["latitude"] = newCoordinates[0]
                # dataDict["longitude"] = newCoordinates[1]
                # dataDict["speed"] = 5
                # dataDict["brakePedal"] = False
                # dataDict["gasPedal"] = True
                # print("OBU 2: coordinates =", newCoordinates, ", speed = 5 m/s")
                print("Continuar percurso")
                # map
                locationOBU2 = positions[positionsIdxOBU2]
        jsonFile.updateFile(camOBU2filePath, dataDict)
        dataStr = jsonFile.toStr(camOBU2filePath)
        # print("----OBU 2 publishing cam")
        print("Publishing CAM: coordinates = (" + str(dataDict["latitude"]) + ", " + str(dataDict["longitude"]) + "), speed =", dataDict["speed"], "m/s")
        res = clients[2].publish(camTopic, dataStr)
        if not res[0]==0:
            break

    # OBU 3
    if idx == startIdxOBU3:
        readyOBU3 = True
    if readyOBU3:
        print("\nOBU 3:")
        dataDict = jsonFile.toDict(camOBU3filePath)
        currCoordinates = (dataDict["latitude"], dataDict["longitude"])
        if not rsuGreen:
            if distanceBetween(currCoordinates, locationOBU2) > 5:
                positionsIdxOBU3 += 1
                newCoordinates = (positions[positionsIdxOBU3][0], positions[positionsIdxOBU3][1])
                #
                newSpeed = 5
                updateCam(camOBU3filePath, dataDict, newCoordinates, newSpeed, lastSpeedOBU3)
                lastSpeedOBU3 = newSpeed
                #
                # dataDict["latitude"] = newCoordinates[0]
                # dataDict["longitude"] = newCoordinates[1]
                # dataDict["speed"] = 5
                # dataDict["brakePedal"] = False
                # dataDict["gasPedal"] = True
                #
                # print("OBU 3: coordinates =", newCoordinates, ", speed = 5 m/s")
                print("Percurso antes do semáforo")
                # map
                locationOBU3 = positions[positionsIdxOBU3]
            else:
                newSpeed = 0
                updateCam(camOBU3filePath, dataDict, currCoordinates, newSpeed, lastSpeedOBU3)
                lastSpeedOBU3 = newSpeed
                # dataDict["speed"] = 0
                # dataDict["brakePedal"] = True
                # dataDict["gasPedal"] = False
                # print("OBU 3: parou, coordinates =", newCoordinates, ", speed = 0 m/s")
                print("Parou")
                locationOBU3 = currCoordinates
        else:
            if not leaderPressedGasPedal:
                # print("OBU 3: delay to move, coordinates =", currCoordinates, ", speed = 0 m/s")
                print("Tempo de espera para OBU 1 reagir")
                # map
                locationOBU3 = positions[positionsIdxOBU3]
            else:
                positionsIdxOBU3 += 1
                newCoordinates = (positions[positionsIdxOBU3][0], positions[positionsIdxOBU3][1])
                newSpeed = 5
                updateCam(camOBU3filePath, dataDict, newCoordinates, newSpeed, lastSpeedOBU3)
                lastSpeedOBU3 = newSpeed
                # dataDict["latitude"] = newCoordinates[0]
                # dataDict["longitude"] = newCoordinates[1]
                # dataDict["speed"] = 5
                # dataDict["brakePedal"] = False
                # dataDict["gasPedal"] = True
                # print("OBU 3: coordinates =", newCoordinates, ", speed = 5 m/s")
                print("Continuar percurso")
                # map
                locationOBU3 = positions[positionsIdxOBU3]
        jsonFile.updateFile(camOBU3filePath, dataDict)
        dataStr = jsonFile.toStr(camOBU3filePath)
        print("Publishing CAM: coordinates = (" + str(dataDict["latitude"]) + ", " + str(dataDict["longitude"]) + "), speed =", dataDict["speed"], "m/s")
        res = clients[3].publish(camTopic, dataStr)
        if not res[0]==0:
            break

    # map
    markerOBU1.location = locationOBU1
    m.add_layer(markerOBU1)

    if readyOBU2:
        markerOBU2.location = locationOBU2
        m.add_layer(markerOBU2)

    if readyOBU3:
        markerOBU3.location = locationOBU3
        m.add_layer(markerOBU3)

    m.save('htmls/map'+str(idx)+'.html')

    m.remove_layer(markerOBU1)

    if readyOBU2:
        m.remove_layer(markerOBU2)

    if readyOBU3:
        m.remove_layer(markerOBU3)

    # verificar se acaba
    if positions[positionsIdxOBU1] == fim:
        print("\nAcabou o percurso\n")
        break

    idx += 1

    print("\n--------------------------------------------------------------------------------------")
    time.sleep(freq)

for client in clients: 
    client.loop_stop()                  # stop loop
    client.disconnect()                 # disconnect