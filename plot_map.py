# -*- coding: utf-8 -*-
"""
Created on Sun Feb 12 01:28:06 2023

@author: Carlos
"""

    import xarray as xr
    import pandas as pd
    import numpy as np
    import csv
    import tqdm
    import cartopy.crs as ccrs
    from cartopy import feature as cf
    import matplotlib.pyplot as plt
    import netCDF4 as nc
    from matplotlib import cm
    
    ncdata = nc.Dataset('C:/Users/Carlos/OneDrive/Documentos/sims_WRF/20220804_20220808_GolfoCadiz/wrfout_d01_2022-08-04.nc')
    
    lat = nc.variables['XLAT'][:]
    lon = nc.variables['XLON'][:]
    u = nc.variables['U'][:]
    v = nc.variables['V'][:]
    
    WS = np.sqrt(u**2+v**2)
    WD = (u,v)
    
    
    
    nlon, nlat = np.meshgrid(lon,lat)
    
    
    fig, ax = plt.subplots(figsize=(12, 12), dpi=300)
    
    # Add Plotting the plot
    ax=plt.subplot(111,projection=ccrs.PlateCarree())
    
    # Add Plot features
    ax.add_feature(cf.BORDERS, linewidth=.5, edgecolor="yellow")
    ax.coastlines('50m', linewidth=0.8)
    # ax.add_feature(cf.LAKES)
    # ax.add_feature(cf.OCEAN)
    ax.add_feature(cf.BORDERS, edgecolor="yellow")
    ax.add_feature(cf.COASTLINE, edgecolor="yellow")
    # ax.add_feature(cf.RIVERS)
    ax.gridlines()
    
    #changing the location of the map
    ax.set_extent([90, 141, 24, -10])
    
    # Add gridlines, and set their font size
    gl = ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=True,
                      linewidth=1, color='black', alpha=0.05, linestyle='-')
    gl.top_labels = False
    gl.left_labels = True
    gl.right_labels = False
    gl.xlines = True
    gl.ylines = True
    
    #colorbar
    cmap = cm.get_cmap('jet') # Colour map coolwarm,hsv,bwr, seismic
    
    # plotting the variables
    pm2p5.plot(transform=ccrs.PlateCarree(), cbar_kwargs={'shrink': 0.5}, cmap=cmap)
    plt.contour(nlon, nlat, pm2p5, fontsize=10,cmap=cmap) #plotting the contours
    
    
    #plotting the quiver
    ax.quiver(X[::3],Y[::3],U[::3,::3],V[::3,::3], color='white')
