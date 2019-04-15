# Import statements
import matplotlib
import matplotlib.pyplot as plt
import sqlite3
import json
import unittest
import requests
import time

#For Cirium Flight API
flight_id="8ab51357"
flight_key="92daab56f079dc523afab96f0a5ef06a"

#Connecting the database
conn=sqlite3.connect('db_fin.sqlite')
cur=conn.cursor()

#Setting up the table
cur.execute('CREATE TABLE IF NOT EXISTS Flights (year TEXT, month TEXT, day TEXT, hour TEXT, scheduled_gate_dep TIMESTAMP, actual_gate_dep TIMESTAMP)')

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
    r=requests.get('https://api.flightstats.com/flex/flightstatus/historical/rest/v3/json/airport/status/DTW/dep/2019/4/{}/{}'.format(days[i],hours[i]),params={'appId':flight_id, 'appKey':flight_key, 'utc':False, 'numHours':'1', 'maxFlights':'20'})
    s=r.json()




print("Pausing for a bit...")
time.sleep(10 )


if __name__ == "__main__":
    
    pass
