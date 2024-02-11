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
    ds = xr.open_dataset('http://nomads.ncep.noaa.gov:80/dods/gfs_0p25/gfs20240211/gfs_0p25_06z')
        
    cropped_ds = ds.sel(lat=slice(extent[2],extent[3]), lon=slice(extent[0]+360,extent[1]+360))
    
    #crain = np.nanmean(cropped_ds.crainsfc[0:2,:,:],axis=0)
    #csnow = np.nanmean(cropped_ds.csnowsfc[0:2,:,:],axis=0)
    #czr = np.nanmean(cropped_ds.cfrzrsfc[0:2,:,:],axis=0)
    #cip = np.nanmean(cropped_ds.cicepsfc[0:2,:,:],axis=0)
    
    crain = cropped_ds.crainavesfc[int(int(i)/3),:,:]
    csnow = cropped_ds.csnowavesfc[int(int(i)/3),:,:]
    czr = cropped_ds.cfrzravesfc[int(int(i)/3),:,:]
    cip = cropped_ds.cicepavesfc[int(int(i)/3),:,:]
    
    time = datetime.strptime(str(crain.time.data)[0:13],"%Y-%m-%dT%H")
        
    crain_resize = resize(crain,prateShape,order=1)
    csnow_resize = resize(csnow,prateShape,order=1)
    czr_resize = resize(czr,prateShape,order=1)
    cip_resize = resize(cip,prateShape,order=1)
    
    return crain_resize, csnow_resize, czr_resize, cip_resize, time

def buildMap(i, ax, extent):            
    # Split out precip rate, latitude, and longitude
    prate, lat, lon = readLocalData(f'./Data/GFS/MostRecent/{i}.grib2',extent)

    crain, csnow, czr, cip, time = readCloudData(extent,np.array(prate).shape,i)

    prate_rain = np.where(np.logical_and(crain[::-1]>=csnow[::-1],crain[::-1]>=czr[::-1],crain[::-1]>=cip[::-1]),prate,0)
    prate_snow = np.where(np.logical_and(csnow[::-1]>=crain[::-1],csnow[::-1]>=czr[::-1],csnow[::-1]>=cip[::-1]),prate,0)
    prate_zr = np.where(np.logical_and(czr[::-1]>=crain[::-1],czr[::-1]>=csnow[::-1],czr[::-1]>=cip[::-1]),prate,0)
    prate_ip = np.where(np.logical_and(cip[::-1]>=crain[::-1],cip[::-1]>=csnow[::-1],cip[::-1]>=czr[::-1]),prate,0)

    # Define color variables for mapping
    cmap_rain = ml.mapStyle.colors.cmap_rain
    cmap_snow = ml.mapStyle.colors.cmap_snow
    cmap_zr = ml.mapStyle.colors.cmap_zr
    cmap_ip = ml.mapStyle.colors.cmap_ip
    levels_rain = ml.mapStyle.colors.levels_rain
    levels_snow = ml.mapStyle.colors.levels_snow
    levels_zr = ml.mapStyle.colors.levels_zr
    levels_ip = ml.mapStyle.colors.levels_ip
    norm_rain = ml.mapStyle.colors.norm_rain
    norm_snow = ml.mapStyle.colors.norm_snow
    norm_zr = ml.mapStyle.colors.norm_zr
    norm_ip = ml.mapStyle.colors.norm_ip
       
    # Plot prate on map using contour fill         
    
    cs = ax.contourf(lon, lat, ((prate_snow*0.039370)*60*60), cmap=cmap_snow, norm=norm_snow, levels=levels_snow, transform=ccrs.PlateCarree())
    czr = ax.contourf(lon, lat, ((prate_zr*0.039370)*60*60), cmap=cmap_zr, norm=norm_zr, levels=levels_zr, transform=ccrs.PlateCarree())
    cip = ax.contourf(lon, lat, ((prate_ip*0.039370)*60*60), cmap=cmap_ip, norm=norm_ip, levels=levels_ip, transform=ccrs.PlateCarree())
    cr = ax.contourf(lon, lat, ((prate_rain*0.039370)*60*60), cmap=cmap_rain, norm=norm_rain, levels=levels_rain, transform=ccrs.PlateCarree())

    # Remove white space
    plt.gca().set_axis_off()
    plt.subplots_adjust(top = 1, bottom = 0, right = 1, left = 0, hspace = 0, wspace = 0)
    plt.margins(0,0)
    plt.gca().xaxis.set_major_locator(plt.NullLocator())
    plt.gca().yaxis.set_major_locator(plt.NullLocator())

    # Save map
    plt.savefig(f'./Exports/GFS/ptype/{time.strftime("%Y%m%d%H")}.png',bbox_inches='tight',dpi=300,pad_inches=0, transparent=True)
    
    # Remove the rain contours
    for coll1, coll2, coll3, coll4 in zip(cr.collections,cs.collections,czr.collections,cip.collections):
        coll1.remove()
        coll2.remove()
        coll3.remove()
        coll4.remove()
            
def startScript():
    files = glob.glob('./Data/GFS/MostRecent/*')
    for f in files:
        os.remove(f)
        
    files = glob.glob('./Exports/GFS/ptype/*')
    for f in files:
        os.remove(f)
    
    ax, extent = createMap() 

    for i in np.arange(6,246,6):
        i = str(i).zfill(3)
        print(i)
        #url = f'https://nomads.ncep.noaa.gov/pub/data/nccf/com/gfs/prod/gfs.20240204/06/atmos/gfs.t06z.sfluxgrbf{i}.grib2'
        url = f'https://nomads.ncep.noaa.gov/pub/data/nccf/com/gfs/prod/gfs.20240211/06/atmos/gfs.t06z.sfluxgrbf{i}.grib2'
        urllib.request.urlretrieve(url,f'./Data/GFS/MostRecent/{i}.grib2')
        
        buildMap(i,ax,extent)

startScript()