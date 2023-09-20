"""Reads in the daily 12 km AMSR data obtained from NSIDC and compiles the files
into a single netcdf file."""

import xarray as xr
import pandas as pd
import numpy as np
import os
import io
import h5py
import pyproj

# Define transformation from latlon to polar stereographic
pol_stere_proj = 'epsg:3411' # 3413 is the newer one, this uses the 1980 ellipsoid
npstere_crs = pyproj.CRS(pol_stere_proj)
source_crs = pyproj.CRS("epsg:4326") # Global lat-lon coordinate system
latlon_to_polar = pyproj.Transformer.from_crs(source_crs, npstere_crs, always_xy=True)

sic_dataloc = '../data/amsr/' # Points to a directory with the daily 12.5km files.
files = [f for f in os.listdir(sic_dataloc) if f != '.DS_Store']
files = [f for f in files if f.split('.')[-1] == 'he5']
files.sort()

with h5py.File(sic_dataloc + files[0]) as ds1:
    lats = ds1['HDFEOS']['GRIDS']['NpPolarGrid12km']['lat'][:, :]
    lons = ds1['HDFEOS']['GRIDS']['NpPolarGrid12km']['lon'][:, :]

# Convert the latitudes and longitudes to polar stereographic coordinates
x, y = latlon_to_polar.transform(np.ravel(lons), np.ravel(lats))
x = np.reshape(x, lons.shape)
y = np.reshape(y, lats.shape)

dates = [pd.to_datetime(f.split('.')[0].split('_')[-1], format='%Y%m%d') for f in files]
data_sic = []
data_motion = []
for file in files:
    with h5py.File(sic_dataloc + file) as ds:
        data_sic.append(ds['HDFEOS']['GRIDS']['NpPolarGrid12km']['Data Fields']['SI_12km_NH_ICECON_DAY'][:,:])
        
        motion = ds['motion'][()]
        df = pd.read_csv(io.BytesIO(motion), skiprows=2, names=['ix', 'iy', 'u', 'v', 'rho'],
            delim_whitespace=True)
        df['ix'] = df.ix.astype(int)
        df['iy'] = df.iy.astype(int)
        data_motion.append(df)

# also pull out the drift data

ds = xr.Dataset({'sea_ice_concentration': (('time', 'y', 'x'), data_sic),
                 'latitude': (('y', 'x'), lats),
                 'longitude': (('y', 'x'), lons)
                },
           coords={'time': ('time', dates),
                   'x_stere': (('y','x'), x),
                   'y_stere': (('y','x'), y)
                 })

ds.attrs = {'sea_ice_concentration': '0: Open Water\n110: Missing\n120: Land\n1-100: Sea ice concentration',
            'crs': 'NSIDC Polar Stereographic North Pole 12.5 km',
            'data_id': 'AU_SI12'}
ds.to_netcdf('../data/amsr_sea_ice_concentration.nc',
             engine='netcdf4',
             encoding={var: {'zlib': True} for var in 
                       ['sea_ice_concentration',
                        'latitude', 'longitude']})