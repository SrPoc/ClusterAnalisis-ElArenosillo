# -*- coding: utf-8 -*-
"""
Spyder Editor

This script contains functions that read gumnet data if the column names are in 
ONE line (if you take more variables they might be organised diferently)

author: Alvaro (Intermet)
"""
import xarray as xr
import pandas as pd
import numpy as np
import csv
import tqdm


# names=['G001901.RADS01#10MN.AVG',
#        'G001901.RADS02#10MN.AVG',
#        'G001901.RADL01#10MN.AVG',
#        'G001901.RADL02#10MN.AVG',
#        'G001901.SHFX01#10MN.AVG',
#        'G001901.WVFX01#10MN.AVG',
#        'G001901.HFXS01#10MN.AVG',
#        'G001901.WSPD03#10MN.AVG',
#        'G001901.WDSO02#10MN.AVG',
#        'G001901.UXWS01#10MN.STD'
#        'G001901.UYWS01#10MN.STD',
#        'G001901.UZWS01#10MN.STD',
#        'G001901.CXCZ01#10MN.SMP',
#        'G001901.CYCZ01#10MN.SMP']

def read_variable(row: str):
        """
        Separate the rows in data and time.
        """
        time = pd.to_datetime(' '.join([row.split(';')[0]] + [row.split(';')[1]]), format='%Y/%m/%d %H:%M:%S')
        data = [float(m) if m != '' else 0 for m in row.split(';')[2:]]

        return data, time

def get_header(file_path: str):
    """
    Get only the first line of a .txt to get the variable names in a list
    """
    with open(file_path, 'r') as read_obj:
        variable_names = read_obj.readline()
        variable_names = variable_names.split()
    return variable_names

def get_rows(file_path: str):
    """
    Get the the dates and the data separately.
    """
    data_rows = []
    time_rows = []

    with open(file_path, 'r') as read_obj:
        # Get variable_names
        variable_names = read_obj.readline()
        # pass the file object to reader() to get the reader object
        csv_reader = csv.reader(read_obj)
        # Iterate over each row in the csv using reader object
        for row in tqdm.tqdm(list(csv_reader), desc='>> Reading ' + file_path):
            # row variable is a list that represents a row in csv
            # Seek the rows that correspond to the variables of interest
            try:
                # Remove multiple blank spaces
                row = " ".join(row[0].split())
                # Replace blank spaces with a more manageable delimiter
                row = row.replace(" ", ";")

                data, data_time = read_variable(row)
                data_rows.append(data)
                time_rows.append(data_time)

            except:
                continue

    return time_rows, data_rows

def open_file(file_path: str):
    """
    Open .txt as pandas
    """
    # Get time index and data
    time_rows, data_rows = get_rows(file_path)
    # Get variable names
    header = get_header(file_path)
    # Join in dataframe
    df_data = pd.DataFrame(data_rows)
    df_data.columns = header
    df_data['time'] = time_rows
    df_data = df_data.sort_values('time')
    df_data = df_data.set_index('time')
    df_data.index = pd.to_datetime(df_data.index)

    return df_data

# if _name_ == '_main_':
#     data = open_file(file_name)
#     print(data)

file_path = r"F:\Tesis\Data\Gumnet\El_Arenosillo_data_20220719_20221031.txt"


