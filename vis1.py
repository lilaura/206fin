# Import statements
import matplotlib
import matplotlib.pyplot as plt
import sqlite3
import json
import unittest
import requests

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

#Connecting the database
conn=sqlite3.connect('Lufthansa.sqlite')
cur=conn.cursor()



#Getting data from Lufthansa API


if __name__ == "__main__":
    
    pass
