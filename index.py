# Created by Allen Mikhailov https://github.com/SlinkyShelf and Dev shroff https://github.com/kiwisontoast
import inspect
from tkinter import E
import requests
import datetime as dt
import random
import sys, os
import socket
sys.executable

import numpy as np
import colorsM

import PySimpleGUI as sg 

import matplotlib 
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from sklearn.linear_model import LinearRegression

import pandas as pd
import pandas_datareader.data as web

import dataPulling

import layout

colors = colorsM.colors
colorlist = colorsM.colorlist

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
            rowData = rowArray[i]
            if not rowData: 
                continue

            # Getting Data Pull type
            dataPullType = rowData["dataPullType"]
            _input = values['dataInput/'+str(i)]

            # Getting Data Frame
            df = dataPulling.pullData(dataPullType, _input, start, end)

            data = df.values[:, int(values["columnInput/"+str(i)] or 0)]

            # Potting data
            plotcolor = colors[rowData["color"]]

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

            window["dataInput/"+str(i)].update(background_color = "white")
        except Exception as e:
            print("Errored while Refreshing: ")
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(str(e), fname, exc_tb.tb_lineno)

            window["dataInput/"+str(i)].update(background_color = "red")
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack()
        

while True:
    rawEvent,values=window.read()
    if rawEvent == sg.WIN_CLOSED:
        break

    if type(rawEvent) != str:
        continue

    eventArgs = rawEvent.split("/")
    event = eventArgs[0]

    print(eventArgs)

    if event=='addRow':
        dataPullType = values["dataPullType"]

        rowData = {"dataPullType": dataPullType, "index": index}
        frame, layoutM = layout.CreateNewRow(values, rowData)
        rowData["layout"] = layoutM
        rowData["obj"] = frame[0][0]

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
    elif len(eventArgs) > 2 and eventArgs[1] == "colorInput":
        row = eventArgs[2]
        rowArray[int(row)]["color"] = eventArgs[3]
        window["colorDisplay/"+row].update("", background_color=colors[eventArgs[3]])

    elif event=="Refresh":
        Refresh(values)

window.close()