# -*- coding: utf-8 -*-
"""
Spyder Editor

Script for calculating WS from an .nc file containing u and v

path and filename variables (with extension) should ve created before running
"""
import xarray as xr 
import numpy as np
import pandas as pd
import datetime as dt
import netCDF4



try:
    path
    filename
    
except NameError:
    # print("Path of the .nc file containing u and v components of the wind is not defined (path = ...)")
    # print("Filename of the .nc file containing u and v components of the wind is not defined (filename = ...)")
    path = str(input('Path of the .nc file containing u and v components of the wind: '))
    filename = str(input('Filename: '))



dataorigin = 'ERA5'
variable = 'WS'
wind_data = xr.open_dataset(path+filename)
WS = np.sqrt(wind_data.u**2+wind_data.v**2)


count = 0
idxdate = 0
for j in [np.min(WS.time), np.max(WS.time)]:
    idxdate = idxdate+1
    for i in ['%Y', '%m', '%d']:
        string = str(np.array(j.dt.strftime(i)))
        if count == 0:
            parentstring = string
        elif count !=0 :
            parentstring = str(parentstring+string)
        count = count+1
    idxdate= idxdate+1
    if idxdate == 2:
        parentstring = str(parentstring+'_')
        
        
WS.to_netcdf(variable+'_'+parentstring+'_'+dataorigin + '.nc', format = 'netcdf4')
