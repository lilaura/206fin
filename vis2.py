# Import statements
import matplotlib
import matplotlib.pyplot as plt
import sqlite3
import json
import requests
import time

def write_calculation(calc_file, calc_dict):

    dumped_json = json.dumps(calc_dict) # serialize dictionary to a JSON formatted string 
    fw = open(calc_file,"w") # open the cache file
    fw.write(dumped_json) # write the JSON
    fw.close() 

def calc_avg_elev(conn, cur):
    cur.execute('SELECT state, elevation FROM Airports ORDER BY state')
    avg_elev={}
    for row in cur:
        state=row[0]
        elevation=row[1]
        avg_elev[state]=avg_elev.get(state,[])+([elevation])
    for key in avg_elev:
        avg_elev[key]=sum(avg_elev[key])/len(avg_elev[key])
    return avg_elev

<<<<<<< HEAD
def avg_temp(conn,cur):
    d = {}
    templist = []
    preciplist = []
    vislist = []
    lnglist = []
    latlist = []
    windlist = []
    cur.execute('SELECT temp_high, temp_low,latitude, longitude, precip_int, wind_speed, visibility from Weather')
    for row in cur:
        templist.append((row[0]+row[1])/2)
        preciplist.append(row[4])
        vislist.append(row[6])
        latlist.append(row[2])
    d["longitude"] = lnglist
    d["latitude"] = latlist
    d["temprature"] = templist
    d["visibility"] = vislist
    d["precipitation"] = preciplist
    d["wind speed"] = windlist
=======
def sort_elev_top_ten(avg_elev):
    top_sort=sorted(avg_elev.items(),key=lambda t: t[1],reverse=True)
    return top_sort[:10]
>>>>>>> 45d036be9d20bfc3baf1ddc2ad70aa1ca0c7cf8e

def barchart_avg_elev_by_state(top_elev_dict):
    x=[]
    y=[]
    for item in top_elev_dict:
        x.append(item[0])
        y.append(item[1])
    fig, ax=plt.subplots()
    ax.bar(x,y)
    ax.set_xlabel('State')
    ax.set_ylabel('Average elevation of all airports')
    ax.set_title('Top10 States in average airport elevation')
    fig.savefig('Top10 States in average airport elevation.png')
    plt.show()


if __name__ == "__main__":
    conn=sqlite3.connect('db_fin_new.sqlite')
    cur=conn.cursor()
    calc_avg_elev(conn,cur)
    elev_dict=calc_avg_elev(conn,cur)
    top_elev_dict=sort_elev_top_ten(elev_dict)
    #write_calculation("calc.json",elev_dict)
    barchart_avg_elev_by_state(top_elev_dict)
