import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import statsmodels.api as sm
from statsmodels.formula.api import ols
import limited_research as rp

master_df = pd.read_csv('final_data.csv')
master_df = master_df.rename(columns = {' !!Total:': 'Total Population', ' !!Total:!!Population of one race:!!White alone': 'White Population',
                                        'Estimate!!Median household income in the past 12 months (in 2019 inflation-adjusted dollars)': 'Median Income',
                             'Estimate!!Total':'Disabled Population'})

race_df = master_df[['Tract', 'Tightness', 'Total Population', 'White Population']].copy()


#disability_df = master_df[['Tract', 'Tightness', 'Estimate!!Total']].copy()

#income_df = master_df[['Tract', 'Tightness', 'Estimate!!Median household income in the past 12 months (in 2019 inflation-adjusted dollars)']].copy()
print(race_df.columns)

table = rp.summary_cont(race_df['Total Population'].groupby(race_df['Tightness']))
print(table)