from pydoc_data.topics import topics
import paho.mqtt.client as mqtt
import time
import sys
import logging
import jsonFile

# client logging function
def on_log(client, userdata, level, buf):
    logging.info("log: " + buf)

# callback functions
def on_connect(client, userdata, flags, rc):
    if rc==0:
        client.connected_flag = True    # set flag
        logging.info("connected OK")
    else:
        logging.info("Bad connection returned code " + rc)
        client.loop_stop()

def on_disconnect(client, userdata, flags, rc=0):
    logging.info("disconnected result code " + str(rc))
    client.connected_flag = False

def on_subscribe(lient, userdata, mid, granted_qos):
    logging.info("subscribed")

def on_message(client, userdata, message):
    logging.info("message received: " + str(message.payload.decode("utf-8")))
    #logging.info("message topic =",message.topic)
    #logging.info("message qos =",message.qos)
    #logging.info("message retain flag =",message.retain)

logging.basicConfig(level=logging.INFO)

mqtt.Client.connected_flag = False  # create flag in class

broker = "192.168.98.10"            # broker to connect
topic = "vanetza/in/cam"            # CAMs
client = mqtt.Client()              # create new instance

client.on_log = on_log             # client logging

# bind callback functions
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_message = on_message
client.on_subscribe = on_subscribe

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

print("subscribing to " + topic)
client.subscribe(topic)

filePath = "my_jsons/cam_rsu.json"
dataStr = jsonFile.toStr(filePath)

while True:
    print("publishing")
    # res = client.publish(topic, '{"accEngaged": true,"acceleration": 0,"altitude": 800001,"altitudeConf": 15,"brakePedal": true,"collisionWarning": true,"cruiseControl": true,"curvature": 1023,"driveDirection": "FORWARD","emergencyBrake": true,"gasPedal": false,"heading": 3601,"headingConf": 127,"latitude": 400000000,"length": 100,"longitude": -80000000,"semiMajorConf": 4095,"semiMajorOrient": 3601,"semiMinorConf": 4095,"specialVehicle": {"publicTransportContainer": {"embarkationStatus": false}},"speed": 16383,"speedConf": 127,"speedLimiter": true,"stationID": 1,"stationType": 15,"width": 30,"yawRate": 0}')
    res = client.publish(topic, dataStr)
    if not res[0]==0:
        break
    time.sleep(0.1)
    
client.loop_stop()                  # stop loop
client.disconnect()                 # disconnect