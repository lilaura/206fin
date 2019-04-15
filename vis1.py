# Import statements
import matplotlib
import matplotlib.pyplot as plt
import sqlite3
import json
import unittest
import requests
import datetime

#For Cirium Flight API
flight_id="8ab51357"
flight_key="92daab56f079dc523afab96f0a5ef06a"

#Generating date stings
#TO BE UPDATED
date_lst=[]
for i in range(1,32):
    date=datetime.datetime(2019,1,i)
    date_lst.append(date)

#Connecting the database
conn=sqlite3.connect('db_fin.sqlite')
cur=conn.cursor()

#Setting up the table
cur.execute('CREATE TABLE IF NOT EXISTS Flights (year TEXT, month TEXT, day TEXT, hour TEXT, scheduled_gate_dep TIMESTAMP, actual_gate_dep TIMESTAMP)')

#Requesting historical flight data from Cirium Flight API; departing from DTW, 120hrs starting from 19-04-01T00:00




if __name__ == "__main__":
    
    pass
