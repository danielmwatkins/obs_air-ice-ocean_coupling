### test - not sure it runs yet
import xarray as xr
import pandas as pd
import proplot as pplt
import numpy as np
import pyproj
import os

ds_slp= xr.open_dataset('../../data/era5/era5_msl_u10_2020-01-25_2020-02-05.nc')[['msl']]
lonmesh, latmesh = np.meshgrid(ds_slp.longitude, ds_slp.latitude)
pol_stere_proj = 'epsg:3413'
npstere_crs = pyproj.CRS('+proj=stere +lat_0=90 +lat_ts=70 +lon_0=90 +x_0=0 +y_0=0 +datum=WGS84 +units=m +no_defs +type=crs')
source_crs = pyproj.CRS("epsg:4326") # Global lat-lon coordinate system
latlon_to_polar = pyproj.Transformer.from_crs(source_crs, npstere_crs, always_xy=True)
polar_to_latlon = pyproj.Transformer.from_crs(npstere_crs, source_crs, always_xy=True)

X, Y = latlon_to_polar.transform(lonmesh, latmesh)

# Storm track

longitude_orig = ds_slp.longitude.to_numpy()
latitude_orig = ds_slp.latitude.to_numpy()
lon_grid, lat_grid = np.meshgrid(longitude_orig, latitude_orig)
dates = pd.date_range('2020-01-31 00:00', '2020-02-03 10:00', freq='1H')
storm_track = pd.DataFrame(data=np.nan, columns=['longitude', 'latitude', 'center_mslp'], index=dates)
for date in dates:
    if date < pd.to_datetime('2020-02-01 06:00'):
        data_slice = ds_slp.sel(latitude=slice(90, 80)).sel(time=date)
        longitude = data_slice.longitude.to_numpy()
        latitude = data_slice.latitude.to_numpy()
    else:
        data_slice = ds_slp.sel(latitude=slice(90, 60)).isel(longitude=(longitude_orig > 60) | (longitude_orig < -60)
                                                            ).sel(time=date)
        longitude = data_slice.longitude.to_numpy()
        latitude = data_slice.latitude.to_numpy()
        
    x = data_slice['msl'].to_numpy()
    lat_idx, lon_idx = np.where(x==x.min())
    storm_track.loc[date, :] = [longitude[lon_idx[0]], latitude[lat_idx[0]], x.min()]

storm_track['lon_smoothed'] = (storm_track.longitude % 360).rolling(5, center=True).mean()
storm_track['lat_smoothed'] = storm_track.latitude.rolling(5, center=True).mean()
storm_track['msl_smoothed'] = storm_track.center_mslp.rolling(5, center=True).mean()    
x, y = latlon_to_polar.transform(storm_track.lon_smoothed, storm_track.lat_smoothed)
storm_track['x_stere'] = x
storm_track['y_stere'] = y
storm_track.loc['2020-01-31 12:00':'2020-02-02 14:00',:].to_csv('../obs_air-ice-ocean_coupling/data/storm_track.csv')