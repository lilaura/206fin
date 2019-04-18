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
cur.execute('CREATE TABLE IF NOT EXISTS Airports (name TEXT, city TEXT, state TEXT, latitude REAL, longitude REAL, elevation REAL, active_status TEXT)')

#Requesting airport data from Cirium Flight API
r=requests.get('https://api.flightstats.com/flex/airports/rest/v1/json/countryCode/US', params={'appId':flightAPI_id, 'appKey':flightAPI_key})
js=r.json()
airport_lst=js['airports']
fw=open("airport_data.json",'w')
fw.write(fw)
fw.close()

#Adding items to database
count=0
for airport in airport_lst:
    if count>20:
        print("Added 20 items to database; restart to add more")
        break
    
    
    #checking to see if dup data exists in database
    cur.execute('SELECT * FROM Airports WHERE name=?',airport['name'])
    try:
        data=cur.fetchone()[0]
        print ("Found in database")
        continue
    except:
        pass


    cur.execute('INSERT INTO Flights (name, city, state, latitude, longitude, elevation, active_status) VALUES (?,?,?,?,?,?,?)',(airport['name'],airport['city'],airport['stateCode'],airport['latitude'],airport['longitude'],airport['elevation'],airport['active']))
    conn.commit()
    count+=1

if __name__ == "__main__":
    
    pass
