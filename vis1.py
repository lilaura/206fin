# Import statements
import matplotlib
import matplotlib.pyplot as plt
import sqlite3
import json
import unittest
import requests
import datetime

#For Lufthansa API
flight_key="zejvcb5vfcub7kyb22jv5grm"
flight_secret="7MYH4x8aRS"

#Getting access token from Lufthansa
r_token=requests.post('https://api.lufthansa.com/v1/oauth/token',data={
                     'client_id':flight_key,
                     'client_secret':flight_secret,
                     'grant_type':'client_credentials'
                     })

s_token=r_token.json()
access_token=s_token['access_token']

#Generating date stings
#TO BE UPDATED
date_lst=[]
for i in range(1,32):
    date=datetime.datetime(2019,1,i)
    date_lst.append(date)

#Connecting the database
conn1=sqlite3.connect('Lufthansa.sqlite')
cur1=conn1.cursor()

#Setting up the table
cur1.execute('DROP TABLE IF EXISTS Fares')
cur1.execute('CREATE TABLE Fares (origin TEXT, destination TEXT, travel_date TIMESTAMP, cabin TEXT, adult_traveler INTEGER)')

#Requesting flight fare data from Lufthansa API
#at least 100 rows?
#the best way to limit number of requests each time?


if __name__ == "__main__":
    
    pass
