# Import statements
import matplotlib
import matplotlib.pyplot as plt
import sqlite3
import json
import unittest
import requests
import time





if __name__ == "__main__":
    conn=sqlite3.connect('db_fin_new.sqlite')
    cur=conn.cursor()
    
