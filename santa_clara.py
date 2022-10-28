#gets cumulative votes for each candidate in santa clara based on data
#does this for all days, and puts into one final dataframe


import pandas as pd
import sys
import os
import numpy as np
from datetime import datetime

finaldf = pd.DataFrame()
dates = []

#read each file
for filename in os.listdir("data/voter_input_sc"):
    scdf = pd.read_excel("data/voter_input_sc/{}".format(filename), sheet_name = "12")
    #isolate names from weird first row formatting
    names = scdf.iloc[[0]].values[0]
    names = names[~pd.isnull(names)]

    #get relevant headers, add names to each
    new_headers = scdf.iloc[[1]].values[0]
    names_only = new_headers[2:29]
    for i in range(len(names_only)):
        names_only[i] = names[int(i/3)] + " " + names_only[i]
    new_headers = new_headers[:2].tolist() + names_only.tolist() + new_headers[29:].tolist()

    #switch headers, isolate columns
    scdf = scdf[1:]
    scdf.columns = new_headers
     #get sums, add to main dataframe
    scdf = scdf[scdf['County'] == 'Total:']
    scdf = scdf[['{} Total Votes'.format(candidate) for candidate in names]]
    scdf = scdf.astype(str).astype(int)
    finaldf = finaldf.append(scdf, ignore_index = True)
    #get date, add to dates list
    day = int(filename.replace("Santa_Clara_June","" ).replace(".xlsx", ""))
    dates.append(datetime(2022,6,day))
    
finaldf['Date'] = dates

finaldf.to_csv("data/voter_output/Santa_Clara_Cumulative.csv")