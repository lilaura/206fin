# Import statements
import matplotlib
import matplotlib.pyplot as plt
import sqlite3
import json
import unittest
import requests
import time


def calc_avg_elev(conn, cur,):
    cur.execute('SELECT state, elevation FROM Airports ORDER BY state')
    d={}
    for row in cur:
        state=row[0]
        elevation=row[1]
        d[state]=d.get(state,[]).append(elevation)
    for key in d:
        d[key]=sum(d[key])/len(d[key])
    return d

def 



if __name__ == "__main__":
    conn=sqlite3.connect('db_fin_new.sqlite')
    cur=conn.cursor()
    
