import win32com.client as win32
from datetime import datetime
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import psycopg2 
import time

import os
import operator
olmailitem = 0x0

olApp = win32.Dispatch('outlook.Application')
# olNS = olApp.GetNameSpace('MAPI')
mailItem = olApp.CreateItem(0)

times = datetime.now().strftime('%#d %b %Y %H:%M:%S')
timesY = datetime.now().strftime(' %Y ')


Limit = [1.3,2,3,4]

try:
    connection = psycopg2.connect(user="admin",
                                  password="Ab123456",
                                  host="191.191.2.179",
                                  port="5432",
                                  database="Totle-2nd-Mask")
    connection
    Postgres_select = "select * from cpk_data ORDER BY id ASC"
    cursor = connection.cursor()
    cursor.execute(Postgres_select)
    data = cursor.fetchall()
    # print(data[1])
    staus = True
except(Exception, psycopg2.Error) as error:
    print("Error while select data from PostgresSQL :", error) 
    staus = False

for x in data :
    # print(x)
    F = float(x[2])
    F1 = float(x[3])
    if (F >= 7 or F1 >= 3) :
        print('ee')
    else:
        print(x[2])