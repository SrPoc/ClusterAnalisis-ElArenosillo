# -*- coding: utf-8 -*-
"""
Created on Sun Feb 12 01:28:06 2023

@author: Carlos
"""


import xarray as xr
import pandas as pd
import numpy as np
import cartopy.crs as ccrs
from cartopy import feature as cf
import matplotlib.pyplot as plt
import netCDF4 as nc
from matplotlib import colormaps
import cartopy.crs as crs
import cartopy.io.shapereader as shpreader
import wrf
from wrf import (extract_vars, extract_dim, getvar, ALL_TIMES, interplevel, to_np, latlon_coords, get_cartopy,
                 cartopy_xlim, cartopy_ylim)
import geopandas as gpd

#loc = 'lab203'
loc = 'home'

if loc == 'lab203':
    municipios = gpd.read_file('C:/Users/Carlos/Desktop/200001926.shp', driver='ESRI Shapefile')
    ncfile = nc.Dataset('C:/Users/Carlos/Downloads/wrfout_d04_2020-02-19_12_00_00.nc')
    path_plot_data = 'C:/Users/Carlos/Desktop/Figuras Arenosillo/Cluster Analisis/'
elif loc == 'home':
    municipios = gpd.read_file('C:/Users/pablo/Documents/Tesis/Data/Poster _EGU23_BrisaMAdrid/200001926.shp', driver='ESRI Shapefile')
    ncfile = nc.Dataset('C:/Users/pablo/Documents/Tesis/Data/Poster _EGU23_BrisaMAdrid/wrfout_d04_2020-02-19_12_00_00.nc')    
    path_plot_data = 'C:/Users/pablo/Documents/Tesis/ClusterAnalisis-ElArenosillo/Cluster-Plots'
    
    
#distritos = gpd.read_file('/mnt/lustre/home/e5664/wrf/python_scripts/Distritos/Distritos_20210712.shp')

# Define la proyección adecuada
crs = {'init': 'epsg:25830'}

# Asigna la proyección adecuada a las geometrías del objeto 'municipios' y 'distritos'
municipios = municipios.set_crs(crs)
#distritos = distritos.set_crs(crs)

# Transforma las geometrías a la proyección geográfica
municipios = municipios.to_crs(epsg=4326)
#distritos = distritos.to_crs(epsg=4326)





print('----------------------')
print('Las variables contenidas en este .nc son:')
print(ncfile.variables.keys())
print('----------------------')

print('----------------------')
print('Cada una de las variables tiene las siguientes dimensiones:')
print(ncfile.dimensions.keys())
print('----------------------')

print('----------------------')
vars_to_load = ('U10', 'V10', 'T2')
u10 = getvar(ncfile, vars_to_load[0], timeidx=ALL_TIMES, method='join')
v10 = getvar(ncfile, vars_to_load[1], timeidx=ALL_TIMES, method='join')
T2 = getvar(ncfile, vars_to_load[2], timeidx=ALL_TIMES, method='join')
orog = getvar(ncfile, 'HGT', timeidx=0)  # Extract the orography variable
print(f'Se importarán las variables {vars_to_load}')
print('----------------------')

tiempos = pd.to_datetime(to_np(getvar(ncfile, 'times', timeidx=ALL_TIMES, method='cat')))
time_idx = np.where(tiempos == np.datetime64("2020-02-21 07:00:00"))[0][0]
print('----------------------')
print('El indice correspondiente al paso de tiempo "2020-02-21 07:00:00" es :')
print(time_idx)
print('----------------------')
tiempos = tiempos.tz_localize('UTC')



print('----------------------')
print('Los datos de viento (u y v) tienen las siguientes dimensiones:')
print(u10.shape)
print(u10.dims)
print('----------------------')


print('----------------------')
print('Atributes for u10 and wspd are:')
print(u10.attrs)
print('----------------------')

lat = getvar(ncfile, "lat", method='join')
lon = getvar(ncfile, "lon", method='join')

step = 6
fig, ax = plt.subplots(figsize=(12, 8))
m = Basemap(projection='lcc', resolution='h', 
            ax=ax)
m.shadedrelief()


levels = np.arange(np.min(wrf.to_np(T2[time_idx] - 273.16)),
                   np.max(wrf.to_np(T2[time_idx] - 273.16)),
                   .5) # especificamos los niveles de temperatura en intervalos de 2 grados
plt.contourf(to_np(lon), to_np(lat), wrf.to_np(T2[time_idx] - 273.16), levels, cmap='coolwarm')

orog_contours = plt.contour(to_np(lon), to_np(lat), wrf.to_np(orog), levels=np.arange(500,200,5), colors='black', linewidths=1.5)
#plt.clabel(orog_contours, inline=True, fontsize=10, fmt='%d')

# Dibuja los contornos de los municipios y los distritos en el eje
municipios.boundary.plot(ax=ax, color=None, edgecolor='grey', linewidth=0.7, zorder=1)
#distritos.boundary.plot(ax=ax, color=None, edgecolor='black', linewidth=0.7, zorder=1)

cbar = plt.colorbar(ax=ax, shrink=.62)
cbar.set_label('ºC')
q = plt.quiver(to_np(lon[::step,::step]), to_np(lat[::step,::step]),
        to_np(u10[time_idx, ::step, ::step]), to_np(v10[time_idx, ::step, ::step]), width=0.003, scale=100)
qk = plt.quiverkey(q, 1, 1.05, 5, r'$5m/s}$', labelpos='E')
ax.set_title(f'Viento a 10m y temperatura a 2m {str(tiempos[time_idx])}')

#ax.add_feature(cf.LAKES)
#ax.add_feature(cf.RIVERS)

plt.xlim([-4.3,-3.2])
plt.ylim([40.1,41.1])

plt.savefig(f'{path_plot_data}plot_breezes_PosterEGU.png')
plt.show()