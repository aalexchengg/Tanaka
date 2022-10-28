import pandas as pd
import os

df = pd.read_csv("data/precinct_data.csv", header = 2, index_col = "Tract")

dataframes = [df]

#makes the list of dataframes
for filename in os.listdir('consolidated_data'):
    dataframes.append(pd.read_csv('consolidated_data/{}'.format(filename), header = 0, index_col = "Tract"))

#combines them into one dataframe
result = pd.concat(dataframes, axis = 1)

#loads it into a csv file
result.to_csv('final_data.csv')
