#this script will average out zero values with those in front of them
#for example, if there were 0 votes on Tuesday, 0 on Wednesday, and 6 on Friday
#the script will calculate it as 2 votes on Tuesday, Wednesday, and Friday each
import pandas as pd
import sys
import os


def main():
   
    df = pd.read_csv("data/mailin.csv")

    def avg(values: list):
        valstack = []
        for i in range(len(values)):
            if(values[i]==0):
                valstack.append(i)
            else:
                if(len(valstack)!=0):
                    valstack.append(i)
                    val = values[i]/(len(valstack))
                    while(len(valstack)!=0):
                        values[valstack.pop()]= val
        return values
    
    for (name, data) in df.iteritems():
        df[name] = pd.Series(avg(data))
    
    df.to_csv("data/mailin_modified.csv")

main()