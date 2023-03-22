# -*- coding: utf-8 -*-
"""
Created on Wed Mar 15 15:55:29 2023

@author: Carlos
"""

import numpy as np
import pandas as pd
from netCDF4 import Dataset
import netCDF4 as nc
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import xarray as xr
from cartopy import feature as cf
from matplotlib import cm
import sympy as sp

runfile('F:/Tesis/Scripts/GumnetData_import/import_gumnet_data.py', wdir='F:/Tesis/Scripts/GumnetData_import')

ncdata = xr.open_dataset(
    'F:/Tesis/Data/Global Models/ECMWF/ERA5/ERA5_AgSepOct_Europe_Geopotential.DataVerticalLevels.nc')

ncvariables = list(ncdata.keys())

var_names= []
for var_name in ncdata.data_vars:
    var_names.append(ncdata[var_name].attrs)
var_names.append({'units': 'm/s', 'long_name': 'Wind Speed'})
nccoords = list(ncdata.coords)
level = 950

lat = ncdata.latitude.values
lon = ncdata.longitude.values
# levs = ncdat1a.level.values

aux = np.sqrt(ncdata.u10.values**2 + ncdata.u10.values**2)

ncdata = ncdata.assign(WS=(list(ncdata.coords),
                           np.sqrt(ncdata.u10.data**2 + ncdata.u10.data**2)))
ncdata = ncdata.resample(time='1D').mean()

## COMMON PERIOD FOR BOTH DATASETS (ERA5 AND CLUSTER SELECTION)
TinaSelec = pd.read_csv('C:/Users/Carlos/Desktop/Figuras Arenosillo/TinaSBSelection.txt', delimiter='\t', index_col=0)
ClustWDSelec = pd.read_csv('C:/Users/Carlos/Desktop/Figuras Arenosillo/Cluster Analisis/Over WD/Clust_select_days.txt', delimiter='\t', index_col=0)
ClustWDSelec.index = pd.to_datetime(ClustWDSelec.index, format='%Y-%m-%d %H:%M:%S')

intersec = np.intersect1d(ClustWDSelec.index, ncdata.time.values)

# select values within the intersection period
ncdata_intersection = ncdata.where(ncdata.time.isin(intersec), drop=True)

# Cluster asociated to each intersection date:
ClustWDSelec_final = ClustWDSelec.reset_index().iloc[np.where(np.isin(ClustWDSelec.index, intersec))]

# Now we have both, ncdata and clust selection covering the same period.
# We select the days corresponding to each cluster and get the composite map:



clust = np.arange(1,3+1)

nlon, nlat = np.meshgrid(lon,lat)
levels = np.arange(composite_days_ncluster.sst.min(),
                   composite_days_ncluster.sst.max(),
                   (composite_days_ncluster.sst.max()-composite_days_ncluster.sst.min())/10)

fig, ax = plt.subplots(figsize=(12, 12), dpi=300, )
plt.suptitle(f'{var_names[2]["long_name"]}', fontsize=20, fontweight="bold", x=0.3, y=1)
for nclust in clust:
    #Data corrresponding to nclust:
    composite_days_ncluster = ncdata_intersection.isel(time=(ClustWDSelec_final['0'] == nclust)).mean(dim='time')

    
    # Add Plotting the plot
    ax=plt.subplot(3,1,nclust,projection=ccrs.PlateCarree())
    
    # Add Plot features
    # ax.add_feature(cf.BORDERS, linewidth=.5, edgecolor="yellow")
    # ax.coastlines('50m', linewidth=0.8)
    # ax.add_feature(cf.LAKES)
    # ax.add_feature(cf.OCEAN)
    ax.add_feature(cf.BORDERS, edgecolor="black")
    ax.add_feature(cf.COASTLINE, edgecolor="black")
    # ax.add_feature(cf.RIVERS)
    ax.gridlines()
    
    #changing the location of the map
    # ax.set_extent([90, 141, 24, -10])
    
    # Add gridlines, and set their font size
    gl = ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=True,
                      linewidth=1, color='black', alpha=0.05, linestyle='-')
    gl.top_labels = False
    gl.left_labels = True
    gl.right_labels = False
    gl.xlines = True
    gl.ylines = True
    
    #colorbar
    cmap = cm.get_cmap('bwr') # Colour map coolwarm,hsv,bwr, seismic

    im = ax.contourf(nlon, nlat, composite_days_ncluster[ncvariables[2]].values,
                     levels=np.arange(composite_days_ncluster[ncvariables[2]].min(),
                                      composite_days_ncluster[ncvariables[2]].max(),
                                      (composite_days_ncluster[ncvariables[2]].max()-composite_days_ncluster[ncvariables[2]].min())/10),
                     fontsize=10,
                     cmap=cmap)
    im2 = ax.contour(nlon, nlat, composite_days_ncluster[ncvariables[2]].values,
                     levels=np.arange(composite_days_ncluster[ncvariables[2]].min(),
                                      composite_days_ncluster[ncvariables[2]].max(),
                                      (composite_days_ncluster[ncvariables[2]].max()-composite_days_ncluster[ncvariables[2]].min())/10),
                      transform=ccrs.PlateCarree(),
                      linewidths =0.4)
    cbar = fig.colorbar(im, ax=ax, orientation='vertical', shrink=0.6, aspect=20, pad=0.05, extend='both')
    cbar.set_label(var_names[2]['units'], fontsize=12, labelpad=10)
    
    # Add title
    ax.set_title(f"Cluster {nclust}", fontsize=12, fontweight="bold")
plt.tight_layout()
# plt.savefig(f'{dir_plots}/SinopticCompositeMaps_CLusters')

print('Ended.')  
