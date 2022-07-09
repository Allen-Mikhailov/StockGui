import PySimpleGUI as sg
import matplotlib as mpl
import numpy as np
import random

inputOptions = ["File", "yahoo"]

colors = mpl.colors.CSS4_COLORS
colorlist = list(colors)

dayoptions = np.arange(1, 32).tolist()
monthoptions = np.arange(1, 13).tolist()
yearoptions = np.arange(2022, 1969, -1).tolist()

rowHeader = [sg.Combo(inputOptions, key="dataPullType", default_value="File", readonly=True, enable_events=True), sg.Button("+", tooltip="Add Row", key="addRow")]

rowData = [
    rowHeader,
    [sg.Column([[]], key="RowColumn")]
]

canvas = [[sg.Canvas(key="Canvas")]]

def CreateNewRow(values, index):
    color = random.choice(colorlist)
    dataPullType = values["dataPullType"]

    tooltip = ""
    if dataPullType=="yahoo":
        tooltip = "Stock Ticker or Name"
    else:
        tooltip = "File Name"

    sindex = str(index)

    layout = [[
        sg.Text(key="colorDisplay/"+sindex, size=(2, 1), background_color=colors[color]),
        sg.Input(key='dataInput/'+sindex, enable_events=True, default_text="", size=(15, 10), tooltip=tooltip),
        sg.Input(key="columnInput/"+sindex,size=(1,20), default_text="5", tooltip="Column"),
        sg.Checkbox("", key="LRCheckBox/"+sindex, default=True, tooltip="Run Linear Regression"),
        sg.Combo(colorlist, key="colorPick/"+sindex, default_value=color, readonly=True, enable_events=True),
        sg.Button("X", tooltip="Remove Row", key="rmRow/"+sindex)
    ]]

    return [[sg.Frame(title="", key="row/"+sindex,layout=layout)]], layout

layout = [
    [sg.Text("Stock Gui")],
    [
        sg.Text("Start Date: "),
        sg.Combo(yearoptions,  key="startYear", size=(5, 10), readonly=True, default_value="2021"), 
        sg.Combo(monthoptions, key="startMonth",  size=(5, 10), readonly=True, default_value="1"), 
        sg.Combo(dayoptions,   key="startDay",    size=(5, 10), readonly=True, default_value="1")
    ],
    [
        sg.Text("End Date:  "),
        sg.Combo(yearoptions,  key="endYear", size=(5, 10), readonly=True, default_value="2021"), 
        sg.Combo(monthoptions, key="endMonth",  size=(5, 10), readonly=True, default_value="1"), 
        sg.Combo(dayoptions,   key="endDay",    size=(5, 10), readonly=True, default_value="10")
    ],
    [sg.Button("Refresh", key="Refresh")],

    [sg.Column(rowData, vertical_alignment='top'),
    sg.VSeperator(),
    sg.Column(canvas)
    ]
]