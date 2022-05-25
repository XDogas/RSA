mosquitto_pub -h 192.168.98.10 -t "vanetza/in/denm" -m \
"{
    \"management\": {
        \"actionID\": {
            \"originatingStationID\": 1798587532,
            \"sequenceNumber\": 0
        },
        \"detectionTime\": 1626453837.658,
        \"referenceTime\": 1626453837.658,
        \"eventPosition\": {
            \"latitude\": 40.637799251415686,
            \"longitude\": -8.652353364491056,
            \"positionConfidenceEllipse\": {
                \"semiMajorConfidence\": 0,
                \"semiMinorConfidence\": 0,
                \"semiMajorOrientation\": 0
            },
            \"altitude\": {
                \"altitudeValue\": 0,
                \"altitudeConfidence\": 1
            }
        },
        \"validityDuration\": 0,
        \"stationType\": 0
    },
    \"situation\": {
        \"informationQuality\": 7,
        \"eventType\": {
            \"causeCode\": 14,
            \"subCauseCode\": 14
        }
    }
}"
