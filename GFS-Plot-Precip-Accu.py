# -*- coding: utf-8 -*-
"""
Created on Sun Dec  3 10:56:52 2023

@author: evanw
"""

import numpy as np
import xarray as xr
import matplotlib.pyplot as plt
from matplotlib.colors import BoundaryNorm
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from datetime import datetime

# Initialize map
fig = plt.figure(figsize=(9, 9))
fig.tight_layout()
ax = plt.axes(projection=ccrs.Mercator()) # Change CRS here as needed

# Set desired map extent
conus_wide = [-143.0,-50.2,16.5,56.8]
conus_extent = [-109.38,-59.91,26.43,51.69]
ax.set_extent(conus_wide,ccrs.PlateCarree())
    
ds = xr.open_dataset('http://nomads.ncep.noaa.gov:80/dods/gfs_0p25/gfs20231231/gfs_0p25_12z')
print(ds)
for i in range(128):
    #Lat: 721  Lon: 1440
    US_y_ind = [410,650]
    US_x_ind = [850,1250]
    
    accu_precip_total = ((ds.apcpsfc[1+i,US_y_ind[0]:US_y_ind[1],US_x_ind[0]:US_x_ind[1]]))*0.03937008
    
    time = datetime.strptime(str(accu_precip_total.time.data)[0:13],"%Y-%m-%dT%H")
            
    
    x = ds.lon.data[US_x_ind[0]:US_x_ind[1]]
    y = ds.lat.data[US_y_ind[0]:US_y_ind[1]]
    
    print(f'Lat: {np.nanmin(y)}:{np.nanmax(y)}')
    print(f'Lon: {np.nanmin(x)}:{np.nanmax(x)}')
    
    xx, yy = np.meshgrid(x,y)

    # Add state and country borders using cartopy's cfeature library
    #ax.add_feature(cfeature.BORDERS)
    #ax.add_feature(cfeature.STATES, linewidth=0.5, zorder=12)
    
    # Define color ramp for snowfall data and create a custom colormap
    #colors = [(0.1,0.1,0.1,0), '#DCDCDC', '#BEBEBE', '#A0A0A0', '#828282', '#B7F0BE', '#9FDBB3', '#87C7A7', '#6FB29C', '#579D90', '#3F8885', '#287479', '#156473','#1450B4','#2A61BB','#4073C3','#5584C9','#6B96D0','#80A7D6','#96B9DE','#ADCAE4','#C1DCEB','#D7EDF2','#CEBCE0','#C9ADDB','#C49ED5','#BF90D0','#BA81CA','#B472C5','#B063BF','#AA55BA','#A546B4','#A037AF','#A63A34','#AD4842','#B5554F','#BD635D','#C6716B','#CE7F79','#D68C86','#DE9A94','#F8EEA2','#EED68C','#E5BD76','#DBA560','#D28C4A','#D28C4A','#AD632D','#965727','#814A21','#6B3E1B','#553115']
    #cmap = plt.cm.colors.ListedColormap(colors)
    #levels = [0,0.01,0.025,0.05,0.075,0.1,0.15,0.2,0.25,0.3,0.35,0.4,0.45,0.5,0.55,0.6,0.65,0.7,0.75,0.8,0.85,0.9,0.95,1,1.1,1.2,1.3,1.4,1.5,1.6,1.7,1.8,1.9,2,2.25,2.5,2.75,3,3.25,3.5,3.75,4,4.5,5,5.5,6,7,8,9,10,12.5,15,1000]
    
    colors = [(0.1,0.1,0.1,0), '#B1EDCF', '#97D8B7', '#7DC19E', '#62AA85', '#48936D', '#2F7E54', '#15673C', '#15678C', '#337E9F', '#5094B6', '#6EACC8', '#8BC4DE','#A9DBF2','#EBD5EB','#D9BED8','#C5A7C5','#B38FB2','#A0779F','#8E5F8D','#7A4779','#682F67','#6C0233','#87253B','#A54945','#C16E4E','#DE9357','#FAC66C','#FBD479','#FDE385','#FEF192','#FFFF9F']
    cmap = plt.cm.colors.ListedColormap(colors)
    levels = [0,0.01,0.05,0.1,0.15,0.2,0.3,0.4,0.5,0.75,1,1.25,1.5,1.75,2,2.5,3,3.5,4,4.5,5,5.5,6,7,8,9,10,12,14,16,20,24,1000]

    # Create a BoundaryNorm to map values to colormap boundaries
    norm = BoundaryNorm(levels, cmap.N, clip=True)
    
    cs = ax.contourf(xx, yy, accu_precip_total, cmap=cmap, norm=norm, levels=levels, transform=ccrs.PlateCarree())
    
    # Remove white space
    plt.gca().set_axis_off()
    plt.subplots_adjust(top = 1, bottom = 0, right = 1, left = 0, hspace = 0, wspace = 0)
    plt.margins(0,0)
    plt.gca().xaxis.set_major_locator(plt.NullLocator())
    plt.gca().yaxis.set_major_locator(plt.NullLocator())
    
    plt.savefig(f'./Exports/GFS/Precip/{time.strftime("%Y%m%d%H")}.png',bbox_inches='tight',dpi=300,pad_inches=0, transparent=True)
        
    # Remove the snow contours
    for coll2 in cs.collections:
        coll2.remove()