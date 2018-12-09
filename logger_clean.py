#!/usr/bin/env python3
#from https://gist.github.com/jasonmhite/c2d9766dc27facf642b2

import paho.mqtt.client as mqtt
from influxdb import InfluxDBClient

TOPIC = "/sensors/#"

DB_SRV = {
    "host": "localhost",
    "username": "***",
    "password": "***",
    "database": "myHEMS",
}

icli = InfluxDBClient(**DB_SRV)

######## Handlers for each sensor class
#
#def handle_ds18b20(sid, data):
#    payload = [{
#        "measurement": "temperature",
#        "tags": {"id": sid},
#        "fields": {"value": float(data)},
#    }]
#    return payload
#
#def handle_dht22(sid, data):
#    error_code, temp, humid = data.split()
#    payload = [
#        {
#            "measurement": "temperature",
#            "tags": {"id": sid, "err": error_code},
#            "fields": {"value": float(temp)},
#        },
#        {
#            "measurement": "humidity",
#            "tags": {"id": sid, "err": error_code},
#            "fields": {"value": float(humid)},
#        }
#    ]
#    return payload
#
#def handle_dht22_bare(sid, data):
#    temp, humid = data.split()
#    payload = [
#        {
#            "measurement": "temperature",
#            "tags": {"id": sid},
#            "fields": {"value": float(temp)},
#        },
#        {
#            "measurement": "humidity",
#            "tags": {"id": sid},
#            "fields": {"value": float(humid)},
#        }
#    ]
#    return payload
#
#def handle_light(sid, data):
#    light = int(data)
#    if light < 0 or light > 3000:
#        light = 3000
#    payload = [
#        {
#            "measurement": "light",
#            "tags": {"id": sid},
#            "fields": {"value": light}
#        }
#    ]
#    return payload
#
#handlers = {
#    "temp2": {
#        "temp": handle_dht22_bare,
#    },
#    "temp3": {
#        "temp": handle_dht22_bare,
#        "light": handle_light,
#    },
#}

#def dispatch(msg):
#    topic = str(msg.topic)
#    path = topic.split('/')
#    
#    # Topics are of form sensors/<sensor unique name>/<measurement type>
#
#    measurement_type = path[-1]
#    sensor_id = path[-2]
#
#    data = msg.payload
#
#    try:
#        handler = handlers[sensor_id][measurement_type]
#        payload = handler(sensor_id, data)
#        return payload
#    except KeyError:
#        print("-> No parser associated with {}/{}".format(sensor_id, measurement_type))
#        return None

def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT broker")
    client.subscribe(TOPIC)

def on_message(client, userdata, msg):
    print(str(msg.topic), str(msg.payload))

#   payload = dispatch(msg)
    if "temperature" in msg.topic:
        payload = [
            {
                "measurement": "temperature",
                "tags": {"id": "dht22temp"},
                "fields": {"value": float(msg.payload)},
            }
        ]

        if payload is not None:
            icli.write_points(payload)
    

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect('maxpi', 1883, 60)


client.loop_forever()