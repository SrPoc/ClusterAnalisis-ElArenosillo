# -*- coding: utf-8 -*-
"""
Created on Tue Mar  7 10:00:19 2023

@author: Carlos

Script que necesita una lista (data_reshape_final) conteniendo los datos de cada variable en un 
array de promedios horarios dentro de ella con dimensiones (ndias, 24horas).
La primera variable de la lista debe ser WD  

Return: Figura con los clusters para cada variable.
"""

########
## PLOT DATA
#Genero el vector del eje X (entre dos fechas cualquiera separadas 1 dia):
import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.ticker import MultipleLocator
import datetime as dt
from kneed import KneeLocator
from sklearn.datasets import make_blobs
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score
from sklearn.cluster import KMeans
from sklearn.impute import SimpleImputer
from datetime import datetime, timedelta


var_codes = ('G001901.WDSO02#10MN.AVG', 'G001901.WSPD02#10MN.AVG', 'G001901.WVCN01#10MN.AVG', 'G001901.TMPA01#10MN.AVG')
var_names = ('WD (º)', 'WS (m/s)', 'H$_{2}$0 conc. (g/m$^{3}$)', 'T (ºC)') #Variable + (units) separated with a space!!!!!

## For abs values
# values_var = [np.arange(0, 450, 90), np.arange(0, 2.5, 0.25), np.arange(8, 15, 1), np.arange(15, 32, 2.5)]
# labels_var = [('N','E','S','W','N'), np.arange(0, 2.5, 0.25), np.arange(8, 15, 1), np.arange(15, 32, 2.5)]

## For anom values
values_var = [np.arange(0, 450, 90), np.arange(-.5, 1, 0.25), np.arange(7, 13, 1), np.arange(12.5, 30, 2.5)]
labels_var = [('N','E','S','W','N'), np.arange(-.5, 1, 0.25), np.arange(7, 13, 1), np.arange(12.5, 30, 2.5)]


dir_plots = f'C:/Users/Carlos/Desktop/Figuras Arenosillo/Cluster Analisis/Over WD/'

########
## SELECT FRECUENCY DATA FROM WHICH CLUSTER ANALISIS WILL APPLIED
resampling = '1H'; time_dim = 24
# resampling = '10min'; time_dim = 24 *6
########

TinaSelec = pd.read_csv('C:/Users/Carlos/Desktop/Figuras Arenosillo/TinaSBSelection.txt', delimiter='\t', index_col=0)
ClustWDSelec = pd.read_csv('C:/Users/Carlos/Desktop/Figuras Arenosillo/Cluster Analisis/Over WD/Clust_select_days.txt', delimiter='\t', index_col=0)

### Generar un vector de fechas con un intervalo cada hora
# date_vector = [dt.time(hour=h) for h in range(24)] # Con esto alponer el  locator en el polot se hace un lio....
# Define the a random date
fixed_date = '2022-01-01'
# Convert time objects to datetime64 objects with fixed date
date_vector = np.array([np.datetime64(f'{fixed_date}T{t}') for t in date_vector])




fig, ax = plt.subplots(2, 2,figsize=(20,14), sharex=True)

fig.suptitle(f'Cluster analisis over {var_names[0][0:(var_names[0].find("(")-1)]} (daily anomalies)', fontsize=30, fontweight="bold") 

for subpl in np.arange(0,4):

    ###### CALCULO DE MEDIAS PARA LOS DÍAS DE CADA CLUSTER
    for clust in range(int(ClustWDSelec.max())):
        cluster_data = anom_data[subpl][np.array(ClustWDSelec['0']) == (clust+1)]
        # Average for WD is different (WD is always located in the first position index)
        if subpl == 0:
            daily_avg_clust = []
            daily_std_clust = []
            for dtime in range(np.shape(cluster_data)[1]):
                # loop over each hour of day
                cluster_data_rad = cluster_data[:, dtime] * np.pi / 180
        
                # calcular el promedio de los senos y cosenos de la dirección del viento
                media_sin = np.mean(np.sin(cluster_data_rad)* np.pi/180)
                media_cos = np.mean(np.cos(cluster_data_rad)* np.pi/180)
    
                std_sin = np.std(np.sin(cluster_data_rad)* np.pi/180)
                std_cos = np.std(np.cos(cluster_data_rad)* np.pi/180)
                
                daily_avg_clust.append(np.arctan2(media_sin, media_cos) * 180 / np.pi %360)
                daily_std_clust.append(np.arctan2(std_sin, std_cos) * 180 / np.pi %360)
      
        else:
            daily_avg_clust = cluster_data.mean(axis =0)
            daily_std_clust = cluster_data.std(axis =0)
        
        ### PLOTTING...
        pd.DataFrame(daily_avg_clust, date_vector).plot(ax = ax.ravel()[subpl], 
                                                        legend=False)
        # ax.ravel()[subpl].plot(pd.DataFrame(daily_avg_clust, date_vector).index,
        #                   pd.DataFrame(daily_avg_clust, date_vector))
        
    ###### FORMATO FIGURA
    ## TITULO SUBPLOT
    ax.ravel()[subpl].set_title(f'{var_names[subpl][0:(var_names[subpl].find("(")-1)]}', fontsize=20, fontweight="bold")  

    ## FORMATO EJES
    # X
    ax.ravel()[subpl].xaxis.set_major_locator(mdates.HourLocator(byhour=range(1))) # set the major tick locator
    ax.ravel()[subpl].xaxis.set_major_formatter(mdates.DateFormatter('%H:%M')) # set the major tick format
    # ax.ravel()[subpl].xaxis.set_minor_locator(MultipleLocator(2)) # set the minor tick locator
    ax.ravel()[subpl].tick_params(axis='x', labelrotation=45)
    # fig.ravel()[subpl].autofmt_xdate(False)
    
    # Y
    ax.ravel()[subpl].set_ylabel(var_names[subpl][(var_names[subpl].find('(') + 1 ):var_names[subpl].find(')')], fontsize=22)
    ax.ravel()[subpl].tick_params(axis='both', which='both', labelsize=18)
    ax.ravel()[subpl].set_yticks(values_var[subpl])
    ax.ravel()[subpl].set_ylim(values_var[subpl][0], values_var[subpl][-1])
    ax.ravel()[subpl].set_yticks(values_var[subpl], labels = labels_var[subpl])
    #######    
        
    ax.ravel()[subpl].grid(True, color='grey', linestyle='--', alpha=0.5)
    plt.legend(['Cluster 1 (P-SB)', 'Cluster 2 (NP-SB)', 'Cluster 3'], fontsize=15)
# fig.autofmt_xdate(False)
plt.savefig(f'{dir_plots}/ClustersWD_v2')
plt.show()
            
