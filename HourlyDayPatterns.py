# -*- coding: utf-8 -*-
"""
Created on Wed Mar  1 17:36:02 2023

@author: Pablo

This script aims to calculate daily patterns (hour by hour) of a given time
series of meteo data.
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


data = open_file(r"F:\Tesis\Data\Gumnet\El_Arenosillo_data_20220719_20221031.txt")
dataWS = data['G001901.WDSO02#10MN.AVG']

dataWS_rad = np.radians(dataWS)

# Calcular la media de los cosenos y senos de la dirección del viento para cada hora
df_hora = dataWS_rad.resample('H').agg({'rad_sin': lambda x: np.mean(np.sin(x)), 'rad_cos': lambda x: np.mean(np.cos(x))})
# Calcular la dirección del viento promedio para cada hora
df_hora['dir_viento'] = np.arctan2(df_hora['rad_sin'], df_hora['rad_cos'])
# Eliminar las columnas de los cosenos y senos
df_hora = df_hora.drop(['rad_sin', 'rad_cos'], axis=1)* 180 / np.pi +180

groups = df_hora.groupby(df_hora.index.hour)

means = groups.mean()
stds = groups.std()
mins = groups.min()
maxs = groups.max()

fig, ax = plt.subplots()
means.plot(ax=ax, label='Mean')
stds.plot(ax=ax, label='Std')
ax.legend()
plt.show()




fig, ax = plt.subplots(figsize=(12, 6))
ax.plot(np.arange(0,24), np.transpose(centroids))


