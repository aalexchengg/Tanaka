#gets cumulative votes for each candidate in san mateo
import pandas as pd
import sys
import os

def main():
    dates = ['09', '10', '13', '15', '17', '21', '23']
    title = "U.S. Representative, 16th District"

    cumdf = pd.DataFrame()
    initialized = False
    for date in dates:
        df = pd.read_excel("data/voter_input_sm/San_Mateo_June{}.xlsx".format(date))
        df = df[df['Contest_title']==title]
        df = df[['Precinct_name', 'Turn_Out', 'Contest_title', 'candidate_name', 'total_votes', 'Vote Centers_votes', 'Vote by Mail_votes']]
        #print(df.head())
        if not initialized:
            cumdf['candidate_name'] = df['candidate_name']
            initialized = True
        cumdf['6/{} Cumulative Votes'.format(date)] = df['total_votes']
    cumdf = cumdf.groupby("candidate_name").sum()
    cumdf.sort_values(by = ['candidate_name'], inplace = True)
    second_row = cumdf.iloc[[1]].values[0]
    reldf = cumdf.apply(lambda row: row - second_row, axis=1)
    print(reldf)
        #df.to_csv("data/voter_output/San_Mateo_June{}_Condensed.csv".format(date))
    #cumdf.to_csv("data/voter_output/San_Mateo_Cumulative.csv")
    #reldf.to_scv("data/voter_output/San_Mateo_Relative.csv")


main()
