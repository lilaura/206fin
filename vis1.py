# Import statements
import matplotlib
import matplotlib.pyplot as plt
import sqlite3
import json
import unittest
import requests
import time

#For Cirium Flight API
flightAPI_id="8ab51357"
flightAPI_key="92daab56f079dc523afab96f0a5ef06a"

#Connecting the database
conn=sqlite3.connect('db_fin.sqlite')
cur=conn.cursor()

#Setting up the table
cur.execute('CREATE TABLE IF NOT EXISTS Flights (day TEXT, hour TEXT, flight_id TEXT, scheduled_runway_dep TIMESTAMP, actual_runway_dep TIMESTAMP, scheduled_runway_arr TIMESTAMP, actual_runway_arr TIMESTAMP)')

#define read_cache and write_cache functions
def read_cache(cache_file):
    fr=open(cache_file)
    s=fr.read()
    d=json.loads(s)
    fr.close()
    return d

def write_cache(cache_file,cache_d):
    fw=open(cache_file,"w")
    js=json.dumps(cache_d)
    fw.write(js)
    fw.close()

#Create days and hours lists to plug in requests url
days=[]
for i in range(1,6):
    for n in range(0,24):
        days.append(str(i))
hours=[]
for i in range(0,24):
    hours.append(str(i))
hours=hours*5

#Requesting historical flight data from Cirium Flight API; departing from DTW, 120hrs starting from 19-04-01T00:00
for i in range(120):
    r=requests.get('https://api.flightstats.com/flex/flightstatus/historical/rest/v3/json/airport/status/DTW/dep/2019/4/{}/{}'.format(days[i],hours[i]),params={'appId':flightAPI_id, 'appKey':flightAPI_key, 'utc':'False', 'numHours':'1', 'maxFlights':'20'})
    dict=r.json()
    
    #checking to see if dup data exists in database
    for flight in dict['flightStatuses']:
        cur.execute('SELECT * FROM Flights WHERE flight_id=?',flight['flightId'])
        try:
            data=cur.fetchone()[0]
            print ("Found in database")
            continue
        except:
            pass

#variables to add to database; I captured UTC time just b/c it will be easier to calculate scheduled vs. actual air time; when requesting data it was still DTW local time used; we can change that tho, or just look at heathrow
        day=dict['day']['requested']
        hour=dict['hour']['requested']
        flight_id=flight['flightId']
        scheduled_runway_dep=flight['scheduledRunwayDeparture']['dateUtc']
        actual_runway_dep=flight['actualRunwayDeparture']['dateUtc']
        scheduled_runway_arr=flight['actualRunwayDeparture']['dateUtc']
        actual_runway_arr=flight['actualRunwayDeparture']['dateUtc']

        cur.execute('INSERT INTO Flights (day, hour, flight_id, scheduled_runway_dep, actual_runway_dep, scheduled_runway_arr, actual_runway_arr) VALUES (?,?,?,?,?,?,?)',(day,hour,flight_id,scheduled_runway_dep,actual_runway_dep,scheduled_runway_arr,actual_runway_arr))
        conn.committ


    print("Pausing for a bit...")
    time.sleep(10)


if __name__ == "__main__":
    
    pass
