## IMPORT LIBRARIES
import sys
import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
import datetime as dt
from sklearn.impute import SimpleImputer


def preprocessing(parent_path:str,resampling_atr:str, var_codes):
    """
    Esta funcion toma los datos en formato (tiempo, variable) procedentes de la funcion open_file()
    creada por Alvaro (Intermet) de los .txt de GUMnet y devuelve una lista con arrays para cada 
    variable (var_code) en formato (ndias, 24*resampling_atr)

    Args:
        parent_path (str): path hasta el directorio en que se encuentran los repositorios de Git
        resampling_atr (str): 'hourly' o '10m'
        var_codes (_type_): lista con el codigo de las variables de interes ej. ('G001901.WDIR01#10MN.AVG',....)

    Returns:
        _type_: Los datos ordenados en (ndias, 24*resampling_atr) para aplicar el analisis cluster
                de patrones diarios.
    """    

    ## IMPORT SCRIPTS (REQUIRED TO RUN THIS FUNCTION)
    sys.path.append(f'{parent_path}Git-Repos/ClusterAnalisis-ElArenosillo/GumnetData-import/')
    import import_gumnet_data
    ##
    
    data = import_gumnet_data.open_file(f'{parent_path}Git-Repos/G001901_20220730_20221201_ElArenosillo.txt')

    # var_codes = ('G001901.WDIR01#10MN.AVG', 'G001901.WSPD02#10MN.AVG', 'G001901.WVCN01#10MN.AVG', 'G001901.TMPA01#10MN.AVG')
    # var_names = ('WD (º)', 'WS (m/s)', 'H$_{2}$0 conc. (g/m$^{3}$)', 'T(K)')


    ########
    ## SELECT FRECUENCY DATA FROM WHICH CLUSTER ANALISIS WILL APPLIED
    if resampling_atr == 'hourly':
        resampling = '1H'; time_dim = 24
    elif resampling_atr == '10m': 
        resampling = '10min'; time_dim = 24 *6
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
        
    print('-------------------')
    print(f'{resampling_atr} data is located as follows:')
    print(f'{np.shape(data_reshape_final[0])[0]} days x {np.shape(data_reshape_final[0])[1]} steps per day')
    print('-------------------')
    return data_reshape_final



if __name__ == '__main__':
    var_codes = ('G001901.WDIR01#10MN.AVG', 'G001901.WSPD02#10MN.AVG', 'G001901.WVCN01#10MN.AVG', 'G001901.TMPA01#10MN.AVG')
    data_reshape_final = preprocessing('C:/Users/Carlos/Documents/','hourly', var_codes)

