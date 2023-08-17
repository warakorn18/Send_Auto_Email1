import win32com.client as win32
from datetime import datetime
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import psycopg2 
import time
import os


olmailitem = 0x0

olApp = win32.Dispatch('outlook.Application')
# olNS = olApp.GetNameSpace('MAPI')
mailItem = olApp.CreateItem(0)

times = datetime.now().strftime('%#d %b %Y %H:%M:%S')
timesY = datetime.now().strftime(' %Y ')

# Email User
User = 'warakorn.sup@murata.com;'


Limit_CPK = '7'
# print(type(Limit_CPK))

#Program Code Chaer
try:
    connection = psycopg2.connect(user="admin",
                                    password="Ab123456",
                                    host="191.191.2.179",
                                    port="5432",
                                    database="Totle-2nd-Mask")
    connection

    cursor = connection.cursor()
    cursor.execute("select * from cpk_data ORDER BY id ASC" )
    print("Select Database From CPK_Data ORDER BY ID ASC")


    # # print(email())
    df = pd.DataFrame(cursor)
    df.to_csv("AAA.csv",index=False)
    rd = pd.read_csv("AAA.csv",index_col=False)
    rd.reset_index(drop=True)


    x = 'ECASD60J337M009KA0+C001/K803'
    rd = rd.loc[rd['6'] == x]


    # Data for plotting
    Id = rd['0']
    Lot = rd['1']
    front_pos = rd['2']
    front_width = rd['3']
    back_pos = rd['4']
    back_width = rd['5']
    partname = rd['6']
 
   
    Lot_filter = np.array(Lot)
    partname_filter = np.array(partname)
    
    L = ', '.join(Lot_filter)
    partname_join = ', '.join(partname_filter)

    print(L)
    print(partname_join)
    staus = True
except:
    print('Postgres Connect Failed :', E)
    staus = False


# print(Lot_filter)

fig1, ax = plt.subplots()
fig2, yx = plt.subplots()

ax.plot(Id, front_pos)
ax.plot(Id, front_width)

yx.plot(Id, back_pos)
yx.plot(Id, back_width)

# ax.plot(t, ss)

#Chart_1
ax.set(xlabel='Lot ', ylabel=' (mm)',
       title='CPK Chart 2M-09 (Front-pos Front-width)')
ax.grid()

#Chart_2
yx.set(xlabel='Lot ', ylabel=' (mm)',
       title='CPK Chart 2M-09 (Back-pos Back-width)')
yx.grid()

fig1.savefig("test.jpg")
fig2.savefig("test2.jpg")


#Program Email Code HTML
body = f"""
        <html>
        <head>
            <style>
                table, th, td {{border: 1px solid black;border-collapse: collapse;font-family:Roboto;}}
                table#t01 th {{width:25%;background-color: #1c3b56;color: #FFFFFF;text-align: center;font-size: 14px;}}
                table#t01 td {{width:25%;color: #000000;text-align: left;vertical-align: top;padding: 5px;}}
                table#t02 th {{width:50%;background-color: #1c3b56;color: #FFFFFF;text-align: center;font-size: 14px;}}
                table#t02 td {{width:50%;background-color: #FFFFFF;color: #000000;text-align: left;vertical-align: top;padding: 5px;height: 6px;}}
                li {{font-size: 14px;}}

                .tab {{
                    display: inline-block;
                    margin-left: 40px;
                }}
                .content{{
                    background-color: #000000;
                    color:#FFFFFF;
                    font-family:Roboto;
                    }}
                .content2{{
                    background-color:#FFFFFF;
                    }}
                #grad1 {{
                    height: 20px;
                    width: 100%;
                    background-color: #F0E68C;
                    background-image: linear-gradient(to right, #F0E68C , #FFFFFF);
                    color: #000000;
                    opacity: 0.95;
                }}
                .imgDP{{
                    display:flex;
                }}
            </style>
        </head>
        <body>
            <font face='Roboto'>
            <p class="content">
                <strong style="font-size:120%;">&emsp;&emsp; Real-time SPC Report at {times} 2M-09 MT900</strong>
            </p>

            <p class="imgDP">
                <img src="test.jpg" width="600" height="300">
                <img src="test2.jpg" width="600" height="300">
                
            </p>

            <p>
                <ul>
                    <table id="t02">
                        <tr>
                            <th>
                                SPC Alert Detail
                            </th>

                            <th>
                                Production Data
                            </th>
                        </tr>

                        <tr style="background-color: #FFFFFF;">
                            <td>
                                <li>Detected time: {times}</li>
                                <li>Parameter Name: Front-Pos, Front-Width, Back-Pos, Back-Width</li>
                                <li>Upper Specification limit (USL): </li>
                                <li>Lower Specification limit (LSL): </li>
                                <li><b>Control limit (CL): </b></li>
                            </td>
                            <td>
                                <li>Department: MT900</li>
                                <li>Process Name: 2nd Masking</li>
                                <li>Machine Name: 2M-09</li>
                                <li>Part Name: {partname_join}</li>
                                <li>Lot No. List: {L}</li>
                            </td>
                        </tr>

                    </table>

                </ul>
            </p>

            <br>

            <p>
                <ul>
                    <table id="t01">
                        <tr>
                            <th>Lot No. (Out of Control, )</th>
                            <th>Value</th>
                        </tr>
                        
                    </table>
                </ul>
            </p>
            <br>
            <p>
                <img src="Logo.jpg" width="70" height="24"><span>&emsp;<a href="http://163.50.57.95/spc/MT900_spc/data_logger">Click here to access the web application for more detail.</a></span>
            </p>
            <p class="content">
                <h5 class="content">&emsp;Copyright © {timesY} Murata Electronics (Thailand), Ltd. All rights reserved.</h5>
            </p>
            </font>
        </body>
        </html>
        """

attachment = mailItem.Attachments.Add(os.getcwd() + "\\Logo.jpg")
attachment = mailItem.Attachments.Add(os.getcwd() + "\\test.jpg")
attachment = mailItem.Attachments.Add(os.getcwd() + "\\test2.jpg")
mailItem.Subject = 'Real-Time SPC 2M-09 Report at  '  + times 
mailItem.BodyFormat = 1 
mailItem.HTMLBody = body
mailItem.To = User


mailItem.Display()
# time.sleep(3)
# mailItem.Send()
# mailItem.Send()