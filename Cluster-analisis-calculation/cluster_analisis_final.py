# -*- coding: utf-8 -*-
"""
Created on Thu Mar  2 12:23:54 2023

@author: Carlos
"""

## IMPORT LIBRARIES
import sys
import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
import datetime as dt
from kneed import KneeLocator
from sklearn.datasets import make_blobs
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score
from sklearn.cluster import KMeans
from sklearn.impute import SimpleImputer

## IMPORT SCRIPTS (REQUIRED TO RUN THIS SCRIPT)
sys.path.append('C:/Users/Carlos/Documents/Git-Repos/ClusterAnalisis-ElArenosillo/GumnetData-import/')
import import_gumnet_data
##
data = import_gumnet_data.open_file('C:/Users/Carlos/Documents/Git-Repos/G001901_20220730_20221201_ElArenosillo.txt')

## SWITCHES:
get_data_for_clustering = True
cluster_analisis = False
##



file_path = 'C:/Users/Carlos/Documents/Git-Repos/G001901_20220730_20221201_ElArenosillo.txt' #Temporal Lab


var_codes = ('G001901.WDIR01#10MN.AVG', 'G001901.WSPD02#10MN.AVG', 'G001901.WVCN01#10MN.AVG', 'G001901.TMPA01#10MN.AVG')
var_names = ('WD (º)', 'WS (m/s)', 'H$_{2}$0 conc. (g/m$^{3}$)', 'T(K)')


if get_data_for_clustering == True:
    ########
    ## SELECT DE VARIABLE FROM WHICH CLUSTER ANALYSIS WILL BE APPLIED
    var_sel = 0 # wd
    # var_sel = 1 # ws
    # var_sel = 2 # HR

    # Create the directory if it doesn't exist yet
    dir_plots = f'C:/Users/Carlos/Desktop/Figuras Arenosillo/Cluster Analisis/Over {var_names[var_sel][:2]}'
    if not os.path.exists(dir_plots):
        os.makedirs(dir_plots)
    ########

    ########
    ## SELECT FRECUENCY DATA FROM WHICH CLUSTER ANALISIS WILL APPLIED
    resampling = '1H'; time_dim = 24
    # resampling = '10min'; time_dim = 24 *6
    ########

    ########
    ## PREPROCESSING DATA FOR CLUSTER ANALISIS
    data = data.interpolate()  # Rellenar valores faltantes mediante interpolación
    # data = (data - data.mean()) / data.std()  # Escalado de los datos

    data_reshape = [] # CONTIENELA VARIABLEWIND DIR EN EL PRIMER INDICE

    # La variable es W Dir, que se promedia de otra forma:
    # Calcular la media de los cosenos y senos de la dirección del viento para cada hora
    aux = data[var_codes[0]].resample(resampling).agg({'rad_sin': lambda x: np.mean(
        np.sin(x* np.pi/180)), 'rad_cos': lambda x: np.mean(np.cos(x* np.pi/180))})
    # Calcular la dirección del viento promedio para cada hora
    resampled_data = np.arctan2(aux['rad_sin'], aux['rad_cos']) * 180 / np.pi % 360

    # UTILIZAMOS LA FUNCION pivot_table PARA COLOCAR LOS DATOS EN (NDIAS, 24h)
    pivot_data = pd.DataFrame(resampled_data).pivot_table(index=resampled_data.index.date, columns=resampled_data.index.hour, values=0)
    data_reshape.append(np.array(pivot_data))
    # data_reshape.append(np.transpose(np.array(resampled_data).reshape(
    #     (time_dim, round((resampled_data.index[-1]-resampled_data.index[0]) / pd.Timedelta(days=1))))))

    for var_code in var_codes[1:]:
        # Calculo medias horarias y coloco los datos en una matriz (ndias, time_dim)
        resampled_data = data[var_code].resample(resampling).mean()
        
        # UTILIZAMOS LA FUNCION pivot_table PARA COLOCAR LOS DATOS EN (NDIAS, 24h)
        pivot_data = pd.DataFrame(resampled_data).pivot_table(index=resampled_data.index.date, columns=resampled_data.index.hour, values=var_code)
        data_reshape.append(np.array(pivot_data))
        
        # data_reshape.append(np.transpose(np.array(resampled_data).reshape(
        #     (time_dim,round((resampled_data.index[-1]-resampled_data.index[0])/ pd.Timedelta(days=1))))))


# Cambios los nan por la media del valor anterior y posterior
data_reshape_final = []
for i in range(len(data_reshape)):
    simple = SimpleImputer().fit(data_reshape[i])
    data_reshape_final.append(simple.transform(data_reshape[i]))

########
## SELECT DE VARIABLE FROM WHICH CLUSTER ANALYSIS WILL BE APPLIED
var_sel = 0 # wd
# var_sel = 1 # ws
# var_sel = 2 # HR
########  
    



# Create the directory if it doesn't exist yet
dir_plots = f'{parent_path}/plots/Cluster-Analisis-calculation/Over-{var_names[var_sel][:2]}'
if not os.path.exists(dir_plots):
    os.makedirs(dir_plots)

########
if cluster_analisis == True:
    ########
    ## SELECTING THE OPTIMAL NUMBER OF CLUSTERS
    # 1- Elbow method.
    kmeans_kwargs = {"init": "random", "n_init": 10, "max_iter": 300}

    # A list holds the SSE values for each k
    sse = []
    for k in range(1, 11):
        kmeans = KMeans(n_clusters=k, **kmeans_kwargs)
        kmeans.fit(data_reshape_final[var_sel])
        sse.append(kmeans.inertia_)

    plt.style.use("fivethirtyeight")
    plt.plot(range(1, 11), sse)
    plt.xticks(range(1, 11))
    plt.xlabel("Number of Clusters")
    plt.ylabel("SSE")
    plt.savefig(f'{dir_plots}/ElbowCoef.jpg')

    plt.show()

    kl = KneeLocator(
        range(1, 11), sse, curve="convex", direction="decreasing")

    n_clusters_elbow = kl.elbow

    # 2- Silhouette coefficient.
    # A list holds the silhouette coefficients for each k
    silhouette_coefficients = []

    # Notice you start at 2 clusters for silhouette coefficient
    for k in range(2, 11):
        kmeans = KMeans(n_clusters=k, **kmeans_kwargs)
        kmeans.fit(data_reshape_final[var_sel])
        score = silhouette_score(data_reshape_final[var_sel], kmeans.labels_)
        silhouette_coefficients.append(score)

    plt.style.use("fivethirtyeight")
    plt.plot(range(2, 11), silhouette_coefficients)
    plt.xticks(range(2, 11))
    plt.xlabel("Number of Clusters")
    plt.ylabel("Silhouette Coefficient")
    plt.savefig(f'{dir_plots}/SilhouetteCoef.jpg')
    plt.show()


    kl_silhouette = KneeLocator(
        range(2, 11), silhouette_coefficients, curve="convex", direction="decreasing")

    n_clusters_silhouette = kl_silhouette.elbow + 1


    # Comparo ambos métodos, y si son iguales, continuo:
    if n_clusters_silhouette == n_clusters_elbow:
        n_clusters = n_clusters_silhouette
    else:
        n_clusters = n_clusters_elbow
        print(f'{n_clusters} is the optimal number os clusters.')

    ########

    ########
    ## APPLY CLUSTER ANALISIS
    print('Appling k-means method...')
    # kmeans = KMeans(n_clusters=3)
    kmeans = KMeans(init="random",  # initialization technique
                    n_clusters=n_clusters,  # sets k for the clustering step
                    # number of initializations to perform (default is 10)
                    n_init=10,
                    max_iter=300)  # number of maximum iterations for each initialization of the k-means algorithm
    kmeans = kmeans.fit(data_reshape_final[var_sel])

    # Obtener las etiquetas de los clusters y los centros
    labels = kmeans.labels_
    centroids = kmeans.cluster_centers_
    ########

    

    ## Print the cluster selection into a .txt and save it:
    datetime_list = data.resample('D').mean().index.to_pydatetime().tolist()

    # Apply strftime on each datetime object in the list
    date_strings = [dt.strftime('%Y-%m-%d') for dt in datetime_list]
    pd.DataFrame(labels+1, index=date_strings).to_csv(f'{dir_plots}Clust_select_days.txt', sep='\t', index=True)

    #########

