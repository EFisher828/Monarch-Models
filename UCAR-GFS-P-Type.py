import pygrib
import xarray as xr
import urllib.request
import matplotlib.pyplot as plt
from io import BytesIO
from eccodes import *

# ds = xr.open_dataset('./Data/GFS/MostRecent/gfs.t06z.atmf000.nc')
                     
# print(ds.ugrd)

ds = pygrib.open('./Data/GFS/MostRecent/gfs.t06z.sfluxgrbf013.grib2')

for var in ds:
    print(var)