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

mqtt.Client.connected_flag = False  # create flag in class

brokerRSU = "192.168.98.10"
brokerOBU1 = "192.168.98.20"
brokerOBU2 = "192.168.98.30"
brokerOBU3 = "192.168.98.40"

# topics
camTopic = "vanetza/in/cam"     # CAMs
denmTopic = "vanetza/in/denm"   # DENMs
cpmTopic = "vanetza/in/cpm"     # CPMs

client1 = mqtt.Client()
client2 = mqtt.Client()
client3 = mqtt.Client()

client1.on_log = on_log  # client logging
client1.on_connect = on_connect
client1.on_disconnect = on_disconnect
client1.on_message = on_message
client1.on_subscribe = on_subscribe
client2.on_log = on_log  # client logging
client2.on_connect = on_connect
client2.on_disconnect = on_disconnect
client2.on_message = on_message
client2.on_subscribe = on_subscribe
client3.on_log = on_log  # client logging
client3.on_connect = on_connect
client3.on_disconnect = on_disconnect
client3.on_message = on_message
client3.on_subscribe = on_subscribe

connectClientToBroker(client1, brokerRSU)
connectClientToBroker(client2, brokerOBU1)
connectClientToBroker(client3, brokerOBU2)

client1.subscribe(camTopic)
client2.subscribe(camTopic)
client2.subscribe(cpmTopic)
client3.subscribe(camTopic)
client3.subscribe(cpmTopic)


# # RSU
# camRSUFilePath = "my_jsons/cam_rsu.json"
# camRSUDataDict = jsonFile.toDict(camRSUFilePath)
# # camRSUDataDict["latitude"] = semaforo[0]
# # camRSUDataDict["longitude"] = semaforo[1]
# jsonFile.writeFile(camRSUDataDict, "my_jsons", "cam_rsu.json")
# camRSUDataStr = jsonFile.toStr(camRSUFilePath)
# denmRSUFilePath = "my_jsons/denm_rsu.json"
# denmRSUDataStr = jsonFile.toStr(denmRSUFilePath)

# # OBUs
# camOBUFilePath = "my_jsons/cam_obu.json"
# camOBUDataDict = jsonFile.toDict(camOBUFilePath)

# # OBU 1
# camOBUDataDict["stationID"] = 2
# # camOBUDataDict["latitude"] = positions[0][0]
# # camOBUDataDict["longitude"] = positions[0][1]
# dirPath = "my_jsons"
# fileName= "cam_obu1.json"
# camOBU1filePath = dirPath + "/" + fileName
# jsonFile.writeFile(camOBUDataDict, dirPath, fileName)
# camOBU1DataStr = jsonFile.toStr(camOBU1filePath)

# OBUs
cpmOBUFilePath = "my_jsons/cpm_obu.json"
cpmOBUDataDict = jsonFile.toDict(cpmOBUFilePath)

# OBU 1
cpmOBU1FilePath = "my_jsons/cpm_obu1.json"
cpmOBU1DataDict = jsonFile.toDict(cpmOBU1FilePath)
cpmOBU1DataDict["cpmParameters"]["managementContainer"]["referencePosition"]["latitude"] = 10
cpmOBU1DataDict["cpmParameters"]["managementContainer"]["referencePosition"]["longitude"] = 10
cpmOBU1DataDict["cpmParameters"]["stationDataContainer"]["originatingVehicleContainer"]["speed"]["speedValue"] = 5
cpmOBU1DataDict["cpmParameters"]["numberOfPerceivedObjects"] = 0

# cpmOBU1DataDict["cpmParameters"]["perceivedObjectContainer"]["xDistance"]["value"] = distanceBetween(...)
# cpmOBU1DataDict["cpmParameters"]["perceivedObjectContainer"]["yDistance"]["value"] = 0
# cpmOBU1DataDict["cpmParameters"]["perceivedObjectContainer"]["xSpeed"]["value"] = velocidade do veiculo à frente
# cpmOBU1DataDict["cpmParameters"]["perceivedObjectContainer"]["ySpeed"]["value"] = 0
dirPath = "my_jsons"
fileName = "cpm_obu1.json"
jsonFile.writeFile(cpmOBU1DataDict, dirPath, fileName)
cpmOBU1DataStr = jsonFile.toStr(cpmOBU1FilePath)


# OBU 2
cpmOBUDataDict["cpmParameters"]["managementContainer"]["referencePosition"]["latitude"] = 10
cpmOBUDataDict["cpmParameters"]["managementContainer"]["referencePosition"]["longitude"] = 10
cpmOBUDataDict["cpmParameters"]["stationDataContainer"]["originatingVehicleContainer"]["speed"]["speedValue"] = 5
cpmOBUDataDict["cpmParameters"]["numberOfPerceivedObjects"] = 1
cpmOBUDataDict["cpmParameters"]["perceivedObjectContainer"][0]["objectID"] = 0 # 0, 1, 2, 3 ou 4, ver no wireshark o que são
cpmOBUDataDict["cpmParameters"]["perceivedObjectContainer"][0]["xDistance"]["value"] = -1
# cpmOBUDataDict["cpmParameters"]["perceivedObjectContainer"]["yDistance"]["value"] = 0
# cpmOBUDataDict["cpmParameters"]["perceivedObjectContainer"]["xSpeed"]["value"] = velocidade do veiculo à frente
# cpmOBUDataDict["cpmParameters"]["perceivedObjectContainer"]["ySpeed"]["value"] = 0
dirPath = "my_jsons"
fileName = "cpm_obu2.json"
cpmOBU2FilePath = dirPath + "/" + fileName
jsonFile.writeFile(cpmOBUDataDict, dirPath, fileName)
cpmOBU2DataStr = jsonFile.toStr(cpmOBU2FilePath)


while True:
    # print("----RSU Publishing cam")
    # camRSURes = client1.publish(camTopic, camRSUDataStr)
    # if not camRSURes[0]==0:
    #     break
    # print("----OBU 1 Publishing cam")
    # camRSURes = client2.publish(camTopic, camOBU1DataStr)
    # if not camRSURes[0]==0:
    #     break
    print("----OBU 1 Publishing CPM")
    camRSURes = client2.publish(cpmTopic, cpmOBU1DataStr)
    if not camRSURes[0]==0:
        break
    print("----OBU 2 Publishing CPM")
    camRSURes = client3.publish(cpmTopic, cpmOBU2DataStr)
    if not camRSURes[0]==0:
        break
    # print("----OBU 2 Publishing cam")
    # camRSURes = client3.publish(camTopic, camOBU2DataStr)
    # if not camRSURes[0]==0:
    #     break

    print()
    time.sleep(5)


client1.loop_stop()                  # stop loop
client1.disconnect()                 # disconnect