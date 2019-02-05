import json
import statistics
import datetime
import sys

from influxdb import InfluxDBClient

import credentials

allowable_time_deviation = 3000

starting_time_input = "2019-02-03 00:00:00"
ending_time_input = "2019-02-03 07:45:00"

room = "bath"

def main():
    host = 'localhost'
    port = 8086
    username = credentials.username
    password = credentials.password
    dbname = 'myHEMS'
    if(room == "Living" or room == "Living room" or room == "living"):
        measurement1 = '"temperature"'
        measurement2 = '"temperature2"'
    elif(room == "bath" or room == "Bath" or room == "Bathroom"):
        measurement1 = '"bathroom-temp"'
        measurement2 = '"bathroom-temp2"'
    else:
        print("Room name not valid!")
        sys.exit        
    # range_last_x_seconds = 120
    # starting_time = datetime.datetime.now()-datetime.timedelta(hours=1, seconds=range_last_x_seconds)
    starting_time = datetime.datetime.strptime(starting_time_input, "%Y-%m-%d %H:%M:%S")
    starting_time = starting_time.isoformat()
    ending_time = datetime.datetime.strptime(ending_time_input, "%Y-%m-%d %H:%M:%S")
    ending_time = ending_time.isoformat()
    query1 = "select * from %s where time >= '%sZ' and time <= '%sZ'" % (measurement1, starting_time, ending_time)
    query2 = "select * from %s where time >= '%sZ' and time <= '%sZ'" % (measurement2, starting_time, ending_time)

    client = InfluxDBClient(host, port, username, password, dbname)

    result1 = client.query(query1, epoch='ms') 
    result2 = client.query(query2, epoch='ms') 

    # pointstest1 = result1.get_points()
    # pointstest2 = result2.get_points()
    # for p in pointstest1:
    #     print(p['value'], p['time'])
    # print() 
    # for p in pointstest2:
    #     print(p['value'], p['time']) 
    # print()          

    points1 = result1.get_points()
    points2 = result2.get_points()
    list_temperature_a = list(points1)
    list_temperature_r = list(points2)
    # print(list_temperature_a)
    # print(list_temperature_r)
    temperature_deltas = []

    for p in list_temperature_a:
        # print(p['value'], p['time'])
        temp2 = find_similar_time_value(p['time'], list_temperature_r)
        try:
            temp_delta = temp2 - p['value']
            temp_delta_time = (temp_delta, p['time'])
            temperature_deltas.append(temp_delta_time)
            # print("%.1f" % temp_delta)
        except:
            None# print("No data available")

    heat_usage = 0.0
    previous_time = 0
    previous_delta = 0.0

    for i in temperature_deltas:
        if(previous_time <= 0):
            previous_time = i[1]
            continue
        else:
            time_delta = i[1] - previous_time
            print("time delta is %.1f in [s]" % (time_delta/1000))
            temp_delta_avg = (previous_delta + i[0]) / 2
            heat_increment = time_delta/1000 * temp_delta_avg
            heat_usage += heat_increment
            print("Heat increment is %.1f, accumulated heat is %.0f" % (heat_increment, heat_usage))
            previous_time = i[1]
    
    print()
    print("The heat usage between \n%s and \n%s has been \n%i FHU ('fictitious heat units')" % (starting_time_input, ending_time_input, heat_usage))


def find_similar_time_value(p1_time, list_temperature_r):
    for p in list_temperature_r:
        if (abs(p1_time - p['time']) <= allowable_time_deviation):
            return p['value']
        else:
            continue


main()