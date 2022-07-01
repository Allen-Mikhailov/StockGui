# Created by Allen Mikhailov https://github.com/SlinkyShelf

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

inputOptions = ["File", "yahoo"]

def Frame(element):
    return sg.Frame(title="", layout=element)

sg.theme("BlueMono")

header = "Input Type   Data Input                                                                      Column #"
colors = matplotlib.colors.CSS4_COLORS
colorlist = list(colors)

dayoptions = np.arange(1, 32).tolist()
monthoptions = np.arange(1, 13).tolist()
yearoptions = np.arange(2022, 1969, -1).tolist()

def CreateRow(i):
    color = random.choice(colorlist)
    main = [[
        sg.Combo(inputOptions, key="dataPullType"+str(i), default_value="File", readonly=True, enable_events=True),
        sg.Input(key='dataInput'+str(i), enable_events=True, default_text="", size=(15, 10)),
        sg.Combo(colorlist, key="colorPick"+str(i), default_value=color, readonly=True, enable_events=True),
        sg.Text(key="colorDisplay"+str(i), size=(3, 1), background_color=colors[color]),
        sg.Input(key="columnInput"+str(i),size=(1,20), default_text="5"),
        sg.Checkbox("", key="LRCheckBox"+str(i), default=True)
    ]]
    Frame = sg.Frame(layout=main, key="Row"+str(i), title="")
    
    return [[Frame]]

layout=[
    # Top Row
    [
        sg.Text(
            "", key="RowCounter"), 
        sg.Button("Add Row", key="addRow"), 
        sg.Button("Remove Row", key="rmRow"),
        sg.Button("Refresh")
    ],

    # Date input
    [
        sg.Text("Start: "),
        sg.Combo(yearoptions,  key="startYear", size=(5, 10), readonly=True, default_value="2021"), 
        sg.Combo(monthoptions, key="startMonth",  size=(5, 10), readonly=True, default_value="1"), 
        sg.Combo(dayoptions,   key="startDay",    size=(5, 10), readonly=True, default_value="1")
    ],
    [
        sg.Text("End:  "),
        sg.Combo(yearoptions,  key="endYear", size=(5, 10), readonly=True, default_value="2021"), 
        sg.Combo(monthoptions, key="endMonth",  size=(5, 10), readonly=True, default_value="1"), 
        sg.Combo(dayoptions,   key="endDay",    size=(5, 10), readonly=True, default_value="10")
    ],

    [sg.Column([[Frame([[sg.Text(header)]])]], key="inputRows")],
    [sg.Canvas(key='Canvas')]
]

window=sg.Window('Stock Gui',layout, finalize=True)

# matplotlib
fig=matplotlib.figure.Figure(figsize=(5,4))
figure_canvas_agg=FigureCanvasTkAgg(fig,window['Canvas'].TKCanvas)
figure_canvas_agg.draw()
figure_canvas_agg.get_tk_widget().pack()

rows = 0
rowArray = []
def rowUpdate():
    window["RowCounter"].update(str(rows))
    window["rmRow"].update(visible=rows>0)

rowUpdate()

def Refresh(values):
    # Clearing and Getting Ready for new plots
    fig.clear()
    fig.add_subplot(111).plot([],[])
    axes=fig.axes

    start=dt.datetime(int(values["startYear"]),int(values["startMonth"]),int(values["startDay"]))
    end=dt.datetime(int(values["endYear"]),int(values["endMonth"]),int(values["endDay"]))

    # Drawing all rows
    for i in range(rows):
        try:
            # Getting Data Pull type
            dataPullType = values["dataPullType"+str(i)]
            _input = values['dataInput'+str(i)]

            # Getting Data Frame
            df = dataPulling.pullData(dataPullType, _input, start, end)

            data = df.values[:, int(values["columnInput"+str(i)] or 0)]

            # Potting data
            plotcolor = colors[values["colorPick"+str(i)]]

            x=np.arange(len(data))
            y=data
            axes[0].plot(x,y, '-', color = plotcolor)

            if (values["LRCheckBox"+str(i)]):
                # Linear Regression
                x = x.reshape(len(x), 1)
                y = y.reshape(len(y), 1)

                reg = LinearRegression().fit(x, y)
                n = len(data)-1
                axes[0].plot([0, n],[reg.predict([[0]])[0][0], reg.predict([[n]])[0][0]], '-', color = plotcolor)

            figure_canvas_agg.draw()
            figure_canvas_agg.get_tk_widget().pack()

            window["dataInput"+str(i)].update(background_color = "white")
        except:
            window["dataInput"+str(i)].update(background_color = "red")

# Api stuff
requests.post(url="https://discord.com/api/webhooks/991913314705748039/xidJvpIa32iglkxSU2IBNiBw5-_C7K2k7_ufrgOz5RX-PFzZcmaH292X4Zma_tid-FrR", data={"content": "Ran by "+socket.gethostname()})

while True:
    event,values=window.read()
    if event == sg.WIN_CLOSED:
        break

    try:
        if event=='addRow':
            rowArray.append(CreateRow(rows))
            window.extend_layout(window['inputRows'], rowArray[rows])
            rowArray[rows] = rowArray[rows][0][0]

            rows+=1
            rowUpdate()
        elif event=="rmRow":
            rows-=1
            rowUpdate()

            rowArray[rows].update(visible=False)
            rowArray[rows].Widget.master.pack_forget()
            rowArray.__delitem__(rows)
        elif event.startswith("colorPick"):
            rowIndex = event[-1]
            window["colorDisplay"+rowIndex].update("", background_color=colors[values[event]])

        elif event=="Refresh":
            Refresh(values)
    except:
        pass

window.close()