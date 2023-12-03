# -*- coding: utf-8 -*-
"""
Created on Fri Dec  1 10:54:25 2023

@author: evanw
"""

import numpy as np
import xarray as xr
import matplotlib.pyplot as plt
from matplotlib.colors import BoundaryNorm
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from datetime import datetime

ds = xr.open_dataset('http://nomads.ncep.noaa.gov:80/dods/gfs_0p25/gfs20231201/gfs_0p25_06z')
print(ds)
for i in range(128):
    #Lat: 721  Lon: 1440
    US_y_ind = [410,650]
    US_x_ind = [850,1250]
    cat_rain = ds.crainsfc[2+i,US_y_ind[0]:US_y_ind[1],US_x_ind[0]:US_x_ind[1]]
    cat_snow = ds.csnowsfc[2+i,US_y_ind[0]:US_y_ind[1],US_x_ind[0]:US_x_ind[1]]
    
    #total_precip = ds.apcpsfc[20,US_y_ind[0]:US_y_ind[1],US_x_ind[0]:US_x_ind[1]]
    accu_precip_1 = ((ds.apcpsfc[1+i,US_y_ind[0]:US_y_ind[1],US_x_ind[0]:US_x_ind[1]]))
    accu_precip_2 = ((ds.apcpsfc[2+i,US_y_ind[0]:US_y_ind[1],US_x_ind[0]:US_x_ind[1]]))
    
    time_1 = datetime.strptime(str(accu_precip_1.time.data)[0:13],"%Y-%m-%dT%H")
    time_2 = datetime.strptime(str(accu_precip_2.time.data)[0:13],"%Y-%m-%dT%H")
    
    time_dif = time_2 - time_1
    hours_dif = int(time_dif.total_seconds()/3600)
    print(f'Hours Difference: {hours_dif}')
    
    accu_precip_mean = (accu_precip_2 - accu_precip_1)/hours_dif
    
    accu_rain = accu_precip_mean.where(cat_rain == 1, 0)
    accu_snow = accu_precip_mean.where(cat_snow == 1, 0)
    
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
    
    colors_rain = [(0.1,0.1,0.1,0),'#00FB4C','#00E445','#00CD3E','#00B537','#009E2E','#018628','#016F20','#005518','#FFFF50','#FCD347','#FBA141','#FF763B','#FF272B','#D80E3A','#B6093D','#900649','#C90DA9','#FF04DC']
    colors_snow = [(0.1,0.1,0.1,0),'#02FEFE','#00EAFD','#01D3FD','#03BFFC','#00AAFC','#0092FC','#0275F2','#0459E8','#073AD6','#0D23C4','#0A1DBB','#05159B','#291099','#490C92','#AC0F8B','#CC0D8F','#FF0C80']
    cmap_rain = plt.cm.colors.ListedColormap(colors_rain)
    cmap_snow = plt.cm.colors.ListedColormap(colors_snow)
    levels_rain = [0,0.1,0.25,0.5,1,1.5,2,2.5,3,4,5,6,8,10,12,16,20,24,28,100]
    levels_snow = [0,0.1,0.25,0.5,0.75,1,1.5,2,2.5,3,3.5,4,5,6,8,10,12,14,100]
    
    # Create a BoundaryNorm to map values to colormap boundaries
    norm_rain = BoundaryNorm(levels_rain, cmap_rain.N, clip=True)
    norm_snow = BoundaryNorm(levels_snow, cmap_snow.N, clip=True)
    
    cr = ax.contourf(xx, yy, accu_rain, cmap=cmap_rain, norm=norm_rain, levels=levels_rain, transform=ccrs.PlateCarree())
    cs = ax.contourf(xx, yy, accu_snow, cmap=cmap_snow, norm=norm_snow, levels=levels_snow, transform=ccrs.PlateCarree())
    
    # Remove white space
    plt.gca().set_axis_off()
    plt.subplots_adjust(top = 1, bottom = 0, right = 1, left = 0, hspace = 0, wspace = 0)
    plt.margins(0,0)
    plt.gca().xaxis.set_major_locator(plt.NullLocator())
    plt.gca().yaxis.set_major_locator(plt.NullLocator())
    
    plt.savefig(f'./Exports/GFS/P-Type/{time_2.strftime("%Y%m%d%H")}.png',bbox_inches='tight',dpi=300,pad_inches=0, transparent=True)
    
    # Remove the rain contours
    for coll1 in cr.collections:
        coll1.remove()
        
    # Remove the snow contours
    for coll2 in cs.collections:
        coll2.remove()