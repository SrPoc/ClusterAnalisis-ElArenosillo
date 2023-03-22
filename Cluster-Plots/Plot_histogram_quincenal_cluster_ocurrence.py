# -*- coding: utf-8 -*-
"""
Created on Mon Mar 13 18:06:02 2023

@author: Carlos

Script for creating  histograms for cluster ocurrence 
"""
import math
import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.ticker import MultipleLocator
import datetime as dt
from datetime import datetime, timedelta

ClustWDSelec = pd.read_csv('C:/Users/Carlos/Desktop/Figuras Arenosillo/Cluster Analisis/Over WD/Clust_select_days.txt', delimiter='\t', index_col=0)
ClustWDSelec['date'] = pd.to_datetime(ClustWDSelec.index)
ClustWDSelec.set_index('date', inplace=True)


counts = ClustWDSelec.resample('15D')['0'].value_counts()


# Unstack the multi-indexed series to create a dataframe with columns for each cluster selection
counts = counts.unstack(level=-1)

# Calculate the number of days with each cluster selection separately for each 15-day interval
days_with_cluster_1 = counts[1]
days_with_cluster_2 = counts[2]
days_with_cluster_3 = counts[3]

# Create the labels of the histogram plot 
n_quincenal = round((ClustWDSelec.index[-1]-ClustWDSelec.index[0]).days/15)


for n_quinc in np.arange(0,n_quincenal):
    if n_quinc < (n_quincenal-1):
        str_quinc = f'{ClustWDSelec.index[n_quinc*15].strftime("%m/%d")}-{ClustWDSelec.index[(n_quinc+1)*15].strftime("%m/%d")}'
        print(str_quinc)
    
    else:
        str_quinc = f'{ClustWDSelec.index[n_quinc*15].strftime("%m/%d")}-{ClustWDSelec.index[-1].strftime("%m/%d")}'
# Plot a stacked bar chart of the counts for each cluster selection
counts.plot(kind='bar', stacked=True)
plt.xlabel('Date')
plt.ylabel('Count')
plt.title('Quincenal Occurrence of Cluster Selections')
plt.show()

