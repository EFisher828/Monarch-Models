# -*- coding: utf-8 -*-
"""
Created on Wed Jan 17 03:28:14 2024

@author: Administrator
"""

import os
import ssl
import time
import gzip
import pygrib
import shutil
import xarray as xr
import urllib.request

def createNetCDF(data,lon,lat,nc_file,untar_file):
    # Define a new xarray dataset using reflectivity, latitude, and longitude
    new_ds = xr.Dataset({'ref': (['lat', 'lon'], data)},
                        coords={'lat': lat, 'lon': lon})
    
    # Save dataset as a NetCDF
    new_ds.to_netcdf(nc_file)
    os.remove(untar_file)
    
def fetchData():
    # Define file names
    tar_file = 'C:/Users/Administrator/Documents/SWIFT/Data/MRMS/latest15Reflectivity.grib2.gz'
    untar_file = 'C:/Users/Administrator/Documents/SWIFT/Data/MRMS/latest15Reflectivity.grib2'
    nc_file = 'C:/Users/Administrator/Documents/SWIFT/Data/MRMS/latest15Reflectivity.nc'
    
    # Remove .gz file
    try:
        os.remove(nc_file)
    except:
        print('Could not remove existing files. Check to see if they are missing.')
    
    # Download the data from NCEP
    url = 'https://mrms.ncep.noaa.gov/data/2D/Reflectivity_-15C/MRMS_Reflectivity_-15C.latest.grib2.gz'
    urllib.request.urlretrieve(url,tar_file) 
        
    # Untar and save as .grib2 file
    with gzip.open(tar_file, 'rb') as f_in:
        with open(untar_file, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
         
    # Remove .gz file
    os.remove(tar_file)
    
    # Open .grib2 file and select the data
    MRMS = pygrib.open(untar_file).read(1)[0]

    # Select the values of the data
    data = MRMS.values

    # Select the latitude and longitude grid
    lat, lon = MRMS.latlons()

    # Convert the lat/lon grid from 2D to 1D - necessary for saving as NetCDF
    lon1D = lon[0,:]
    lat1D = lat[:,0]

    # Call function to save NetCDF
    createNetCDF(data,lon1D,lat1D,nc_file,untar_file)

# Workaround for urllib certificate error
ssl._create_default_https_context = ssl._create_unverified_context

# Run script continuously
while (True):
    # Execute the code
    fetchData()
    
    # Code takes 24s to run, then sleep fo 276s. Update triggered every 5 min.
    time.sleep(276)