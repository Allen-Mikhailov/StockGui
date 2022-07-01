import pandas as pd
import numpy as np

Tickerdf = pd.read_csv("./Tickers.csv")
symbols = Tickerdf.values[:, 2]
names = Tickerdf.values[:, 1]

for i in range(len(names)):
    names[i] = names[i].upper()

def getTicker(string):
    string = string.upper()

    if string == "":
        return

    if len(np.where(symbols == string)[0]) > 0:
        return string
    else:
        cases = np.where(names == string)
        if len(cases[0]) > 0:
            return cases[0][0]

        for i in range(len(names)):
            if names[i].startswith(string):
                return symbols[i]

    return ""