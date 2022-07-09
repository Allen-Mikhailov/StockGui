# Created by Allen Mikhailov https://github.com/SlinkyShelf and Dev shroff https://github.com/kiwisontoast
import inspect
import requests
import datetime as dt
import random
import sys
import socket
sys.executable

import numpy as np

import PySimpleGUI as sg 

import matplotlib 
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from sklearn.linear_model import LinearRegression

import pandas as pd
import pandas_datareader.data as web

import dataPulling

import layout

colors = matplotlib.colors.CSS4_COLORS

sg.theme("BlueMono")

window=sg.Window('Stock Gui',layout.layout, finalize=True)

# matplotlib
fig=matplotlib.figure.Figure(figsize=(5,4))
figure_canvas_agg=FigureCanvasTkAgg(fig,window['Canvas'].TKCanvas)
figure_canvas_agg.draw()
figure_canvas_agg.get_tk_widget().pack()

rowArray = []

index = 0
def Refresh(values):
    # Clearing and Getting Ready for new plots
    fig.clear()
    fig.add_subplot(111).plot([],[])
    axes=fig.axes

    start=dt.datetime(int(values["startYear"]),int(values["startMonth"]),int(values["startDay"]))
    end=dt.datetime(int(values["endYear"]),int(values["endMonth"]),int(values["endDay"]))

    # Drawing all rows
    for i in range(index):
        try:
            data = rowArray[i]
            if not data: 
                continue

            # Getting Data Pull type
            dataPullType = data["dataPullType"]
            _input = values['dataInput/'+str(i)]

            # Getting Data Frame
            df = dataPulling.pullData(dataPullType, _input, start, end)

            data = df.values[:, int(values["columnInput/"+str(i)] or 0)]

            # Potting data
            plotcolor = colors[values["colorPick/"+str(i)]]

            x=np.arange(len(data))
            y=data
            axes[0].plot(x,y, '-', color = plotcolor)

            if (values["LRCheckBox/"+str(i)]):
                # Linear Regression
                x = x.reshape(len(x), 1)
                y = y.reshape(len(y), 1)

                reg = LinearRegression().fit(x, y)
                n = len(data)-1
                axes[0].plot([0, n],[reg.predict([[0]])[0][0], reg.predict([[n]])[0][0]], '-', color = plotcolor)

            figure_canvas_agg.draw()
            figure_canvas_agg.get_tk_widget().pack()

            window["dataInput/"+str(i)].update(background_color = "white")
        except:
            window["dataInput/"+str(i)].update(background_color = "red")
        

while True:
    rawEvent,values=window.read()
    if rawEvent == sg.WIN_CLOSED:
        break

    print(rawEvent)

    if type(rawEvent) != str:
        continue

    eventArgs = rawEvent.split("/")
    event = eventArgs[0]

    if event=='addRow':
        dataPullType = values["dataPullType"]

        frame, layoutM = layout.CreateNewRow(values, index)

        rowData = {"dataPullType": dataPullType, "obj": frame[0][0], "index": index, "layout": layoutM}

        try:
            rowArray[index] = rowData
        except:
            rowArray.append(rowData)

        window.extend_layout(window['RowColumn'], frame)

        index += 1

    elif event=="rmRow":
        row = int(eventArgs[1])

        rowArray[row]["obj"].update(visible=False)
        rowArray[row]["obj"].Widget.master.pack_forget()
        rowArray[row] = None
    elif event == "colorPick":
        row = eventArgs[1]
        window["colorDisplay/"+row].update("", background_color=colors[values[rawEvent]])

    elif event=="Refresh":
        Refresh(values)

window.close()