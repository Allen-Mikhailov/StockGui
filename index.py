import PySimpleGUI as sg 
import sys

from matplotlib import pyplot as plt
sys.executable

from os.path import exists

import matplotlib 
import datetime as dt
import matplotlib 
import pandas as pd
import pandas_datareader.data as web 
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

dataPullType = "File"

def update_figure(data):
    fig.clear()
    fig.add_subplot(111).plot([],[])
    axes=fig.axes
    x=[i[0] for i in data]
    y=[int(i[1]) for i in data]
    axes[0].plot(x,y,'r-')
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack()

sg.theme("BlueMono")
table_content=[]
layout=[
    [
        sg.Text("Data Pulling:"),
        sg.Combo(["File", "yahoo"], key="dataPullType", default_value=dataPullType, readonly=True, enable_events=True),
        sg.Text("Column:"),
        sg.Input(key="columnInput",size=(10,20))
    ],
    [sg.Text("", key="errLabel", text_color="red")],
    [
        sg.Text("...", key="dataPullTypeLabel"), 
        sg.Input(key='dataInput',expand_x=True, enable_events=True),
        sg.Button('Refresh')
    ],
    [sg.Canvas(key='Canvas')]
]

window=sg.Window('Graphing',layout, finalize=True)

# matplotlib
fig=matplotlib.figure.Figure(figsize=(5,4))
figure_canvas_agg=FigureCanvasTkAgg(fig,window['Canvas'].TKCanvas)
figure_canvas_agg.draw()
figure_canvas_agg.get_tk_widget().pack()

def UpdateDataPullType():
    if dataPullType == "File":
        window["dataPullTypeLabel"].update("File Name:")
    else:
        window["dataPullTypeLabel"].update("Stock Name:")
        


def UpdateContent():
    update_figure(table_content)

# def Refresh():

UpdateDataPullType()

while True:
    event,values=window.read()
    if event == sg.WIN_CLOSED:
        break

    if event == 'dataPullType':
        dataPullType = values["dataPullType"]
        UpdateDataPullType()
    elif event == 'dataInput':
        errmessage = ""
        if dataPullType == "File":
            if not exists(values['dataInput']):
                errmessage = "Error: file \""+values['dataInput']+"\" does not exist"
        window["errLabel"].update(errmessage)
    elif event == "Refresh":
        # Getting CSV
        df = ""
        if dataPullType == "File":
            if not exists(values['dataInput']):
                continue
            df = pd.read_csv(values['dataInput'])
        elif dataPullType == "yahoo":
            start=dt.datetime(2020,1,1)
            end=dt.datetime(2022,6,19)
            df = web.DataReader(values['dataInput'], "yahoo", start, end)

        data = df.values[:, int(values["columnInput"])]

        table_content = []
        for i in range(len(data)):
            table_content.append([i+1, data[i]])
        UpdateContent()



window.close()