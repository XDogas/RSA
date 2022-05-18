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

broker = "192.168.98.30"            # broker to connect
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

filePath = "my_jsons/cam.json"

while True:
    dataDict = jsonFile.toDict(filePath)
    print("latitude ======================================================================", dataDict["latitude"]) # DEBUG
    jsonFile.setValue(filePath, "latitude", dataDict["latitude"]+1)
    dataStr = jsonFile.toStr(filePath)
    print("publishing")
    res = client.publish(topic, dataStr)
    if not res[0]==0:
        break
    time.sleep(1)
    
client.loop_stop()                  # stop loop
client.disconnect()                 # disconnect