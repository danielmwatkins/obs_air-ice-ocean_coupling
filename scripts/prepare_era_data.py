"""First downloads ERA5 data to file. Then projects onto a polar stereographic grid centered on the North Pole."""
import cdsapi
import xarray as xr
import os
import numpy as np
import pandas as pd
import pyproj
from urllib.request import urlopen
import xesmf as xe

# Settings
start_date = '2020-01-25 00:00'
end_date = '2020-02-05 00:00'
savename = '2020-01-25_2020-02-05'

saveloc = '../data/era5/'
saveloc_regridded = '../data/era5_regridded/'
download = False

if download:
    c = cdsapi.Client(verify=True)
    print('Downloading MSL, U10')
    params = {'product_type': 'reanalysis',
              'format': 'netcdf',
              'variable': ['mean_sea_level_pressure', '10m_u_component_of_wind', '10m_v_component_of_wind'],
              'date': list(pd.date_range(start_date, end_date, freq='1D').strftime('%Y-%m-%d')),
              'time': list(map("{:02d}:00".format, range(0,24))),
              'area': [90, -180, 50, 180]}

    fl = c.retrieve('reanalysis-era5-single-levels', params)
    saveloc = '../data/era5/'
    with urlopen(fl.location) as f:
        with xr.open_dataset(f.read()) as ds:
            ds.to_netcdf(saveloc + 'era5_msl_u10_' + savename + '.nc',
                         encoding={var: {'zlib': True}
                                      for var in ['msl',
                                                  'longitude', 'latitude']})
    print('Downloading q, t, u, v')
    params = {'product_type': 'reanalysis',
              'format': 'netcdf',
              'pressure_level': ['925', '950'],
              'variable': ['specific_humidity',
                           'temperature',
                           'u_component_of_wind',
                           'v_component_of_wind'],
              'date': list(pd.date_range(start_date, end_date, freq='1D').strftime('%Y-%m-%d')),
              'time': list(map("{:02d}:00".format, range(0,24))),
              'area': [90, -180, 50, 180]}

    fl = c.retrieve('reanalysis-era5-pressure-levels', params)
    saveloc = '../data/era5/'
    with urlopen(fl.location) as f:
        with xr.open_dataset(f.read()) as ds:
            ds.to_netcdf(saveloc + 'era5_qtuv_925_950_' + savename + '.nc',
                         encoding={var: {'zlib': True}
                                      for var in ['q', 't', 'u', 'v',
                                                  'longitude', 'latitude']})

print('Regridding')
with xr.open_dataset(saveloc + 'era5_msl_u10_' + savename + '.nc') as ds_msl:
    lon = ds_msl.longitude
    lat = ds_msl.latitude
    lon2d, lat2d = np.meshgrid(lon, lat)

dx = 25e3
xgrid = np.arange(-2e6, 2e6+1, dx)
xgrid, ygrid = np.meshgrid(xgrid, xgrid)

proj_LL = 'epsg:4326' # WGS 84 Ellipsoid
# proj_XY = 'epsg:3413' # NSIDC Polar Stereographic
# Polar stereographic projection with WGS84 datum, central longitude 90, central latitude 90, and true scale latitude 70.
proj_XY = '+proj=stere +lat_0=90 +lat_ts=70 +lon_0=90 +x_0=0 +y_0=0 +datum=WGS84 +units=m +no_defs +type=crs'
transform_to_ll = pyproj.Transformer.from_crs(proj_XY, proj_LL, always_xy=True)

longrid = np.zeros(xgrid.shape)
latgrid = np.zeros(xgrid.shape)
for ii in range(xgrid.shape[0]):
    for jj in range(xgrid.shape[1]):
        lonij, latij = transform_to_ll.transform(xgrid[ii, jj], ygrid[ii, jj])
        longrid[ii, jj] = lonij
        latgrid[ii, jj] = latij
        
datasets = {}
with xr.open_dataset(saveloc + 'era5_msl_u10_' + savename + '.nc') as ds:
    for var in ['msl', 'u10', 'v10']:
        attrs = ds.attrs
        ds_in = xr.Dataset({var: (('time', 'xc', 'yc'), ds[var].data)},
                           coords={'time': (('time',), ds['time'].data),
                                   'lon': (('xc', 'yc'), lon2d),
                                   'lat': (('xc', 'yc'), lat2d)})

        ds_out = xr.Dataset(coords={'lon': (('xc', 'yc'), longrid),
                                    'lat': (('xc', 'yc'), latgrid)})
        regridder = xe.Regridder(ds_in, ds_out, "bilinear")
        ds_regridded = regridder(ds_in)

        if var == 'msl':
            valid = ds_regridded['msl'] > 0
        ds_regridded[var] = ds_regridded[var].where(valid)
        ds_regridded = ds_regridded.assign_coords({'x_stere': (('xc', 'yc'), xgrid),
                                'y_stere': (('xc', 'yc'), ygrid)})
        for x in ds_regridded.attrs:
            attrs[x] = ds_regridded.attrs[x]

        attrs['crs'] = proj_XY
        ds_regridded.attrs = attrs
        datasets[var] = ds_regridded
    
    
with xr.open_dataset(saveloc + 'era5_qtuv_925_950_' + savename + '.nc') as ds:
    for var in ['q', 't', 'u', 'v']:
        for level in [925, 950]:
            attrs = ds.attrs
            ds_sel = ds.sel(level=level)[var].drop('level')
            for x in ds_sel.attrs:
                attrs[x] = ds_sel.attrs[x]

            ds_in = xr.Dataset({var: (('time', 'xc', 'yc'), ds.sel(level=level)[var].data)},
                               coords={'time': (('time',), ds['time'].data),
                                       'lon': (('xc', 'yc'), lon2d),
                                       'lat': (('xc', 'yc'), lat2d)})

            ds_out = xr.Dataset(coords={'lon': (('xc', 'yc'), longrid),
                                        'lat': (('xc', 'yc'), latgrid)})
            regridder = xe.Regridder(ds_in, ds_out, "bilinear")
            ds_regridded = regridder(ds_in)

            ds_regridded[var] = ds_regridded[var].where(valid) # Mask boundaries using SLP > 0
            ds_regridded = ds_regridded.assign_coords({'x_stere': (('xc', 'yc'), xgrid),
                                    'y_stere': (('xc', 'yc'), ygrid)})
            for x in ds_regridded.attrs:
                attrs[x] = ds_regridded.attrs[x]

            attrs['crs'] = proj_XY
            ds_regridded.attrs = attrs
            datasets[var + '_' + str(level)] = ds_regridded.rename({var: var + '_' + str(level)})
            
for var in datasets:
    ds = datasets[var].rename({'lon': 'longitude', 'lat': 'latitude'})
    ds.to_netcdf(saveloc_regridded + 'era5_' + var + '_regridded_' + savename + '.nc',
                     encoding={v: {'zlib': True}
                                  for v in [var, 'longitude', 'latitude']})
