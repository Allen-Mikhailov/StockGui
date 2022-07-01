import pandas as pd
import pandas_datareader.data as web

import tickers 

def pullData(pulltype, _input, start, end):
    df = ""
    if pulltype == "File":
        df = pd.read_csv(_input)
    elif pulltype == "yahoo":
        df = web.DataReader(tickers.getTicker(_input), "yahoo", start, end)
    return df