mosquitto_pub -h 192.168.98.20 -t "vanetza/in/cam" -m \
"{
    \"accEngaged\": true,
    \"acceleration\": 0,
    \"altitude\": 800001,
    \"altitudeConf\": 15,
    \"brakePedal\": true,
    \"collisionWarning\": true,
    \"cruiseControl\": true,
    \"curvature\": 1023,
    \"driveDirection\": \"FORWARD\",
    \"emergencyBrake\": true,
    \"gasPedal\": false,
    \"heading\": 3601,
    \"headingConf\": 127,
    \"latitude\": 400000000,
    \"length\": 100,
    \"longitude\": -80000000,
    \"semiMajorConf\": 4095,
    \"semiMajorOrient\": 3601,
    \"semiMinorConf\": 4095,
    \"specialVehicle\": {
        \"publicTransportContainer\": {
            \"embarkationStatus\": false
        }
    },
    \"speed\": 16383,
    \"speedConf\": 127,
    \"speedLimiter\": true,
    \"stationID\": 2,
    \"stationType\": 5,
    \"width\": 30,
    \"yawRate\": 0
}"