# -*- coding: utf-8 -*-
"""
Created on Fri Dec  1 14:54:50 2023

@author: evanw
"""

import numpy as np
import xarray as xr
import matplotlib.pyplot as plt
from matplotlib.colors import BoundaryNorm
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from datetime import datetime

ds = xr.open_dataset('http://nomads.ncep.noaa.gov:80/dods/gfs_0p25/gfs20231231/gfs_0p25_12z')
print(ds)
for i in range(128):
    #Lat: 721  Lon: 1440
    US_y_ind = [410,650]
    US_x_ind = [850,1250]
    cat_rain = ds.crainsfc[2+i,US_y_ind[0]:US_y_ind[1],US_x_ind[0]:US_x_ind[1]]
    cat_snow = ds.csnowsfc[2+i,US_y_ind[0]:US_y_ind[1],US_x_ind[0]:US_x_ind[1]]
    
    accu_precip_1 = ((ds.apcpsfc[1+i,US_y_ind[0]:US_y_ind[1],US_x_ind[0]:US_x_ind[1]]))
    accu_precip_2 = ((ds.apcpsfc[2+i,US_y_ind[0]:US_y_ind[1],US_x_ind[0]:US_x_ind[1]]))
    
    time_1 = datetime.strptime(str(accu_precip_1.time.data)[0:13],"%Y-%m-%dT%H")
    time_2 = datetime.strptime(str(accu_precip_2.time.data)[0:13],"%Y-%m-%dT%H")
    
    accu_precip_mean = (accu_precip_2 - accu_precip_1)
    
    accu_snow = (accu_precip_mean.where(cat_snow == 1, 0)*0.03937008)*10
    
    if i == 0:
        accu_snow_total = accu_snow
    else:
        accu_snow_total += accu_snow
    
    x = ds.lon.data[US_x_ind[0]:US_x_ind[1]]
    y = ds.lat.data[US_y_ind[0]:US_y_ind[1]]
    
    print(f'Lat: {np.nanmin(y)}:{np.nanmax(y)}')
    print(f'Lon: {np.nanmin(x)}:{np.nanmax(x)}')
    
    xx, yy = np.meshgrid(x,y)
    
    # Initialize map
    fig = plt.figure(figsize=(9, 9))
    fig.tight_layout()
    ax = plt.axes(projection=ccrs.Mercator()) # Change CRS here as needed
    
    # Add state and country borders using cartopy's cfeature library
    #ax.add_feature(cfeature.BORDERS)
    #ax.add_feature(cfeature.STATES, linewidth=0.5, zorder=12)
    
    # Set desired map extent
    conus_wide = [-143.0,-50.2,16.5,56.8]
    conus_extent = [-109.38,-59.91,26.43,51.69]
    ax.set_extent(conus_wide,ccrs.PlateCarree())
    
    # Define color ramp for snowfall data and create a custom colormap
    colors = [(0.1,0.1,0.1,0), '#E1E1E1', '#C8C8C8', '#AFAFAF', '#969696', '#A9E7F2', '#73BFD7', '#3C98BB', '#0270A0', '#0046B0', '#2864BC', '#4D82C8', '#74A0D3','#9ABEDF','#C1DCEB','#C9ADDB','#C195D2','#B97EC9','#B066C1','#A84FB8','#A037AF','#870A47','#971C5A','#A72D6E','#B63F81','#C65095','#D663A8','#EBA7B7','#E89BA1','#E78F8A','#E38274','#E2765D','#DE6A47','#DC8150','#E19568','#E6A97F','#ECBD97','#F1D1AF','#F6E5C6','#FCF9DE']
    cmap = plt.cm.colors.ListedColormap(colors)
    levels = [0, 0.1, 0.25, 0.5, 0.75, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5, 5.5, 6, 7, 8, 9, 10, 11, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 32, 34, 36, 40, 44, 48, 52, 56, 60, 1000]

    # Create a BoundaryNorm to map values to colormap boundaries
    norm = BoundaryNorm(levels, cmap.N, clip=True)
    
    cs = ax.contourf(xx, yy, accu_snow_total, cmap=cmap, norm=norm, levels=levels, transform=ccrs.PlateCarree())
    
    # Remove white space
    plt.gca().set_axis_off()
    plt.subplots_adjust(top = 1, bottom = 0, right = 1, left = 0, hspace = 0, wspace = 0)
    plt.margins(0,0)
    plt.gca().xaxis.set_major_locator(plt.NullLocator())
    plt.gca().yaxis.set_major_locator(plt.NullLocator())
    
    plt.savefig(f'./Exports/GFS/Snow/{time_2.strftime("%Y%m%d%H")}.png',bbox_inches='tight',dpi=300,pad_inches=0, transparent=True)
        
    # Remove the snow contours
    for coll2 in cs.collections:
        coll2.remove()