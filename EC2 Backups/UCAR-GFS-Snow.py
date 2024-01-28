# -*- coding: utf-8 -*-
"""
Created on Sun Jan 14 01:59:44 2024

@author: Administrator
"""

import os
import glob
import pygrib
import numpy as np
import xarray as xr
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
from skimage.transform import resize
import monarchlibrary as ml
import urllib.request
from datetime import datetime

def iCheck(i):
    i = str(i)
    if len(i)==1:
        i = '00'+i
    elif len(i)==2:
        i = '0'+i
    return i

def createMap():
    # Initialize map
    fig = plt.figure(figsize=(9, 9))
    fig.tight_layout()
    ax = plt.axes(projection=ccrs.Mercator()) # Change CRS here as needed
    
    # Set desired map extent
    conus_wide = [-143.0,-50.2,16.5,56.8]
    conus_extent = [-109.38,-59.91,26.43,51.69]
    extent = conus_wide
    ax.set_extent(extent,ccrs.PlateCarree())
    
    return ax, extent
    
def readLocalData(data_path,extent):
    # Open the GRIB file
    data_path = data_path
    ds = pygrib.open(data_path)

    # Complete precipitation rate dataset
    ds_prate = ds.select(name='Precipitation rate')[0]
    
    return ds_prate.data(lat1=extent[2],lat2=extent[3],lon1=extent[0]+360,lon2=extent[1]+360)

def readCloudData(extent,prateShape,i):
    # Open the NOMADS GFS file
    ds = xr.open_dataset('http://nomads.ncep.noaa.gov:80/dods/gfs_0p25/gfs20240122/gfs_0p25_12z')
        
    cropped_ds = ds.sel(lat=slice(extent[2],extent[3]), lon=slice(extent[0]+360,extent[1]+360))
    
    #crain = np.nanmean(cropped_ds.crainsfc[0:2,:,:],axis=0)
    #csnow = np.nanmean(cropped_ds.csnowsfc[0:2,:,:],axis=0)
    #czr = np.nanmean(cropped_ds.cfrzrsfc[0:2,:,:],axis=0)
    #cip = np.nanmean(cropped_ds.cicepsfc[0:2,:,:],axis=0)
    
    csnow = cropped_ds.csnowavesfc[int(int(i)/3),:,:]
    
    time = datetime.strptime(str(csnow.time.data)[0:13],"%Y-%m-%dT%H")
        
    csnow_resize = resize(csnow,prateShape,order=1)
    
    return csnow_resize, time

def buildMap(i, ax, extent, total_precip, time, lon, lat):            
    # Define color variables for mapping
    cmap_accuprecip = ml.mapStyle.colors.cmap_accuprecip
    levels_accuprecip = ml.mapStyle.colors.levels_accuprecip
    norm_accuprecip = ml.mapStyle.colors.norm_accuprecip
       
    # Plot prate on map using contour fill         
    cs = ax.contourf(lon, lat, total_precip, cmap=cmap_accuprecip, norm=norm_accuprecip, levels=levels_accuprecip, transform=ccrs.PlateCarree())

    # Remove white space
    plt.gca().set_axis_off()
    plt.subplots_adjust(top = 1, bottom = 0, right = 1, left = 0, hspace = 0, wspace = 0)
    plt.margins(0,0)
    plt.gca().xaxis.set_major_locator(plt.NullLocator())
    plt.gca().yaxis.set_major_locator(plt.NullLocator())

    # Save map
    plt.savefig(f'./Exports/GFS/accuprecip/{time.strftime("%Y%m%d%H")}.png',bbox_inches='tight',dpi=300,pad_inches=0, transparent=True)
    
    # Remove the rain contours
    for coll1 in cs.collections:
        coll1.remove

def startScript():    
    ax, extent = createMap() 

    for i in np.arange(6,246,6):
        i = str(i).zfill(3)
        print(i)
        
        # Split out precip rate, latitude, and longitude
        prate, lat, lon = readLocalData(f'./Data/GFS/MostRecent/{i}.grib2',extent)

        csnow, time = readCloudData(extent,np.array(prate).shape,i)
        
        accuprecip = (prate*0.039370)*60*60*6
        
        if i == '006':
            total_precip = accuprecip
        else:
            total_precip += accuprecip

        buildMap(i,ax,extent,total_precip,time,lon,lat)

startScript()