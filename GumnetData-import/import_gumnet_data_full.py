# -*- coding: utf-8 -*-
"""
Created on Tue Feb  7 10:24:10 2023

@author: Carlos
"""

def open_observations(file_path):
    # Extract the variable name from the path of the file
    variable = (file_path.split('/')[-1]).split('_')[1]

    # Open de file as a dataframe
    data = pd.read_csv(str(file_path), index_col=0, skiprows=[0, 1, 2, 3], encoding='latin1')

    # Take only the validated data
    idx = data.index[data['Validación'] != 'V'].tolist()
    data = data.drop(['Validación'], axis=1)
    data.loc[idx] = np.nan

    # Drop column of validated samples, only in the case of statistical variables
    if 'Muestras Validadas' in data.columns:
        data = data.drop(['Muestras Validadas'], axis=1)

    # Rename the columns from latin encoding to avoid compatibility probles
    data = data.rename({'Media': variable + '_mean',
                        'Mínima': variable + '_min',
                        'Máxima': variable + '_max',
                        'Mediana': variable + '_median',
                        'Total': variable + '_total',
                        'Tipo': variable + '_type'}, axis='columns')

    # Change format and name of the index to datetime
    data.index = pd.to_datetime(data.index)
    data.index.names = ['dates']

    return data