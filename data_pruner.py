import pandas as pd
import os

precinct_list = []

## getting the list of precincts

with open("data/precinct_list.txt") as precinct_file:
    for line in precinct_file:
        if(len(line)>5):
            precinct_list.append(str(int(100*float(line))))
        else:
            precinct_list.append(str(int(line)))

## reading various data

#iterate through all files in data folder
for filename in os.listdir('data'):
    if('.') not in filename:
        entries = []
        df = pd.read_csv("data/{}/{}.csv".format(filename, filename), header = 1)
        #change the id so that its exactly what we want
        df['id'] = df['id'].apply(lambda x: str(x).split('US')[1][5:11])
        #reads the csv file that should have the same name as the subfolder
        #col_array = df.columns.drop(['id', 'Geographic Area Name'])
        for precinct in precinct_list:
            entry = df[df['id'].str.contains(precinct)]
            #total = entry.loc[:, col_array].sum(axis = 0)
            entries.append(entry)
        #iterate throw precinct list to look for matches. if so, add to a list
        found_df = pd.concat(entries)
        #create a dataframe out of the list
        found_df.to_csv('pruned_data/{}_pruned.csv'.format(filename))
    #write to the pruned data file
