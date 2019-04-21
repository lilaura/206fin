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
    
#Requesting airport data from Cirium Flight API
def get_airport_lst(APIid,APIkey):
    r=requests.get('https://api.flightstats.com/flex/airports/rest/v1/json/countryCode/US', params={'appId':APIid, 'appKey':APIkey})
    js=r.json()
    airport_lst=js['airports']
    return airport_lst


#Adding items to database
def add_airport_to_db(conn, cur, airport_lst):
    count = 0
    for airport in airport_lst:
        if count >= 20:
              print("Added 20 items to database; restart to add more")
              break
    
              #checking to see if dup data exists in database
        cur.execute('SELECT name FROM Airports WHERE name=?',(airport['name'],))
        try:
            data=cur.fetchone()[0]
            print ("Found in database")
            continue
        except:
            pass

        if airport['active']==1:
              cur.execute('INSERT INTO Airports (name, city, state, latitude, longitude, elevation, time_zone) VALUES (?,?,?,?,?,?,?)',(airport['name'],airport['city'],airport['stateCode'],airport['latitude'],airport['longitude'],airport['elevationFeet'],airport['timeZoneRegionName']))
              conn.commit()
              count+=1


#get longtitude and latitue from airport table in database

def add_weather_to_db(conn, cur):
    count = 0
    cur.execute('SELECT latitude, longitude FROM Airports')
    l = []
    for row in cur:
        l.append(row)
    for ro in l:
        lat = ro[0] 
        lng = ro[1]
        weatherurl = ("https://api.darksky.net/forecast/662c5daaecc7bc6892843b225162afac/{},{}").format(lat,lng)
        r1 = requests.get(weatherurl)
        count += 1
        data1 = json.loads(r1.text)
        lat2 = data1["latitude"]
        lng2 = data1["longitude"]
        time = data1["timezone"]
        precip = data1["daily"]["data"][0]["precipIntensity"]
        wind = data1["daily"]["data"][0]["windSpeed"]
        vis = data1["daily"]["data"][0]["visibility"]
        
        cur.execute('INSERT INTO Weather (latitude, longitude, time_zone, precip_int, wind_speed, visibility) VALUES(?, ?, ?, ?, ?, ?)', (lat2,lng2,time,precip,wind, vis))
    
    conn.commit()
    print(count)



if __name__ == "__main__":
    conn=sqlite3.connect('db_fin_new.sqlite')
    cur=conn.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS Airports (name TEXT, city TEXT, state TEXT, latitude REAL, longitude REAL, elevation REAL, time_zone TEXT)')
    cur.execute('CREATE TABLE IF NOT EXISTS Weather (latitude REAL, longitude REAL, time_zone TEXT, precip_int REAL, wind_speed REAL, visibility REAL)')
    get_airport_lst(flightAPI_id, flightAPI_key)
    airport_lst = get_airport_lst(flightAPI_id,flightAPI_key)
    add_airport_to_db(conn, cur, airport_lst)
    add_weather_to_db(conn, cur)
