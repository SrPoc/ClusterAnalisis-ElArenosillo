# -*- coding: utf-8 -*-
"""
Created on Mon Mar 13 17:12:17 2023

@author: Carlos

sCRIPT PARA CALCULAR LA ANOMALÍA RESPECTO DE LA MEDIA DIARIA DE LOS DATOS DEL DATA_RESHAPE
"""

# Creo un dataframe de los datos de cada variable para calcular su anomalía diaria:
abs_data = pd.DataFrame(data_reshape_final[1], ClustWDSelec.index)
daily_means = aux.mean(axis = 1)

auxx = []
for day_mean in enumerate(daily_means):

    auxx.append(np.array(abs_data)[day_mean[0]]- day_mean[1])

anom_data = np.array(auxx)
