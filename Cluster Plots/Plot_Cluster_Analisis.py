# -*- coding: utf-8 -*-
"""
Created on Tue Mar  7 10:00:19 2023

@author: Carlos

Script que necesita una lista (data_reshape_final)conteniendo los datos de cada variable en un 
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
import datetime as dt
from kneed import KneeLocator
from sklearn.datasets import make_blobs
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score
from sklearn.cluster import KMeans
from sklearn.impute import SimpleImputer
from datetime import datetime, timedelta

var_codes = ('G001901.WDSO02#10MN.AVG', 'G001901.WSPD02#10MN.AVG', 'G001901.WVCN01#10MN.AVG', 'G001901.TMPA01#10MN.AVG')
var_names = ('WD (º)', 'WS (m/s)', 'H$_{2}$0 conc. (g/m$^{3}$)', 'T(K)')
values_var = [np.arange(0, 450, 90), np.arange(0, 2, 0.25), np.arange(8, 13, 1), np.arange(17, 32, 2.5)]

# Create the directory if it doesn't exist yet
dir_plots = f'C:/Users/Carlos/Desktop/Figuras Arenosillo/Cluster Analisis/Over WD/'


########
## SELECT FRECUENCY DATA FROM WHICH CLUSTER ANALISIS WILL APPLIED
resampling = '1H'; time_dim = 24
# resampling = '10min'; time_dim = 24 *6
########

TinaSelec = pd.read_csv('C:/Users/Carlos/Desktop/Figuras Arenosillo/TinaSBSelection.txt', delimiter='\t', index_col=0)
ClustWDSelec = pd.read_csv('C:/Users/Carlos/Desktop/Figuras Arenosillo/Cluster Analisis/Over WD/Clust_select_days.txt', delimiter='\t', index_col=0)
ClustWDSelec = ClustWDSelec

# Definir las fechas de inicio y fin
start_date = datetime(2023, 3, 1, 0, 0) # 1 de marzo de 2023, 00:00
end_date = datetime(2023, 3, 2, 0, 0) # 2 de marzo de 2023, 00:00

# Definir la distancia entre cada fecha
if resampling == '10min':
    delta = timedelta(minutes=10)
else:
    delta = timedelta(hours = 1)

# Generar un vector de fechas con un intervalo de 10 minutos
current_date = start_date
date_vector = []
while current_date < end_date:
    date_vector.append(current_date)
    current_date += delta

fig, ax = plt.subplots(kmeans.n_clusters, len(var_codes),figsize=(9*2*3,15*2.5), sharex=True)

fig.suptitle(f'Cluster analisis over {var_codes[var_sel]}', fontsize=40, fontweight="bold") 
for var_idx in np.arange(len(var_codes)):
   
    
    for i in range(kmeans.n_clusters):
        cluster_data = data_reshape_final[var_idx][np.array(ClustWDSelec['0']) == (i+1)]
        
        # Average for WD is different
        if var_idx == 0:
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

                ax[i][var_idx].set_ylim(0, 450)

                ax[i][var_idx].set_yticks(values_var[var_idx], labels = ('N','E','S','W','N'))
        else:
            daily_avg_clust = cluster_data.mean(axis =0)
            daily_std_clust = cluster_data.std(axis =0)
            ax[i][var_idx].set_yticks(values_var[var_idx])
        ######
        # Uncomment for any variable EXCEPT WIND DIRECTION
        pd.DataFrame(daily_avg_clust, date_vector).plot(ax = ax[i][var_idx])
        ax[i][var_idx].fill_between(date_vector, daily_avg_clust-np.array(daily_std_clust), daily_avg_clust+np.array(daily_std_clust), alpha=0.2)
        ######
        # Establecer el formato de fecha para el eje X
        date_format = mdates.DateFormatter('%H:%M')
        date_locator =  mdates.HourLocator()
        ax[i][var_idx].xaxis.set_major_formatter(date_format)
        
        ax[i][var_idx].tick_params(axis = 'x', which='both', labelrotation=45)
        # ax[i].xaxis.set_major_locator(date_locator)
        
        ax[i][var_idx].set_ylabel(var_names[var_idx], fontsize=30)
        ax[i][var_idx].tick_params(axis='both', which='both', labelsize=30)
        ax[i][var_idx].set_title(f'{var_names[var_idx]} (Cluster {i+1})', fontsize=40, fontweight="bold")
        
        # ax[i][var_idx].grid(True)
        # ax1.get_shared_x_axes().join(ax1, ax2)
        
        
    ax[i][var_idx].set_xlabel('UTC time', fontsize=40)
    ax[i][var_idx].get_shared_x_axes().join(ax[i-1][var_idx], ax[i][var_idx],ax[i-2][var_idx])
plt.savefig(f'{dir_plots}/Clusters{var_names[var_sel][:2]}')
plt.show()

print('Ended.')  
