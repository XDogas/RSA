import paho.mqtt.client as mqtt

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("$SYS/#")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))

broker_address="192.168.98.10" # ADICIONEI

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

# client.connect("mqtt.eclipseprojects.io", 1883, 60)
client.connect(broker_address, 1883, 60) # ADICIONEI EM VEZ DA LINHA ANTERIOR (VER SE SE TIRA OS 2 ULTIMOS ARGS)

client.publish('{"accEngaged": true,"acceleration": 0,"altitude": 800001,"altitudeConf": 15,"brakePedal": true,"collisionWarning": true,"cruiseControl": true,"curvature": 1023,"driveDirection": "FORWARD","emergencyBrake": true,"gasPedal": false,"heading": 3601,"headingConf": 127,"latitude": 400000000,"length": 100,"longitude": -80000000,"semiMajorConf": 4095,"semiMajorOrient": 3601,"semiMinorConf": 4095,"specialVehicle": {"publicTransportContainer": {"embarkationStatus": false}},"speed": 16383,"speedConf": 127,"speedLimiter": true,"stationID": 1,"stationType": 15,"width": 30,"yawRate": 0}') # ADICIONEI MAS ESTÁ MAL

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()