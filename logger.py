#!/usr/bin/env python3

import paho.mqtt.client as mqtt
from influxdb import InfluxDBClient

TOPIC = "/sensors/#"

DB_SRV = {
    "host": "localhost",
    "username": "max",
    "password": "myHEMSJolt",
    "database": "myHEMS",
}

icli = InfluxDBClient(**DB_SRV)

#functions

def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT broker")
    client.subscribe(TOPIC)

def on_message(client, userdata, msg):
    print(str(msg.topic), str(msg.payload))

# what will be done with a temperature message
    if "dht22/temperature" in msg.topic:
        payload = [
            {
                "measurement": "temperature",
                "tags": {"id": "dht22temp"},
                "fields": {"value": float(msg.payload)},
            }
        ]
        if payload is not None:
            icli.write_points(payload)

# what will be done with a humidity message
    if "dht22/humidity" in msg.topic:
        payload = [
            {
                "measurement": "humidity",
                "tags": {"id": "dht22humid"},
                "fields": {"value": float(msg.payload)},
            }
        ]
        if payload is not None:
            icli.write_points(payload)
    
# what will be done with a temperature2 message
    if "DS18B20" in msg.topic:
        payload = [
            {
                "measurement": "temperature2",
                "tags": {"id": "ds18b20_temp"},
                "fields": {"value": float(msg.payload)},
            }
        ]
        if payload is not None:
            icli.write_points(payload)

# what will be done with a temperature2 message
    if "DS18B20" in msg.topic:
        payload = [
            {
                "measurement": "temperature2",
                "tags": {"id": "ds18b20_temp"},
                "fields": {"value": float(msg.payload)},
            }
        ]
        if payload is not None:
            icli.write_points(payload)

# what will be done with a bme-1/bathroom-temp message
    if "bme280-1/temperature" in msg.topic:
        payload = [
            {
                "measurement": "bathroom-temp",
                "tags": {"id": "bathroom_temp"},
                "fields": {"value": float(msg.payload)},
            }
        ]
        if payload is not None:
            icli.write_points(payload)

# what will be done with a bme-1/bathroom-humid message
    if "bme280-1/humidity" in msg.topic:
        payload = [
            {
                "measurement": "bathroom-humidity",
                "tags": {"id": "bathroom-humidity"},
                "fields": {"value": float(msg.payload)},
            }
        ]
        if payload is not None:
            icli.write_points(payload)

# what will be done with a bme-1/bathroom-airpressure message
    if "bme280-1/airpressure" in msg.topic:
        payload = [
            {
                "measurement": "bathroom-airpressure",
                "tags": {"id": "bathroom-airpressure"},
                "fields": {"value": float(msg.payload)},
            }
        ]
        if payload is not None:
            icli.write_points(payload)

# what will be done with a bme-2/bathroom-temp message
    if "bme280-2/temperature" in msg.topic:
        payload = [
            {
                "measurement": "bathroom-temp2",
                "tags": {"id": "bathroom_temp2"},
                "fields": {"value": float(msg.payload)},
            }
        ]
        if payload is not None:
            icli.write_points(payload)

# what will be done with a bme-2/bathroom-humid message
    if "bme280-2/humidity" in msg.topic:
        payload = [
            {
                "measurement": "bathroom-humidity2",
                "tags": {"id": "bathroom-humidity2"},
                "fields": {"value": float(msg.payload)},
            }
        ]
        if payload is not None:
            icli.write_points(payload)

# what will be done with a bme-2/bathroom-airpressure message
    if "bme280-2/airpressure" in msg.topic:
        payload = [
            {
                "measurement": "bathroom-airpressure2",
                "tags": {"id": "bathroom-airpressure2"},
                "fields": {"value": float(msg.payload)},
            }
        ]
        if payload is not None:
            icli.write_points(payload)            


#execution

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect('maxpi', 1883, 60)


client.loop_forever()