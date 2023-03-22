# -*- coding: utf-8 -*-
"""
Created on Tue Feb  7 10:24:10 2023

Script used to calculate the average daily hour mean for a subset os data
"""

import xarray as xr
import pandas as pd
import numpy as np
import csv
import tqdm

def calculate_average_day_by_hour(df_data):
    """
    Calculate average of each daily hour
    """
    
    for hour in tqdm.tqdm(np.arange(0,24)):
        data_hour = pd.DataFrame(df_data[df_data.index.hour == hour].mean(axis = 0))
        if hour ==0:
            data_fin = pd.DataFrame(data_hour)
        elif hour!=0:
            data_fin = pd.concat([data_fin,data_hour], axis =1)

    data_fin = data_fin.T.set_index(np.arange(0,24), drop=True)
    return data_fin


