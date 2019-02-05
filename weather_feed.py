#!/usr/bin/env python3
""" This script uses code from https://dzone.com/articles/playing-with-grafana-and-weather-apis """

import json
import requests
import credentials
from influxdb import InfluxDBClient

# instantiation of database connection
DB_SRV = {
    "host": "localhost",
    "username": credentials.username,
    "password": credentials.password,
    "database": "myHEMS",
}
db_client = InfluxDBClient(**DB_SRV)
db_client.create_database(DB_SRV["database"])

r = requests.get("http://api.openweathermap.org/data/2.5/weather?q=Berlin&appid={}&units=metric".format(credentials.owm_key))
data_in = json.loads(r.text)

data_out = [
    {
        "measurement": "weather",
        "tags": {
            "source": "openweathermap",
        },
        "time": data_in["dt"]*1000000000,
        "fields": {
            "temperature": float(data_in["main"]["temp"]),
            "humidity": float(data_in["main"]["humidity"])
        }
    }
]

#print(data_in)
#print(data_out)
db_client.write_points(data_out)